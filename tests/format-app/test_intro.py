# -*- coding: utf-8 -*-
"""Écran d'ouverture : une fois par visite, jamais en mouvement réduit,
retiré seul, passé d'un toucher, présent sur toutes les pages (un seul bloc)."""
import pytest

from aide import ORDINATEUR, TELEPHONE, ouvrir, pages_du_site, source


@pytest.mark.parametrize('nom', pages_du_site())
def test_un_seul_ecran_juste_apres_body(nom):
    html = source(nom)
    assert html.count('id="intro"') == 1
    assert html.count('<!-- app:intro-tete -->') == 1
    corps = html.index('<body')
    assert html.index('<!-- app:intro -->') == html.index('>', corps) + 1 + 1  # juste après <body>


def test_ecran_puis_page(navigateur, base_url):
    ctx = navigateur.contexte_brut(**ORDINATEUR)
    try:
        page, erreurs = ouvrir(ctx, base_url, 'index.html')
        assert page.locator('html.intro').count() == 1
        assert page.locator('#intro').is_visible()
        page.wait_for_selector('#intro', state='detached', timeout=4500)
        assert page.locator('html.intro').count() == 0
        # Page suivante de la même visite : plus d'écran.
        page.goto(f'{base_url}/offres.html')
        assert page.locator('html.intro').count() == 0
        assert page.locator('#intro').count() == 0
        assert erreurs == []
    finally:
        ctx.close()


def test_un_toucher_passe_l_ecran(navigateur, base_url):
    ctx = navigateur.contexte_brut(**TELEPHONE)
    try:
        page, erreurs = ouvrir(ctx, base_url, 'index.html')
        page.locator('#intro').tap()
        page.wait_for_selector('#intro', state='detached', timeout=1500)
        assert page.evaluate('document.documentElement.scrollWidth') <= 390
        assert erreurs == []
    finally:
        ctx.close()


def test_rien_en_mouvement_reduit(navigateur, base_url):
    ctx = navigateur.contexte_brut(**ORDINATEUR, reduced_motion='reduce')
    try:
        page, _ = ouvrir(ctx, base_url, 'index.html')
        assert page.locator('html.intro').count() == 0
        assert page.locator('#intro').count() == 0
    finally:
        ctx.close()


def test_rien_sans_javascript(navigateur, base_url):
    ctx = navigateur.contexte_brut(**ORDINATEUR, java_script_enabled=False)
    try:
        page = ctx.new_page()
        page.goto(f'{base_url}/index.html')
        assert not page.locator('#intro').is_visible()
    finally:
        ctx.close()
