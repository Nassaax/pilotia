# -*- coding: utf-8 -*-
from aide import attendu, ouvrir, pages_du_site


def test_le_serveur_sert_le_site(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    assert page.title().startswith('Pilotia')
    assert erreurs == []


def test_chaque_page_est_classee_dans_la_conception():
    for nom in pages_du_site():
        attendu(nom)  # KeyError si une page manque au tableau du § 3.2
