# -*- coding: utf-8 -*-
"""Menu « Services » à icônes, anneaux et cartes photo."""
from PIL import Image

from aide import RACINE, ouvrir

def test_menu_services_survol_et_echap(ordinateur, base_url):
    page, erreurs = ouvrir(ordinateur, base_url, 'index.html')
    bouton = page.locator('.dropdown-trigger')
    page.hover('.dropdown-trigger')
    page.wait_for_timeout(350)
    assert bouton.get_attribute('aria-expanded') == 'true'
    assert page.locator('.dropdown-tout a').is_visible()
    page.keyboard.press('Escape')
    assert bouton.get_attribute('aria-expanded') == 'false'
    assert erreurs == []


def test_anneaux_se_dessinent_a_l_ecran(ordinateur, base_url):
    page, erreurs = ouvrir(ordinateur, base_url, 'marketing-digital.html')
    schema = page.locator('[data-anneaux]')
    assert not schema.evaluate("e => e.classList.contains('vu')")
    schema.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    assert schema.evaluate("e => e.classList.contains('vu')")
    assert erreurs == []


def test_cartes_photo_metiers(ordinateur, base_url):
    page, erreurs = ouvrir(ordinateur, base_url, 'entreprises.html')
    liens = page.eval_on_selector_all('.cartes-photo .carte-photo', 'els => els.map(a => a.getAttribute("href"))')
    assert liens == ['coaching-restaurant.html', 'coaching-boulangerie.html', 'coaching-coiffeur.html',
                     'coaching-esthetique.html', 'coaching-agent-immobilier.html']
    for src, alt in page.eval_on_selector_all('.carte-photo img', 'els => els.map(i => [i.getAttribute("src"), i.alt])'):
        assert alt
        with Image.open(RACINE / src) as im:
            assert im.size == (640, 800) and im.format == 'WEBP'
    assert erreurs == []
