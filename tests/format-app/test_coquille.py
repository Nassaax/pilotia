# -*- coding: utf-8 -*-
"""La coquille d'app s'affiche en mode app et seulement là (§ 3 de la conception)."""
import pytest

from aide import LARGEURS, TELEPHONE, attendu, ouvrir, pages_du_site

PAGES = pages_du_site()

CONTRASTE = r"""(sel) => {
  const lin = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = c => { const [r, g, b] = c.match(/[\d.]+/g).map(Number);
                     return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b); };
  const fond = el => {
    for (; el; el = el.parentElement) {
      const c = getComputedStyle(el).backgroundColor;
      const p = c.match(/[\d.]+/g).map(Number);
      if (p.length < 4 || p[3] > 0.99) return c;
    }
    return 'rgb(255, 255, 255)';
  };
  return [...document.querySelectorAll(sel)]
    .filter(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden')
    .map(e => { const a = lum(getComputedStyle(e).color), b = lum(fond(e));
                return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); });
}"""

BOITES = """(sel) => [...document.querySelectorAll(sel)].filter(e => e.getClientRects().length)
  .map(e => { const r = e.getBoundingClientRect(); return [r.width, r.height]; })"""


@pytest.mark.parametrize('nom', PAGES)
def test_barre_en_mode_app_seulement(nom, telephone, ordinateur, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    assert page.locator('.onglets').is_visible()
    assert not page.locator('.nav-links').is_visible()
    page, _ = ouvrir(ordinateur, base_url, nom)
    assert not page.locator('.onglets').is_visible()
    assert not page.locator('.app-retour').is_visible()
    assert page.locator('.nav-links').is_visible()


@pytest.mark.parametrize('nom', PAGES)
def test_retour_ou_logo(nom, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    retour = attendu(nom)[2]
    assert page.locator('.app-retour').is_visible() == (retour is not None)
    assert page.locator('.site-header .brand').is_visible() == (retour is None)


@pytest.mark.parametrize('largeur', LARGEURS)
@pytest.mark.parametrize('nom', PAGES)
def test_pas_de_defilement_horizontal(nom, largeur, navigateur, base_url):
    ctx = navigateur.new_context(viewport={'width': largeur, 'height': 800})
    try:
        page, _ = ouvrir(ctx, base_url, nom)
        assert page.evaluate('document.documentElement.scrollWidth') <= largeur
    finally:
        ctx.close()


@pytest.mark.parametrize('nom', PAGES)
def test_la_barre_ne_cache_pas_le_bas_de_page(nom, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    # « instant » : le site défile en douceur (scroll-behavior), le test n'attend pas.
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_timeout(100)
    # Le pied de page, ou le contenu principal sur la page 404 qui n'en a pas.
    bas = page.evaluate("(document.querySelector('.site-footer') || document.querySelector('main'))"
                        ".getBoundingClientRect().bottom")
    barre = page.evaluate("document.querySelector('.onglets').getBoundingClientRect().top")
    assert bas <= barre + 1


@pytest.mark.parametrize('nom', ['index.html', 'calculateur-marge.html',
                                 'conseils-facture-impayee.html', 'contact.html'])
def test_zones_a_toucher(nom, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    for sel in ('.onglet', '.app-retour', '#navToggle'):
        for largeur, hauteur in page.evaluate(BOITES, sel):
            assert largeur >= 48 and hauteur >= 48, (sel, largeur, hauteur)


@pytest.mark.parametrize('schema', ['light', 'dark'])
@pytest.mark.parametrize('nom', ['index.html', 'calculateur-marge.html',
                                 'facturation-electronique.html', 'conseils-facture-impayee.html',
                                 'contact.html'])
def test_contrastes_de_la_navigation(nom, schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, _ = ouvrir(ctx, base_url, nom)
        for sel in ('.onglet-libelle', '.app-retour span'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
    finally:
        ctx.close()
