# -*- coding: utf-8 -*-
"""Les six pages pilotes au format app (§ 5 de la conception)."""
import re

from playwright.sync_api import expect

from aide import ouvrir, source


def visible(page, sel):
    return page.evaluate(f"document.querySelector({sel!r}).checkVisibility()")


def test_mentions_legales(telephone, ordinateur, base_url):
    titres = len(re.findall(r'<h2 id="', source('mentions-legales.html')))
    page, erreurs = ouvrir(telephone, base_url, 'mentions-legales.html')
    assert page.locator('.repli-bouton').count() == titres == 10
    assert page.locator('.replis-tout').count() == 1
    assert visible(page, 'h1') and visible(page, '.note')
    assert not visible(page, '#hebergeur + .repli-corps p')
    page, _ = ouvrir(telephone, base_url, 'mentions-legales.html#hebergeur')
    assert visible(page, '#hebergeur + .repli-corps p')
    page, _ = ouvrir(ordinateur, base_url, 'mentions-legales.html')
    assert page.locator('.repli-bouton, .repli-groupe').count() == 0
    assert erreurs == []


def test_page_de_service_peppol(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'facturation-electronique.html')
    assert page.locator('.essentiel li').count() == 3
    # L'encadré vient juste avant les boutons du haut de page : « puis le bouton d'action ».
    assert page.evaluate("document.querySelector('.hero .essentiel').nextElementSibling.className") == 'btn-row'
    assert page.locator('.repli-bouton').count() == 4
    assert page.locator('.replis-tout').count() == 1
    assert visible(page, '.annonce') and visible(page, '.banner')
    assert not visible(page, '.faq details')
    page, _ = ouvrir(ordinateur, base_url, 'facturation-electronique.html')
    assert visible(page, '.essentiel') and visible(page, '.faq details')
    assert erreurs == []
