# -*- coding: utf-8 -*-
"""Tuiles à icône, menu « Découvrir », anneaux et cartes photo."""
from PIL import Image

from aide import RACINE, ouvrir

PROFILS = ['Une entreprise déjà en activité', 'Un futur indépendant', 'Un particulier',
           'Un porteur de projet', 'Autre']


def test_contact_profil_en_tuiles(ordinateur, base_url):
    page, erreurs = ouvrir(ordinateur, base_url, 'contact.html')
    valeurs = page.eval_on_selector_all('.choix-type input[type="radio"][name="profil"]', 'els => els.map(e => e.value)')
    assert valeurs == PROFILS
    page.locator('.choix-tuile', has_text='Un particulier').click()
    assert page.evaluate("document.querySelector('input[name=profil]:checked').value") == 'Un particulier'
    assert erreurs == []


def test_diagnostic_avance_seul_et_une_seule_fois(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'diagnostic.html')
    page.locator('#question-block .choix-tuile').first.click()
    page.wait_for_timeout(600)
    assert 'Question 2 / 8' in page.text_content('#progress')
    page.locator('#question-block .choix-tuile').nth(1).click()
    page.click('#btnNext')        # avant la fin du délai : on n'avance qu'une fois
    page.wait_for_timeout(600)
    assert 'Question 3 / 8' in page.text_content('#progress')
    assert erreurs == []


def test_menu_decouvrir_survol_et_echap(ordinateur, base_url):
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
