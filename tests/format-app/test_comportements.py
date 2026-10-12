# -*- coding: utf-8 -*-
"""Panneau « Plus », barre masquée pendant la saisie, aucune erreur JavaScript."""
import pytest
from playwright.sync_api import expect

from aide import TELEPHONE, ouvrir, pages_du_site
from test_coquille import CONTRASTE

OUVERT = "document.getElementById('panneauPlus').open"


def test_le_panneau_s_ouvre_et_se_ferme(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    bouton = page.locator('#navToggle')
    bouton.click()
    assert page.evaluate(OUVERT)
    expect(bouton).to_have_attribute('aria-expanded', 'true')
    page.keyboard.press('Escape')
    assert not page.evaluate(OUVERT)
    # L'évènement « close » d'un <dialog> arrive juste après : expect attend.
    expect(bouton).to_have_attribute('aria-expanded', 'false')
    expect(bouton).to_be_focused()
    bouton.click()
    page.locator('.plus-fermer').click()
    assert not page.evaluate(OUVERT)
    bouton.click()
    page.mouse.click(195, 60)  # sur le voile, au-dessus du panneau
    assert not page.evaluate(OUVERT)
    assert erreurs == []


def test_le_panneau_signale_la_page_courante(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'cgv.html')
    page.locator('#navToggle').click()
    assert page.locator('.plus-liste a[aria-current="page"]').inner_text().strip() == 'Conditions générales'
    page.locator('.plus-liste a', has_text='À propos').click()
    page.wait_for_url('**/a-propos.html')


@pytest.mark.parametrize('schema', ['light', 'dark'])
def test_contrastes_du_panneau(schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, _ = ouvrir(ctx, base_url, 'index.html')
        page.locator('#navToggle').click()
        for sel in ('.plus-titre', '.plus-groupe', '.plus-liste a'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
    finally:
        ctx.close()


def test_la_saisie_masque_la_barre(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'calculateur-marge.html')
    page.focus('#prixVente')
    page.wait_for_timeout(100)
    assert not page.locator('.onglets').is_visible()
    page.evaluate('document.activeElement.blur()')
    page.wait_for_timeout(150)
    assert page.locator('.onglets').is_visible()


@pytest.mark.parametrize('nom', pages_du_site())
def test_aucune_erreur_javascript(nom, telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, nom)
    page.wait_for_timeout(200)
    assert erreurs == []
