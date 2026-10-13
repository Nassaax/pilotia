# -*- coding: utf-8 -*-
"""Lire et écrire le contenu de l'espace : versions, refus et validation
(conception, § 3.4, 3.5, 4.3 et 6)."""
import pytest

from aide_espace import Client, connecter

DIAG = {'date': '2026-10-08T09:00:00.000Z', 'total': 11, 'pill': 'Des failles ciblées',
        'themes': {'Finances': 3, 'Trésorerie & résilience': 2}, 'reponses': []}
PLAN = {'etat': {'version': 3, 'modifie': True, 'soldeDepart': 9000, 'lignes': [], 'factures': [], 'realise': []},
        'resume': {'montant': 1250, 'mois': 'mars', 'annee': 2027, 'maj': '2026-10-10T08:00:00.000Z'}}
CALCULS = {'marge': {'titre': 'Marge et seuil de rentabilité', 'champs': {'prixVente': '18', 'fraisFixes': '3200'},
                     'resultat': '12,00 € de marge · 267 ventes / mois', 'maj': '2026-10-12T14:05:00.000Z'}}


def espace(serveur, email='marie@exemple.be', ip='203.0.113.30', prenom=None):
    c = Client(serveur, ip=ip)
    connecter(serveur, c, email, prenom=prenom)
    return c


def ecrire(c, cle, valeur, version):
    return c.put(f'/api/donnees?cle={cle}', {'valeur': valeur, 'version': version})


def test_sans_connexion_rien_ne_se_lit_ni_ne_s_ecrit(client):
    assert client.get('/api/donnees').statut == 401
    r = ecrire(client, 'plan', PLAN, 0)
    assert r.statut == 401 and r.json['raison'] is None


def test_un_espace_neuf_ne_contient_que_le_prenom(serveur):
    a = espace(serveur, prenom='Marie')
    r = a.get('/api/donnees')
    assert r.statut == 200 and r.entete('Cache-Control') == ['no-store']
    assert set(r.json['elements']) == {'fiche'}
    assert r.json['elements']['fiche']['valeur'] == {'prenom': 'Marie'}
    assert r.json['elements']['fiche']['version'] == 1


def test_chaque_ecriture_monte_la_version(serveur):
    a = espace(serveur)
    r = ecrire(a, 'diagnostic', DIAG, 0)
    assert r.statut == 200 and r.json['version'] == 1 and r.json['maj']
    assert ecrire(a, 'diagnostic', dict(DIAG, total=12), 1).json['version'] == 2
    lu = a.get('/api/donnees').json['elements']['diagnostic']
    assert lu['version'] == 2 and lu['valeur']['total'] == 12


def test_une_ecriture_sur_une_version_depassee_est_refusee(serveur):
    a = espace(serveur)
    b = espace(serveur, ip='203.0.113.31')
    assert ecrire(a, 'plan', PLAN, 0).json['version'] == 1
    r = ecrire(b, 'plan', dict(PLAN, resume=None), 0)
    assert r.statut == 409 and r.json['conflit'] is True
    assert r.json['actuel']['version'] == 1 and r.json['actuel']['valeur'] == PLAN
    assert ecrire(a, 'plan', PLAN, 1).statut == 200
    assert ecrire(b, 'plan', PLAN, 1).statut == 409


def test_effacer_un_element(serveur):
    a = espace(serveur)
    ecrire(a, 'plan', PLAN, 0)
    ecrire(a, 'plan', PLAN, 1)
    assert ecrire(a, 'plan', None, 1).statut == 409
    r = ecrire(a, 'plan', None, 2)
    assert r.statut == 200 and r.json['version'] == 0
    assert 'plan' not in a.get('/api/donnees').json['elements']
    assert ecrire(a, 'plan', None, 2).statut == 200  # déjà effacé ailleurs : rien à faire


def test_la_fiche_est_verifiee_champ_par_champ(serveur):
    a = espace(serveur)
    fiche = {'prenom': '  Marie ', 'entreprise': 'Salon Dupont', 'secteur': '', 'statut': 'principal',
             'tva': 'assujetti', 'chiffreAffaires': 85000, 'fraisFixes': 3200, 'salaries': None}
    r = ecrire(a, 'fiche', fiche, 0)
    assert r.statut == 200
    # Espaces retirés, champs vides omis : la fiche gardée est celle renvoyée.
    assert r.json['valeur'] == {'prenom': 'Marie', 'entreprise': 'Salon Dupont', 'statut': 'principal',
                                'tva': 'assujetti', 'chiffreAffaires': 85000, 'fraisFixes': 3200}


@pytest.mark.parametrize('champ, valeur', [
    ('inconnu', 'x'), ('secteur', 'astronaute'), ('statut', 'salarie'), ('tva', 'oui'),
    ('chiffreAffaires', -1), ('chiffreAffaires', 12.5), ('chiffreAffaires', 1_000_000_001),
    ('fraisFixes', '3200'), ('salaries', 10_001), ('prenom', 'x' * 61), ('entreprise', 'x' * 121),
    ('prenom', 42),
])
def test_une_fiche_invalide_est_refusee(serveur, champ, valeur):
    a = espace(serveur)
    assert ecrire(a, 'fiche', {champ: valeur}, 0).statut == 400


@pytest.mark.parametrize('cle, valeur', [
    ('diagnostic', {'date': '2026-10-08T09:00:00Z', 'themes': {}}),
    ('diagnostic', {'total': 20, 'date': '2026-10-08T09:00:00Z', 'themes': {}}),
    ('diagnostic', {'total': 11, 'date': 'hier', 'themes': {}}),
    ('plan', {'etat': {'lignes': 'aucune'}, 'resume': None}),
    ('plan', ['pas', 'un', 'objet']),
    ('calculs', {'calculateur-pirate': CALCULS['marge']}),
    ('calculs', {'marge': dict(CALCULS['marge'], resultat=None)}),
    ('calculs', {'marge': dict(CALCULS['marge'], champs={'x' * 5: 'y' * 41})}),
])
def test_un_element_de_forme_inattendue_est_refuse(serveur, cle, valeur):
    a = espace(serveur)
    assert ecrire(a, cle, valeur, 0).statut == 400


def test_les_calculs_de_forme_attendue_s_enregistrent(serveur):
    a = espace(serveur)
    r = ecrire(a, 'calculs', CALCULS, 0)
    assert r.statut == 200 and r.json['valeur'] == CALCULS


def test_un_element_trop_volumineux_est_refuse(serveur):
    a = espace(serveur)
    gros = dict(DIAG, reponses=[{'question': 'q' * 1000, 'reponse': 'r'}] * 40)
    assert ecrire(a, 'diagnostic', gros, 0).statut == 413
    plan = {'etat': {'lignes': [{'categorie': 'x' * 1000}] * 300}, 'resume': None}
    assert ecrire(a, 'plan', plan, 0).statut == 413


def test_une_cle_inconnue_ou_une_demande_mal_formee(serveur):
    a = espace(serveur)
    assert ecrire(a, 'secret', {}, 0).statut == 404
    assert a.put('/api/donnees?cle=plan', {'valeur': PLAN}).statut == 400
    assert a.put('/api/donnees?cle=plan', {'valeur': PLAN, 'version': -1}).statut == 400
    assert a.put('/api/donnees?cle=plan', {'valeur': PLAN, 'version': 0},
                 origine='https://autre-site.example').statut == 403


def test_chaque_espace_ne_voit_que_le_sien(serveur):
    a = espace(serveur)
    b = espace(serveur, email='paul@exemple.be', ip='203.0.113.32')
    ecrire(a, 'diagnostic', DIAG, 0)
    assert 'diagnostic' not in b.get('/api/donnees').json['elements']
    assert ecrire(b, 'diagnostic', dict(DIAG, total=3), 0).json['version'] == 1
    assert a.get('/api/donnees').json['elements']['diagnostic']['valeur']['total'] == 11


def test_interrupteur_ferme_plus_de_donnees(serveur):
    a = espace(serveur)
    serveur.env(ESPACE_CLIENT='ferme')
    assert a.get('/api/donnees').statut == 404
