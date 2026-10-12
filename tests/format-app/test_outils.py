# -*- coding: utf-8 -*-
"""Onglet Outils : sous-onglets et listes à toucher (§ 4.3 de la conception)."""
import pytest

from aide import ouvrir
from test_coquille import BOITES


@pytest.mark.parametrize('nom', ['outils.html', 'conseils.html', 'ressources.html'])
def test_sous_onglets_en_mode_app_seulement(nom, telephone, ordinateur, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    assert page.locator('.segment').is_visible()
    for largeur, hauteur in page.evaluate(BOITES, '.segment a'):
        assert hauteur >= 48 and largeur >= 48
    page, _ = ouvrir(ordinateur, base_url, nom)
    assert not page.locator('.segment').is_visible()


@pytest.mark.parametrize('nom,liens,documents', [('outils.html', 8, 1), ('conseils.html', 7, 0),
                                                 ('ressources.html', 0, 8)])
def test_cartes_en_lignes(nom, liens, documents, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    lignes = page.locator('.grille-liste > a.card')
    assert lignes.count() == liens
    for i in range(liens):
        assert page.evaluate('e => getComputedStyle(e).display', lignes.nth(i).element_handle()) == 'grid'
        assert lignes.nth(i).bounding_box()['height'] >= 56
    if liens:
        serre = page.evaluate("getComputedStyle(document.querySelector('.grille-liste > a.card > p')).webkitLineClamp")
        assert serre == '2'
    assert page.locator('.grille-liste > div.card').count() == documents
