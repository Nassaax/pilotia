# -*- coding: utf-8 -*-
"""La page de connexion, sur téléphone (conception, § 3.2 et 3.7 ; maquette E1)."""
import json

import pytest
from playwright.sync_api import expect

from aide_espace import BOITES, CONTRASTE, TELEPHONE, Client, connecter, dernier_code, ouvrir

EMAIL = 'marie@exemple.be'
DIAG = {'date': '2026-10-08T09:00:00.000Z', 'total': 11, 'pill': 'Des failles ciblées',
        'themes': {'Finances': 3}, 'reponses': []}
PLAN = {'version': 3, 'modifie': True, 'soldeDepart': 9000, 'moisDepart': '2026-10', 'horizon': 12,
        'seuil': 5000, 'lignes': [], 'factures': [], 'realise': []}
AUTRE = {'compte': '0123456789abcdef', 'prenom': 'Paul', 'fiche': {}, 'calculs': {}, 'sync': {}}


def poser(page, cle, valeur):
    page.evaluate('([c, v]) => localStorage.setItem(c, v)', [cle, json.dumps(valeur)])


def lire(page, cle):
    return page.evaluate('(c) => JSON.parse(localStorage.getItem(c))', cle)


def saisir_email(page, email=EMAIL):
    page.fill('#connexion-email', email)
    page.click('#etape-email button[type="submit"]')
    expect(page.locator('#etape-code')).to_be_visible()


def test_espace_ferme_la_page_le_dit(serveur, telephone):
    serveur.env(ESPACE_CLIENT='ferme')
    page, erreurs = ouvrir(telephone, '/connexion.html')
    expect(page.locator('#connexion-ferme')).to_be_visible()
    expect(page.locator('h1')).to_have_text('Mon espace')
    for etape in ('#etape-email', '#etape-code', '#etape-bienvenue'):
        expect(page.locator(etape)).to_be_hidden()
    assert erreurs == []


def test_le_titre_suit_le_lien_suivi(telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    expect(page.locator('#etape-email')).to_be_visible()
    expect(page.locator('h1')).to_have_text('Créer mon espace')
    page, _ = ouvrir(telephone, '/connexion.html?mode=connexion')
    expect(page.locator('h1')).to_have_text('Me connecter')


def test_creation_avec_les_resultats_deja_sur_l_appareil(serveur, telephone):
    page, erreurs = ouvrir(telephone, '/connexion.html')
    poser(page, 'pilotia-diagnostic', DIAG)
    poser(page, 'pilotia-tresorerie', PLAN)
    saisir_email(page)
    expect(page.locator('h1')).to_have_text('Entrez votre code')
    expect(page.locator('#code-adresse')).to_have_text(EMAIL)
    assert page.evaluate('document.activeElement.id') == 'connexion-titre'
    page.fill('#connexion-code', dernier_code(serveur, EMAIL))  # le sixième chiffre valide
    expect(page.locator('h1')).to_have_text('Votre espace est presque prêt')
    expect(page.locator('#bienvenue-liste li')).to_have_text(
        ['Diagnostic express, fait le 8 octobre', 'Plan de trésorerie'])
    page.fill('#bienvenue-prenom', 'Marie')
    page.click('#etape-bienvenue button[type="submit"]')
    expect(page.locator('#bienvenue-erreur')).to_have_text(
        "Cochez la case pour accepter les conditions d'utilisation.")
    page.check('#bienvenue-conditions')
    page.click('#etape-bienvenue button[type="submit"]')
    page.wait_for_url('**/mon-espace.html')
    e = lire(page, 'pilotia-espace')
    assert len(e['compte']) == 16 and e['prenom'] == 'Marie' and e['expire'] is False
    assert lire(page, 'pilotia-diagnostic')['total'] == 11  # rejoindra l'espace à la synchronisation
    assert page.evaluate("sessionStorage.getItem('pilotia-message')") == 'cree'
    assert [c['name'] for c in telephone.cookies()] == ['__Host-pilotia-session']
    assert erreurs == []


def test_sans_resultat_sur_l_appareil_pas_d_encadre(serveur, telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    saisir_email(page)
    page.fill('#connexion-code', dernier_code(serveur, EMAIL))
    expect(page.locator('#etape-bienvenue')).to_be_visible()
    expect(page.locator('#bienvenue-import')).to_be_hidden()


def test_un_espace_existant_entre_directement(serveur, telephone):
    connecter(serveur, Client(serveur, ip='203.0.113.60'), EMAIL, prenom='Marie')
    page, _ = ouvrir(telephone, '/connexion.html?mode=connexion')
    saisir_email(page)
    page.fill('#connexion-code', dernier_code(serveur, EMAIL))
    page.wait_for_url('**/mon-espace.html')
    assert lire(page, 'pilotia-espace')['prenom'] == 'Marie'
    assert page.evaluate("sessionStorage.getItem('pilotia-message')") == 'connecte'


def test_un_code_faux_est_annonce(serveur, telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    saisir_email(page)
    bon = dernier_code(serveur, EMAIL)
    page.fill('#connexion-code', '000000' if bon != '000000' else '111111')
    expect(page.locator('#code-erreur')).to_have_text('Ce code ne correspond pas. Il vous reste 4 essais.')
    assert page.locator('#code-erreur').get_attribute('role') == 'alert'


def test_un_code_expire_propose_un_nouveau_code(serveur, telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    saisir_email(page)
    serveur.sql("update codes set expire_le = now() - interval '1 second'")
    page.fill('#connexion-code', dernier_code(serveur, EMAIL))
    expect(page.locator('#code-erreur')).to_have_text('Ce code a expiré. Demandez-en un nouveau.')
    bouton = page.locator('#code-renvoyer')
    expect(bouton).to_have_text('Recevoir un nouveau code')
    expect(bouton).to_be_enabled()
    serveur.sql("update codes set envoye_le = envoye_le - interval '2 minutes'")
    bouton.click()
    expect(page.locator('#code-erreur')).to_have_text('Un nouveau code vient de partir.')
    assert len([c for c in serveur.courriels() if c['to'][0]['email'] == EMAIL]) == 2


def test_renvoyer_le_code_apres_une_minute(telephone):
    page = telephone.new_page()
    page.clock.install()
    page.goto('/connexion.html')
    saisir_email(page)
    expect(page.locator('#code-renvoyer')).to_be_disabled()
    page.clock.fast_forward(61000)
    expect(page.locator('#code-renvoyer')).to_be_enabled()


def test_modifier_l_adresse(telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    saisir_email(page)
    page.click('#code-modifier')
    expect(page.locator('#etape-email')).to_be_visible()
    expect(page.locator('h1')).to_have_text('Créer mon espace')


def test_une_adresse_invalide_ne_part_pas(serveur, telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    page.fill('#connexion-email', 'pas-une-adresse')
    page.click('#etape-email button[type="submit"]')
    expect(page.locator('#email-erreur')).to_have_text(
        'Entrez une adresse email valide, par exemple nom@entreprise.be.')
    assert serveur.courriels() == []


def test_un_autre_espace_sur_l_appareil_est_efface_apres_accord(serveur, telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    poser(page, 'pilotia-espace', AUTRE)
    poser(page, 'pilotia-diagnostic', DIAG)
    page.on('dialog', lambda d: d.accept())
    connecter(serveur, Client(serveur, ip='203.0.113.61'), EMAIL)
    saisir_email(page)
    page.fill('#connexion-code', dernier_code(serveur, EMAIL))
    page.wait_for_url('**/mon-espace.html')
    assert lire(page, 'pilotia-espace')['compte'] != AUTRE['compte']
    assert lire(page, 'pilotia-diagnostic') is None


def test_refuser_garde_les_donnees_de_l_autre_espace(serveur, telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    poser(page, 'pilotia-espace', AUTRE)
    page.on('dialog', lambda d: d.dismiss())
    connecter(serveur, Client(serveur, ip='203.0.113.62'), EMAIL)
    saisir_email(page)
    page.fill('#connexion-code', dernier_code(serveur, EMAIL))
    expect(page.locator('#email-erreur')).to_have_text(
        "Connexion annulée : les données de l'autre espace restent sur cet appareil.")
    assert lire(page, 'pilotia-espace')['compte'] == AUTRE['compte']
    expect(page.locator('#etape-email')).to_be_visible()


def test_deja_connecte_la_page_renvoie_vers_mon_espace(serveur, telephone):
    page, _ = ouvrir(telephone, '/connexion.html')
    saisir_email(page)
    page.fill('#connexion-code', dernier_code(serveur, EMAIL))
    page.check('#bienvenue-conditions')
    page.click('#etape-bienvenue button[type="submit"]')
    page.wait_for_url('**/mon-espace.html')
    page.goto('/connexion.html')
    page.wait_for_url('**/mon-espace.html')


def test_sans_javascript_aucune_etape_ne_s_affiche(navigateur, serveur):
    # Le message <noscript> est vérifié dans le source (test_espace_pages) : Chromium
    # piloté sans JavaScript ne l'affiche pas, contrairement à un vrai navigateur.
    ctx = navigateur.new_context(**TELEPHONE, java_script_enabled=False, base_url=serveur.url)
    try:
        page = ctx.new_page()
        page.goto('/connexion.html')
        for etape in ('#etape-email', '#etape-code', '#etape-bienvenue', '#connexion-ferme'):
            expect(page.locator(etape)).to_be_hidden()
    finally:
        ctx.close()


@pytest.mark.parametrize('schema', ['light', 'dark'])
def test_contrastes_et_cibles_au_pouce(navigateur, serveur, schema):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema, base_url=serveur.url)
    try:
        page, erreurs = ouvrir(ctx, '/connexion.html')
        page.fill('#connexion-email', 'pas-une-adresse')
        page.click('#etape-email button[type="submit"]')
        for sel in ('#etape-email label', '#etape-email .lead', '.espace-petit', '#email-erreur'):
            ratios = page.evaluate(CONTRASTE, sel)
            assert ratios and min(ratios) >= 4.5, (sel, schema, ratios)
        for sel in ('#connexion-email', '#etape-email button[type="submit"]'):
            for largeur, hauteur in page.evaluate(BOITES, sel):
                assert hauteur >= 48, (sel, hauteur)
        saisir_email(page)
        for largeur, hauteur in page.evaluate(BOITES, '#code-renvoyer, #connexion-code'):
            assert hauteur >= 48
        assert erreurs == []
    finally:
        ctx.close()
