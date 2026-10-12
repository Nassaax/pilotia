# -*- coding: utf-8 -*-
"""Les trois clés du stockage local sont déclarées (conception, § 6)."""
import pytest

from aide import source


@pytest.mark.parametrize('nom', ['cookies.html', 'confidentialite.html'])
def test_les_trois_cles_sont_declarees(nom):
    html = source(nom)
    for cle in ('pilotia-diagnostic', 'pilotia-tresorerie', 'pilotia-tresorerie-resume'):
        assert f'<td><code>{cle}</code></td>' in html, cle
    assert 'href="mon-espace.html"' in html
    assert 'Dernière mise à jour : 20 septembre 2026' not in html
