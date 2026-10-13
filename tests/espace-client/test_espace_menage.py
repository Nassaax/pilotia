# -*- coding: utf-8 -*-
"""Le ménage de nuit et la configuration Vercel (conception, § 5 et 6)."""
import json
import re

from aide_espace import RACINE, Client, compte_url, connecter

AUTORISE = {'Authorization': 'Bearer secret-de-test-du-menage'}


def menage(client, entetes=AUTORISE):
    return client.get('/api/menage', entetes=entetes)


def comptes_inactifs(serveur, nombre, depuis, averti=None):
    serveur.sql(
        "insert into comptes (email, conditions_version, vu_le, averti_le) "
        "select 'inactif' || g || '@exemple.be', '2026-10-13', now() - $1::interval, now() - $2::interval "
        "from generate_series(1, $3::int) g", depuis, averti or '100 years', nombre)
    if averti is None:
        serveur.sql("update comptes set averti_le = null where email like 'inactif%'")


def test_sans_le_secret_de_vercel_rien_ne_se_passe(client):
    assert menage(client, {}).statut == 401
    assert menage(client, {'Authorization': 'Bearer devine'}).statut == 401


def test_espace_ferme_le_menage_ne_fait_rien(serveur, client):
    serveur.env(ESPACE_CLIENT='ferme')
    r = menage(client)
    assert r.statut == 200 and r.json == {'ok': True, 'ignore': True}


def test_codes_sessions_et_compteurs_expires_sont_effaces(serveur, client):
    connecter(serveur, Client(serveur, ip='203.0.113.40'), 'marie@exemple.be')
    serveur.sql("insert into codes (email_empreinte, code_empreinte, expire_le) values "
                "('vieux', 'x', now() - interval '2 hours'), ('frais', 'x', now() + interval '5 minutes')")
    serveur.sql("insert into sessions (jeton_empreinte, compte_id, expire_le) "
                "select 'perimee', id, now() - interval '1 day' from comptes")
    serveur.sql("insert into limites (cle, fenetre, nombre) values "
                "('ancien', now() - interval '3 days', 4), ('recent', now(), 1)")
    assert menage(client).statut == 200
    assert {l['email_empreinte'] for l in serveur.sql('select email_empreinte from codes')} == {'frais'}
    assert 'perimee' not in {l['jeton_empreinte'] for l in serveur.sql('select jeton_empreinte from sessions')}
    assert 'ancien' not in {l['cle'] for l in serveur.sql('select cle from limites')}


def test_avertissement_a_23_mois_une_seule_fois(serveur, client):
    comptes_inactifs(serveur, 1, '23 months 1 day')
    assert menage(client).json['avertis'] == 1
    (courriel,) = serveur.courriels()
    assert courriel['to'] == [{'email': 'inactif1@exemple.be'}]
    assert re.fullmatch(r'Votre espace Pilotia sera supprimé le \d{1,2} \w+ \d{4}', courriel['subject'])
    assert 'connectez-vous simplement avant cette date' in courriel['textContent']
    assert 'http' not in courriel['htmlContent']
    assert menage(client).json['avertis'] == 0 and len(serveur.courriels()) == 1


def test_cinquante_avertissements_par_nuit_au_plus(serveur, client):
    comptes_inactifs(serveur, 60, '23 months 1 day')
    assert menage(client).json['avertis'] == 50
    assert menage(client).json['avertis'] == 10


def test_suppression_a_24_mois_si_l_avertissement_date_de_25_jours(serveur, client):
    comptes_inactifs(serveur, 1, '24 months 1 day', averti='26 days')
    serveur.sql("insert into comptes (email, conditions_version, vu_le, averti_le) values "
                "('averti-recemment@exemple.be', 'v', now() - interval '24 months 1 day', now() - interval '10 days'), "
                "('jamais-averti@exemple.be', 'v', now() - interval '24 months 1 day', null)")
    r = menage(client).json
    assert r['supprimes'] == 1 and r['avertis'] == 1 and r['comptes'] == 2
    restants = {l['email'] for l in serveur.sql('select email from comptes')}
    assert restants == {'averti-recemment@exemple.be', 'jamais-averti@exemple.be'}


def test_une_connexion_efface_l_avertissement(serveur, client):
    connecter(serveur, client, 'marie@exemple.be')
    serveur.sql("update comptes set vu_le = now() - interval '23 months 2 days', averti_le = now() - interval '1 day'")
    connecter(serveur, Client(serveur, ip='203.0.113.41'), 'marie@exemple.be')
    (c,) = serveur.sql("select averti_le, vu_le > now() - interval '1 minute' as vu from comptes")
    assert c == {'averti_le': None, 'vu': True}


def test_le_journal_donne_le_nombre_de_comptes_sans_adresse(serveur, client):
    connecter(serveur, client, 'marie@exemple.be')
    menage(client)
    lignes = [l for l in serveur.journal() if l.startswith('menage')]
    assert lignes and 'comptes=1' in lignes[-1]
    assert not any('@' in l for l in serveur.journal())


def test_vercel_fait_tourner_les_fonctions_a_francfort_et_le_menage_chaque_nuit():
    config = json.loads((RACINE / 'vercel.json').read_text(encoding='utf-8'))
    assert config['regions'] == ['fra1']
    (tache,) = config['crons']
    assert tache['path'] == '/api/menage'
    minute, heure, *reste = tache['schedule'].split()
    assert minute.isdigit() and heure.isdigit() and reste == ['*', '*', '*']  # une fois par jour
    assert config['functions']['api/menage.js']['maxDuration'] == 60
    assert config['headers'][0]['source'] == '/(.*)'  # en-têtes de sécurité inchangés
