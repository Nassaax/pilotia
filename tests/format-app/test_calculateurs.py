# -*- coding: utf-8 -*-
"""Les pourcentages calculés s'écrivent avec une virgule décimale, comme le
reste du site : « 75,0 % », jamais « 75.0 % »."""
from playwright.sync_api import expect

from aide import ouvrir


def test_marge_le_taux_s_ecrit_avec_une_virgule(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'calculateur-marge.html')
    page.fill('#prixVente', '20')
    page.fill('#coutRevient', '5')
    page.get_by_role('button', name='Calculer la marge →').click()
    expect(page.locator('#margePct')).to_have_text('Soit un taux de marge de 75,0 % du prix de vente.')
    assert erreurs == []


def test_taux_horaire_une_occupation_a_virgule_reste_a_virgule(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'calculateur-taux-horaire.html')
    page.fill('#occupation', '72.5')  # ce que rend le champ quand on y tape 72,5
    expect(page.locator('#outFactures')).to_contain_text('(72,5 % de ')
    assert erreurs == []
