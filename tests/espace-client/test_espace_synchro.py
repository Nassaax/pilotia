# -*- coding: utf-8 -*-
"""La synchronisation entre deux appareils (conception, § 3.7, 3.8 et 4.3 ;
maquette E3)."""
import pytest
from playwright.sync_api import expect

from aide_espace import (TELEPHONE, appareil, attendre, compte_url, dernier_code, element, lire_local,
                         poser_local)

EMAIL = 'marie@exemple.be'
DIAG = {'date': '2026-10-08T09:00:00.000Z', 'total': 11, 'pill': 'Des failles ciblées',
        'themes': {'Finances': 3}, 'reponses': []}
PLAN = {'version': 3, 'modifie': True, 'soldeDepart': 9000, 'moisDepart': '2026-10', 'horizon': 12,
        'seuil': 5000, 'lignes': [], 'factures': [], 'realise': []}
RESUME = {'montant': 1250, 'mois': 'mars', 'annee': 2027, 'maj': '2026-10-10T08:00:00.000Z'}
OUTILS = ['calculateur-cotisations-independant.html', 'calculateur-cout-salarie.html',
          'calculateur-delai-encaissement.html', 'calculateur-marge.html', 'calculateur-taux-horaire.html',
          'calculateur-tva-franchise.html', 'diagnostic.html', 'rapport-diagnostic.html', 'plan-tresorerie.html']


@pytest.fixture
def deux(navigateur, serveur):
    a = appareil(navigateur, serveur, '203.0.113.70')
    b = appareil(navigateur, serveur, '203.0.113.71')
    yield a, b
    a[0].close()
    b[0].close()


def version(serveur, cle):
    return (element(serveur, cle) or {}).get('version')


def plan_synchronise(serveur, page):
    """Le plan de l'appareil, enregistré dans l'espace (version 1)."""
    poser_local(page, 'pilotia-tresorerie', PLAN)
    poser_local(page, 'pilotia-tresorerie-resume', RESUME)
    page.goto('/mon-espace.html')
    attendre(lambda: lire_local(page, 'pilotia-espace')['sync'].get('plan', {}).get('version') == 1)
    assert element(serveur, 'plan')['valeur'] == {'etat': PLAN, 'resume': RESUME}


def test_le_diagnostic_d_un_appareil_rejoint_l_autre(serveur, deux):
    (_, a, _), (_, b, _) = deux
    poser_local(a, 'pilotia-diagnostic', DIAG)
    a.goto('/mon-espace.html')
    assert attendre(lambda: element(serveur, 'diagnostic'))['valeur'] == DIAG
    b.goto('/mon-espace.html')
    assert attendre(lambda: lire_local(b, 'pilotia-diagnostic')) == DIAG


def test_un_plan_cree_sur_un_appareil_s_ouvre_sur_l_autre(serveur, deux):
    (_, a, _), (_, b, _) = deux
    plan_synchronise(serveur, a)
    b.goto('/plan-tresorerie.html')  # l'exemple d'abord, puis la page se recharge avec le plan
    expect(b.locator('#p-solde')).to_have_value('9000', timeout=8000)


def test_une_modification_part_d_elle_meme_en_quelques_secondes(serveur, deux):
    (_, a, _), _ = deux
    poser_local(a, 'pilotia-diagnostic', DIAG)
    a.goto('/mon-espace.html')
    attendre(lambda: version(serveur, 'diagnostic') == 1)
    poser_local(a, 'pilotia-diagnostic', dict(DIAG, total=12, date='2026-10-12T09:00:00.000Z'))
    attendre(lambda: version(serveur, 'diagnostic') == 2, delai=5)
    assert element(serveur, 'diagnostic')['valeur']['total'] == 12


def test_le_plan_d_exemple_ne_part_jamais(serveur, deux):
    (_, a, _), _ = deux
    a.goto('/plan-tresorerie.html')
    expect(a.locator('#p-solde')).to_have_value('12000')
    a.wait_for_timeout(3500)
    assert element(serveur, 'plan') is None


def test_effacer_le_plan_l_efface_de_l_espace(serveur, deux):
    (_, a, _), _ = deux
    plan_synchronise(serveur, a)
    a.evaluate("localStorage.removeItem('pilotia-tresorerie'); localStorage.removeItem('pilotia-tresorerie-resume')")
    attendre(lambda: element(serveur, 'plan') is None)


def conflit_de_plan(serveur, deux):
    """L'espace reçoit une autre version du plan (5000), puis B modifie le sien
    (7000) sans l'avoir lue."""
    (_, a, client_a), (_, b, _) = deux
    plan_synchronise(serveur, a)
    b.goto('/mon-espace.html')
    attendre(lambda: lire_local(b, 'pilotia-espace')['sync'].get('plan', {}).get('version') == 1)
    r = client_a.put('/api/donnees?cle=plan', {'valeur': {'etat': dict(PLAN, soldeDepart=5000), 'resume': RESUME},
                                               'version': 1})
    assert r.statut == 200 and r.json['version'] == 2
    poser_local(b, 'pilotia-tresorerie', dict(PLAN, soldeDepart=7000))
    feuille = b.locator('dialog.feuille')
    expect(feuille).to_be_visible(timeout=8000)
    expect(feuille.locator('h2')).to_have_text('Votre plan a aussi changé sur un autre appareil')
    expect(feuille.locator('p').first).to_contain_text(
        'Il a été modifié dans votre espace le ')
    expect(feuille.locator('p').first).to_contain_text(', pendant que vous le modifiiez ici. Lequel garder ?')
    expect(feuille.locator('.feuille-note')).to_have_text(
        "La version écartée est remplacée. Pour garder les deux, exportez d'abord celle-ci (bouton en bas du plan).")
    return b, feuille


def test_deux_versions_du_plan_garder_celui_de_cet_appareil_au_clavier(serveur, deux):
    b, feuille = conflit_de_plan(serveur, deux)
    assert b.evaluate('document.activeElement.textContent') == 'Garder celui de cet appareil'
    b.keyboard.press('Enter')
    expect(feuille).to_have_count(0)
    attendre(lambda: version(serveur, 'plan') == 3)
    assert element(serveur, 'plan')['valeur']['etat']['soldeDepart'] == 7000


def test_deux_versions_du_plan_reprendre_celui_de_mon_espace(serveur, deux):
    b, feuille = conflit_de_plan(serveur, deux)
    b.keyboard.press('Tab')
    assert b.evaluate('document.activeElement.textContent') == 'Reprendre celui de mon espace'
    b.keyboard.press('Enter')
    expect(feuille).to_have_count(0)
    assert lire_local(b, 'pilotia-tresorerie')['soldeDepart'] == 5000
    b.wait_for_timeout(3500)
    assert version(serveur, 'plan') == 2


def test_echap_laisse_le_plan_en_attente_sans_reposer_la_question(serveur, deux):
    b, feuille = conflit_de_plan(serveur, deux)
    b.keyboard.press('Escape')
    expect(feuille).to_have_count(0)
    b.wait_for_timeout(3500)
    expect(feuille).to_have_count(0)
    assert version(serveur, 'plan') == 2
    assert lire_local(b, 'pilotia-tresorerie')['soldeDepart'] == 7000
    b.goto('/mon-espace.html')  # la question revient à la page suivante
    expect(feuille).to_be_visible(timeout=8000)


def test_le_meme_plan_des_deux_cotes_ne_pose_pas_de_question(serveur, deux):
    # Un envoi parti à la fermeture d'une page arrive sans que l'appareil lise
    # la réponse : à la page suivante, l'espace a une version plus récente, au
    # même contenu (clés dans un autre ordre, la base ne le garde pas).
    (_, a, client_a), _ = deux
    plan_synchronise(serveur, a)
    modifie = dict(PLAN, soldeDepart=6000)
    assert client_a.put('/api/donnees?cle=plan', {'valeur': {'etat': modifie, 'resume': RESUME},
                                                  'version': 1}).statut == 200
    poser_local(a, 'pilotia-tresorerie', modifie)
    attendre(lambda: lire_local(a, 'pilotia-espace')['sync']['plan']['version'] == 2)
    expect(a.locator('dialog.feuille')).to_have_count(0)
    assert version(serveur, 'plan') == 2


def test_le_diagnostic_le_plus_recent_l_emporte_sans_question(serveur, deux):
    (_, a, client_a), _ = deux
    poser_local(a, 'pilotia-diagnostic', DIAG)
    a.goto('/mon-espace.html')
    attendre(lambda: version(serveur, 'diagnostic') == 1)
    plus_ancien = dict(DIAG, total=5, date='2026-09-01T09:00:00.000Z')
    assert client_a.put('/api/donnees?cle=diagnostic', {'valeur': plus_ancien, 'version': 1}).statut == 200
    poser_local(a, 'pilotia-diagnostic', dict(DIAG, total=14, date='2026-10-13T09:00:00.000Z'))
    attendre(lambda: version(serveur, 'diagnostic') == 3)
    assert element(serveur, 'diagnostic')['valeur']['total'] == 14
    expect(a.locator('dialog.feuille')).to_have_count(0)


def test_les_calculs_sont_fusionnes_outil_par_outil(serveur, deux):
    (_, a, client_a), _ = deux
    a.goto('/mon-espace.html')
    a.wait_for_timeout(300)
    cotisations = {'titre': 'Cotisations sociales', 'champs': {'revenu': '35000', 'statut': 'principal'},
                   'resultat': '1 794 € / trimestre', 'maj': '2026-10-03T10:00:00.000Z'}
    marge = {'titre': 'Marge et seuil de rentabilité', 'champs': {'prixVente': '18'},
             'resultat': '12,00 € de marge · 267 ventes / mois', 'maj': '2026-10-12T14:05:00.000Z'}
    assert client_a.put('/api/donnees?cle=calculs', {'valeur': {'cotisations': cotisations},
                                                     'version': 0}).statut == 200
    e = lire_local(a, 'pilotia-espace')
    e['calculs'] = {'marge': marge}
    poser_local(a, 'pilotia-espace', e)
    attendre(lambda: version(serveur, 'calculs') == 2)
    assert element(serveur, 'calculs')['valeur'] == {'cotisations': cotisations, 'marge': marge}
    assert lire_local(a, 'pilotia-espace')['calculs'] == {'cotisations': cotisations, 'marge': marge}


def test_connexion_expiree_puis_reprise(serveur, deux):
    (_, a, _), _ = deux
    serveur.sql("update sessions set expire_le = now() - interval '1 minute'")
    a.goto('/diagnostic.html')
    attendre(lambda: lire_local(a, 'pilotia-espace')['expire'] is True)
    poser_local(a, 'pilotia-diagnostic', DIAG)  # un résultat obtenu pendant ce temps
    a.wait_for_timeout(3500)
    assert element(serveur, 'diagnostic') is None  # rien ne part
    a.goto('/connexion.html?mode=connexion')
    a.fill('#connexion-email', EMAIL)
    a.click('#etape-email button[type="submit"]')
    expect(a.locator('#etape-code')).to_be_visible()
    a.fill('#connexion-code', dernier_code(serveur, EMAIL))
    a.wait_for_url('**/mon-espace.html')
    assert attendre(lambda: element(serveur, 'diagnostic'))['valeur'] == DIAG
    assert lire_local(a, 'pilotia-espace')['expire'] is False


def test_connexion_fermee_a_distance_l_appareil_se_vide(serveur, deux):
    (_, a, client_a), (_, b, _) = deux
    poser_local(b, 'pilotia-diagnostic', DIAG)
    assert client_a.post(compte_url('deconnexion-partout')).statut == 200
    b.goto('/diagnostic.html')
    attendre(lambda: lire_local(b, 'pilotia-espace') is None)
    assert lire_local(b, 'pilotia-diagnostic') is None
    assert b.evaluate("sessionStorage.getItem('pilotia-message')") == 'fermee'


def test_interrupteur_referme_l_appareil_garde_tout_puis_reprend(serveur, deux):
    (_, a, _), _ = deux
    serveur.env(ESPACE_CLIENT='ferme')
    appels = []
    a.on('request', lambda r: appels.append(r.method) if '/api/donnees' in r.url else None)
    poser_local(a, 'pilotia-diagnostic', DIAG)
    a.goto('/diagnostic.html')
    a.wait_for_timeout(3500)
    assert appels == ['GET']  # une lecture, puis rien tant que l'espace est fermé
    assert lire_local(a, 'pilotia-espace')['expire'] is False
    assert lire_local(a, 'pilotia-diagnostic') == DIAG
    serveur.env(ESPACE_CLIENT='ouvert')
    a.goto('/diagnostic.html')
    assert attendre(lambda: element(serveur, 'diagnostic'))['valeur'] == DIAG


def test_un_plan_trop_volumineux_est_signale_et_ne_repart_pas(serveur, deux):
    (_, a, _), _ = deux
    gros = dict(PLAN, lignes=[{'id': n, 'sens': 'out', 'categorie': 'x' * 900, 'montant': 1,
                               'frequence': 'mensuel', 'decalage': 0} for n in range(300)])
    envois = []
    a.on('request', lambda r: envois.append(r.url) if r.method == 'PUT' and 'cle=plan' in r.url else None)
    poser_local(a, 'pilotia-tresorerie', gros)
    a.goto('/mon-espace.html')
    attendre(lambda: (lire_local(a, 'pilotia-espace').get('erreurs') or {}).get('plan') == 'trop-grand')
    a.wait_for_timeout(3500)
    assert len(envois) == 1
    assert element(serveur, 'plan') is None


@pytest.mark.parametrize('nom', OUTILS)
def test_sans_espace_aucune_requete_sur_les_outils(navigateur, serveur, nom):
    ctx = navigateur.new_context(**TELEPHONE, base_url=serveur.url)
    try:
        page = ctx.new_page()
        appels = []
        page.on('request', lambda r: appels.append(r.url) if '/api/' in r.url else None)
        page.goto('/' + nom)
        page.wait_for_timeout(500)
        assert appels == []
    finally:
        ctx.close()
