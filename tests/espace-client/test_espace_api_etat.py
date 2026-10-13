# -*- coding: utf-8 -*-
"""La base, l'interrupteur et l'état de l'espace (conception, § 4.2, 6 et 7)."""
import json

from aide_espace import RACINE, compte_url

TABLES = {'comptes', 'sessions', 'codes', 'elements', 'limites', 'schema_version'}


def test_interrupteur_ferme_l_espace_n_existe_pas(serveur, client):
    serveur.env(ESPACE_CLIENT='ferme')
    r = client.get(compte_url('etat'))
    assert r.statut == 200 and r.json == {'ouvert': False}
    assert client.post(compte_url('demander-code'), {'email': 'a@exemple.be'}).statut == 404
    serveur.env(ESPACE_CLIENT=None)
    assert client.get(compte_url('etat')).json == {'ouvert': False}


def test_interrupteur_ouvert_personne_n_est_connecte(client):
    r = client.get(compte_url('etat'))
    assert r.statut == 200
    assert r.json == {'ouvert': True, 'connecte': False, 'raison': None}
    assert r.entete('Cache-Control') == ['no-store']


def test_les_tables_s_installent_a_la_premiere_requete(serveur, client):
    client.cookie = 'jeton-quelconque'  # sans cookie, « etat » ne touche pas la base
    client.get(compte_url('etat'))
    lignes = serveur.sql("select tablename from pg_tables where schemaname = 'public'")
    assert TABLES <= {l['tablename'] for l in lignes}


def test_une_action_inconnue_ou_une_mauvaise_methode_est_refusee(client):
    assert client.get(compte_url('pirater')).statut == 404
    assert client.post(compte_url('etat')).statut == 405


def test_un_cookie_inconnu_vaut_une_connexion_fermee(client):
    client.cookie = 'jeton-que-le-serveur-ne-connait-pas'
    assert client.get(compte_url('etat')).json['raison'] == 'fermee'


def test_le_pilote_neon_est_fixe_a_une_version_exacte():
    version = json.loads((RACINE / 'package.json').read_text())['dependencies']['@neondatabase/serverless']
    assert version[0].isdigit(), version
