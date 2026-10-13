# -*- coding: utf-8 -*-
"""Le compte : déconnexion, fermeture à distance, téléchargement, suppression
(conception, § 3.6, 3.7 et 6)."""
import json
import re

from aide_espace import Client, compte_url, connecter

EMAIL = 'marie@exemple.be'


def appareils(serveur, n=2):
    """n appareils connectés au même espace."""
    liste = [Client(serveur, ip=f'203.0.113.{20 + k}') for k in range(n)]
    for a in liste:
        connecter(serveur, a, EMAIL, prenom='Marie')
    return liste


def test_se_deconnecter_ferme_la_session_de_cet_appareil(serveur):
    a, b = appareils(serveur)
    ancien = a.cookie
    r = a.post(compte_url('deconnexion'))
    assert r.statut == 200 and r.json == {'ok': True}
    assert 'Max-Age=0' in r.entete('Set-Cookie')[0] and a.cookie is None
    assert a.get(compte_url('etat')).json['raison'] is None
    a.cookie = ancien  # le jeton d'avant ne vaut plus rien
    assert a.get(compte_url('etat')).json['raison'] == 'fermee'
    assert b.get(compte_url('etat')).json['connecte'] is True


def test_se_deconnecter_de_tous_les_appareils(serveur):
    a, b = appareils(serveur)
    assert a.post(compte_url('deconnexion-partout')).statut == 200
    assert a.cookie is None
    etat_b = b.get(compte_url('etat')).json
    assert etat_b['connecte'] is False and etat_b['raison'] == 'fermee'
    r = b.post(compte_url('deconnexion'))
    assert r.statut == 401 and r.json['raison'] == 'fermee'
    lignes = serveur.sql('select revoquee_le is not null as fermee from sessions')
    assert len(lignes) == 2 and all(l['fermee'] for l in lignes)


def test_une_session_trop_vieille_est_expiree(serveur):
    (a,) = appareils(serveur, 1)
    serveur.sql("update sessions set expire_le = now() - interval '1 minute'")
    assert a.get(compte_url('etat')).json == {'ouvert': True, 'connecte': False, 'raison': 'expiree'}
    r = a.get(compte_url('export'))
    assert r.statut == 401 and r.json['raison'] == 'expiree'


def test_la_session_est_prolongee_au_plus_une_fois_par_jour(serveur):
    (a,) = appareils(serveur, 1)
    assert a.get(compte_url('etat')).entete('Set-Cookie') == []
    serveur.sql("update sessions set renouvele_le = now() - interval '2 days', expire_le = now() + interval '1 day'")
    serveur.sql("update comptes set vu_le = now() - interval '30 days', averti_le = now()")
    r = a.get(compte_url('etat'))
    assert 'Max-Age=7776000' in r.entete('Set-Cookie')[0]
    (s,) = serveur.sql("select expire_le > now() + interval '89 days' as prolongee from sessions")
    assert s['prolongee'] is True
    (c,) = serveur.sql("select vu_le > now() - interval '1 minute' as vu, averti_le from comptes")
    assert c == {'vu': True, 'averti_le': None}


def test_telecharger_mes_donnees(serveur):
    (a,) = appareils(serveur, 1)
    r = a.get(compte_url('export'))
    assert r.statut == 200
    (disposition,) = r.entete('Content-Disposition')
    assert re.fullmatch(r'attachment; filename="pilotia-mon-espace-\d{4}-\d{2}-\d{2}\.json"', disposition)
    assert r.entete('Cache-Control') == ['no-store']
    donnees = json.loads(r.texte)
    assert donnees['compte']['email'] == EMAIL
    assert donnees['compte']['cree_le'] and donnees['compte']['derniere_connexion']
    assert donnees['fiche'] == {'prenom': 'Marie'}
    assert donnees['diagnostic'] is None and donnees['plan'] is None and donnees['calculs'] is None


def test_sans_connexion_rien_a_telecharger(client):
    r = client.get(compte_url('export'))
    assert r.statut == 401 and r.json['raison'] is None


def test_supprimer_mon_espace_efface_tout(serveur):
    a, b = appareils(serveur)
    assert a.post(compte_url('supprimer')).statut == 400
    r = a.post(compte_url('supprimer'), {'confirmer': True})
    assert r.statut == 200 and a.cookie is None
    for table in ('comptes', 'sessions', 'elements'):
        assert serveur.sql(f'select count(*)::int as n from {table}') == [{'n': 0}]
    assert b.get(compte_url('etat')).json['raison'] == 'fermee'


def test_les_actions_du_compte_viennent_du_site(serveur):
    (a,) = appareils(serveur, 1)
    r = a.post(compte_url('supprimer'), {'confirmer': True}, origine='https://autre-site.example')
    assert r.statut == 403
    assert serveur.sql('select count(*)::int as n from comptes') == [{'n': 1}]
