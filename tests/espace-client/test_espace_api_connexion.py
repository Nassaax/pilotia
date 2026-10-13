# -*- coding: utf-8 -*-
"""Codes de connexion et création d'espace (conception, § 3.2 et 5)."""
import pytest

from aide_espace import COOKIE, Client, compte_url, connecter, dernier_code

EMAIL = 'marie@exemple.be'


def demander(client, email=EMAIL, **autres):
    return client.post(compte_url('demander-code'), dict(email=email, **autres))


def verifier(client, code, email=EMAIL, **autres):
    return client.post(compte_url('verifier-code'), dict(email=email, code=code, **autres))


def rajeunir(serveur):
    """Fait comme si la dernière demande de code datait de plus d'une minute."""
    serveur.sql("update codes set envoye_le = envoye_le - interval '2 minutes'")


def test_le_code_part_par_email_sans_lien_et_avec_une_version_texte(serveur, client):
    r = demander(client, 'Marie@Exemple.be ')
    assert r.statut == 200 and r.json == {'ok': True}
    (courriel,) = serveur.courriels()
    assert courriel['to'] == [{'email': EMAIL}]
    assert courriel['sender']['name'] == 'Pilotia'
    code = dernier_code(serveur, EMAIL)
    assert courriel['subject'] == f'Votre code Pilotia : {code[:3]} {code[3:]}'
    for version in (courriel['htmlContent'], courriel['textContent']):
        assert f'{code[:3]} {code[3:]}' in version
        assert 'valable 10 minutes' in version and 'http' not in version


def test_la_reponse_est_la_meme_qu_un_espace_existe_ou_non(serveur, client):
    connecter(serveur, Client(serveur, ip='203.0.113.50'), EMAIL)
    rajeunir(serveur)
    assert demander(client).json == demander(client, 'inconnu@exemple.be').json == {'ok': True}


def test_le_champ_leurre_rempli_n_envoie_rien(serveur, client):
    r = demander(client, website='https://robot.example')
    assert r.statut == 200 and r.json == {'ok': True}
    assert serveur.courriels() == []


@pytest.mark.parametrize('email', ['', 'pas-une-adresse', 'a@b', 'x' * 200 + '@exemple.be', 42])
def test_une_adresse_invalide_est_refusee(serveur, client, email):
    assert demander(client, email).statut == 400
    assert serveur.courriels() == []


def test_une_demande_venue_d_un_autre_site_est_refusee(serveur, client):
    url = compte_url('demander-code')
    assert client.post(url, {'email': EMAIL}, origine='https://autre-site.example').statut == 403
    assert client.post(url, {'email': EMAIL}, origine='').statut == 403
    assert client.post(compte_url('demander-code'), f'email={EMAIL}', type_json=False,
                       entetes={'Content-Type': 'application/x-www-form-urlencoded'}).statut == 403
    assert serveur.courriels() == []


def test_si_brevo_echoue_aucun_code_ne_reste_en_attente(serveur, client):
    serveur.env(TEST_BREVO_ECHEC='1')
    r = demander(client)
    assert r.statut == 502 and 'Réessayez' in r.json['erreur']
    assert serveur.sql('select count(*)::int as n from codes') == [{'n': 0}]
    assert EMAIL not in ' '.join(serveur.journal())


def test_le_code_n_est_garde_que_sous_forme_d_empreinte(serveur, client):
    demander(client)
    code = dernier_code(serveur, EMAIL)
    (ligne,) = serveur.sql('select email_empreinte, code_empreinte from codes')
    assert code not in str(ligne) and EMAIL not in str(ligne)


def test_creation_en_deux_temps_puis_connexion(serveur, client):
    demander(client)
    code = dernier_code(serveur, EMAIL)
    r = verifier(client, code)
    assert r.statut == 200 and r.json == {'ok': True, 'nouveau': True}
    assert client.cookie is None
    r = verifier(client, code, prenom='  Marie ', conditions=True)
    assert r.statut == 200
    assert r.json['connecte'] is True and r.json['cree'] is True and r.json['prenom'] == 'Marie'
    assert len(r.json['compte']) == 16
    (cookie,) = r.entete('Set-Cookie')
    for attribut in ('HttpOnly', 'Secure', 'SameSite=Strict', 'Path=/', 'Max-Age=7776000'):
        assert attribut in cookie
    assert cookie.startswith(COOKIE + '=') and client.cookie
    etat = client.get(compte_url('etat')).json
    assert etat == {'ouvert': True, 'connecte': True, 'compte': r.json['compte'],
                    'email': EMAIL, 'prenom': 'Marie'}
    (compte,) = serveur.sql('select conditions_version from comptes')
    assert compte['conditions_version']


def test_un_espace_existant_se_connecte_directement(serveur, client):
    cree = connecter(serveur, Client(serveur, ip='203.0.113.51'), EMAIL, prenom='Marie')
    rajeunir(serveur)
    demander(client)
    r = verifier(client, dernier_code(serveur, EMAIL))
    assert r.json['connecte'] is True and r.json['cree'] is False
    assert r.json['compte'] == cree['compte'] and r.json['prenom'] == 'Marie'


def test_un_code_ne_sert_qu_une_fois(serveur, client):
    demander(client)
    code = dernier_code(serveur, EMAIL)
    assert verifier(client, code, conditions=True).statut == 200
    assert verifier(Client(serveur), code).statut == 410


def test_cinq_essais_au_plus(serveur, client):
    demander(client)
    bon = dernier_code(serveur, EMAIL)
    faux = '000000' if bon != '000000' else '111111'
    r = verifier(client, faux)
    assert r.statut == 400 and r.json['essaisRestants'] == 4
    assert 'Il vous reste 4 essais' in r.json['erreur']
    for _ in range(3):
        verifier(client, faux)
    r = verifier(client, faux)
    assert r.statut == 429 and 'Demandez un nouveau code' in r.json['erreur']
    assert verifier(client, bon, conditions=True).statut == 429


def test_un_code_expire_au_bout_de_dix_minutes(serveur, client):
    demander(client)
    serveur.sql("update codes set expire_le = now() - interval '1 second'")
    assert verifier(client, dernier_code(serveur, EMAIL), conditions=True).statut == 410


def test_un_code_juste_pour_une_nouvelle_adresse_tient_quinze_minutes(serveur, client):
    demander(client)
    code = dernier_code(serveur, EMAIL)
    verifier(client, code)
    (ligne,) = serveur.sql("select expire_le > now() + interval '14 minutes' as prolonge from codes")
    assert ligne['prolonge'] is True
    assert verifier(client, code, conditions=True).json['cree'] is True


def test_un_nouveau_code_remplace_le_precedent(serveur, client):
    demander(client)
    ancien = dernier_code(serveur, EMAIL)
    rajeunir(serveur)
    demander(client)
    nouveau = dernier_code(serveur, EMAIL)
    if ancien != nouveau:
        assert verifier(client, ancien, conditions=True).statut == 400
    assert verifier(client, nouveau, conditions=True).statut == 200


def test_une_minute_entre_deux_demandes(serveur, client):
    assert demander(client).statut == 200
    r = demander(client)
    assert r.statut == 429 and 'une minute' in r.json['erreur']
    assert len(serveur.courriels()) == 1


def test_cinq_codes_par_heure_pour_une_adresse(serveur, client):
    for _ in range(5):
        assert demander(client).statut == 200
        rajeunir(serveur)
    assert demander(client).statut == 429


def test_vingt_codes_par_heure_pour_un_reseau(serveur, client):
    for n in range(20):
        assert demander(client, f'personne{n}@exemple.be').statut == 200
    assert demander(client, 'encore@exemple.be').statut == 429
    assert demander(Client(serveur, ip='198.51.100.7'), 'encore@exemple.be').statut == 200


def test_deux_cents_codes_par_jour_pour_tout_le_site(serveur, client):
    serveur.sql("insert into limites (cle, fenetre, nombre) values ('code:site', date_trunc('day', now()), 200)")
    r = demander(client)
    assert r.statut == 429 and 'très demandé' in r.json['erreur']
    assert serveur.courriels() == []


def test_trente_verifications_par_heure_pour_un_reseau(serveur, client):
    for _ in range(30):
        verifier(client, '123456', email='personne@exemple.be')
    assert verifier(client, '123456', email='personne@exemple.be').statut == 429


def test_un_code_mal_forme_est_refuse_sans_compter_d_essai(serveur, client):
    demander(client)
    for code in ('12345', 'abcdef', '1234567', 123456):
        assert verifier(client, code).statut == 400
    (ligne,) = serveur.sql('select essais from codes')
    assert ligne['essais'] == 0
