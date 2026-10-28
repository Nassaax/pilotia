# -*- coding: utf-8 -*-
"""Bandeau de pré-lancement : une seule annonce, avant l'en-tête, sur toutes
les pages, lisible en clair comme en sombre. À supprimer avec le bandeau à
l'ouverture, en janvier 2027."""
import pytest

from aide import TELEPHONE, ouvrir, pages_du_site, source
from test_coquille import CONTRASTE

PAGES = pages_du_site()


@pytest.mark.parametrize('nom', PAGES)
def test_un_bandeau_avant_l_en_tete(nom):
    html = source(nom)
    assert html.count('<aside class="prelancement"') == 1
    assert html.index('<aside class="prelancement"') < html.index('<header class="site-header')
    bandeau = html[html.index('<!-- prelancement'):html.index('<!-- /prelancement -->')]
    assert 'janvier 2027' in bandeau
    assert 'href="contact.html"' in bandeau
    assert '—' not in bandeau


def test_les_offres_rappellent_la_date():
    assert 'Prestations payantes disponibles à partir de janvier 2027.' in source('offres.html')


@pytest.mark.parametrize('schema', ['light', 'dark'])
@pytest.mark.parametrize('nom', ['index.html', 'offres.html', 'contact.html'])
def test_le_bandeau_est_lisible(nom, schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, erreurs = ouvrir(ctx, base_url, nom)
        assert page.locator('.prelancement').is_visible()
        for sel in ('.prelancement p', '.prelancement a', '.prelancement-note'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
        assert not erreurs, erreurs
    finally:
        ctx.close()
