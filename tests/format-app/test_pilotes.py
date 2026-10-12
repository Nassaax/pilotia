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
