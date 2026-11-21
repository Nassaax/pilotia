# -*- coding: utf-8 -*-
"""Le crédit de réalisation du site figure en bas de chaque page."""
import pathlib

import pytest

from aide import pages_du_site, source


@pytest.mark.parametrize('nom', [n for n in pages_du_site() if 'class="site-footer"' in source(n)])
def test_credit_en_pied_de_page(nom):
    html = source(nom)
    pied = html[html.index('class="site-footer"'):html.index('</footer>')]
    assert pied.count('class="credit-site"') == 1
    assert 'Site réalisé par <img src="nayas-visuals.png" alt=""' in pied
    assert '<span>Nayas Visuals</span>' in pied


def test_logo_du_credit_present():
    racine = pathlib.Path(__file__).resolve().parents[2]
    assert (racine / 'nayas-visuals.png').stat().st_size < 20000
