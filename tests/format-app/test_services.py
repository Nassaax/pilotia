# -*- coding: utf-8 -*-
"""Écran Services (§ 4.1 de la conception)."""
import re

import pytest

from aide import RACINE, TELEPHONE, ouvrir, source
from test_coquille import BOITES, CONTRASTE

LIENS = ['entreprises.html', 'independants.html', 'facturation-electronique.html',
         'affacturage.html', 'marketing-digital.html', 'offres.html',
         'coaching-restaurant.html', 'coaching-boulangerie.html', 'coaching-coiffeur.html',
         'coaching-esthetique.html', 'coaching-agent-immobilier.html', 'diagnostic.html']


def test_les_liens_de_services():
    principal = re.search(r'<main id="contenu">(.*?)</main>', source('services.html'), re.S).group(1)
    liens = re.findall(r'href="([^"]+)"', principal)
    assert liens == LIENS
    assert all((RACINE / l).exists() for l in liens)


def test_services_reference():
    html = source('services.html')
    assert '<link rel="canonical" href="https://pilotis-murex.vercel.app/services.html">' in html
    assert '<meta property="og:url" content="https://pilotis-murex.vercel.app/services.html">' in html
    assert 'https://pilotis-murex.vercel.app/services.html' in source('sitemap.xml')
    assert 'https://pilotis-murex.vercel.app/services.html' in source('llms.txt')


def test_services_sur_telephone(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'services.html')
    assert page.locator('.onglet[aria-current="page"] .onglet-libelle').inner_text() == 'Services'
    for sel in ('.tuile', '.ligne-app', '.puces a', '.carte-pas-sur .btn'):
        for largeur, hauteur in page.evaluate(BOITES, sel):
            assert largeur >= 48 and hauteur >= 48, (sel, largeur, hauteur)
    assert erreurs == []


def test_services_en_grille_sur_ordinateur(ordinateur, base_url):
    page, _ = ouvrir(ordinateur, base_url, 'services.html')
    colonnes = page.evaluate("getComputedStyle(document.querySelector('.liste-app')).gridTemplateColumns")
    assert len(colonnes.split()) == 2


@pytest.mark.parametrize('schema', ['light', 'dark'])
def test_contrastes_de_services(schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, _ = ouvrir(ctx, base_url, 'services.html')
        for sel in ('.titre-groupe', '.tuile-titre', '.tuile-texte', '.ligne-titre', '.ligne-sous',
                    '.puces a', '.carte-pas-sur p', '.carte-pas-sur .btn'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
    finally:
        ctx.close()
