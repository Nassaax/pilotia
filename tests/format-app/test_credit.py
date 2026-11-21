# -*- coding: utf-8 -*-
"""Collaboration avec Nayas Visuals : chaque mention porte son logo et son lien."""
import pathlib
import re

import pytest

from aide import pages_du_site, source

INSTAGRAM = 'https://www.instagram.com/nayas.visuals/'
RACINE = pathlib.Path(__file__).resolve().parents[2]


@pytest.mark.parametrize('nom', [n for n in pages_du_site() if 'class="site-footer"' in source(n)])
def test_collaboration_en_pied_de_page(nom):
    html = source(nom)
    pied = html[html.index('class="site-footer"'):html.index('</footer>')]
    assert pied.count('class="credit-site"') == 1
    assert 'Création digitale en collaboration avec <a href="' + INSTAGRAM + '"' in pied
    assert 'img/nayas-visuals-logo.svg' in pied and 'img/nayas-visuals-logo-fonce.svg' in pied


@pytest.mark.parametrize('nom', pages_du_site())
def test_chaque_mention_a_son_logo_ou_son_lien(nom):
    # Chaque section (ou pied de page) qui nomme Nayas Visuals montre aussi son
    # logo ou un lien vers son compte, au plus près de la mention.
    html = re.sub(r'<head>.*?</head>', '', source(nom), flags=re.S)
    html = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    blocs = re.findall(r'<(?:section|footer|header)\b.*?</(?:section|footer|header)>', html, flags=re.S)
    for bloc in blocs:
        if 'Nayas Visuals' not in re.sub(r'<[^>]+>', ' ', bloc):
            continue
        assert INSTAGRAM in bloc or 'nayas-visuals-logo' in bloc, bloc[:200]
    # Toute mention hors de ces blocs serait une mention orpheline.
    reste = re.sub(r'<(section|footer|header)\b.*?</\1>', '', html, flags=re.S)
    assert 'Nayas Visuals' not in re.sub(r'<[^>]+>', ' ', reste)


def test_l_orange_reste_dans_le_logo():
    # La couleur de Nayas Visuals ne s'invite pas dans la charte du site.
    for f in ['style.css'] + [n for n in pages_du_site()]:
        assert '#FF5B2E' not in (RACINE / f).read_text().upper(), f
    for logo in ('img/nayas-visuals-logo.svg', 'img/nayas-visuals-logo-fonce.svg'):
        assert (RACINE / logo).stat().st_size < 20000
