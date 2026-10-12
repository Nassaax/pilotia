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


def test_article_facture_impayee(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'conseils-facture-impayee.html')
    assert page.locator('.essentiel li').count() == 3
    assert page.locator('.repli-bouton').count() == 7  # 6 parties et la FAQ
    assert page.locator('.replis-tout').count() == 1
    assert page.locator('.app-retour span').inner_text() == 'Conseils'
    page.locator('.replis-tout').click()
    assert visible(page, 'table') and visible(page, '.faq details')
    page, _ = ouvrir(ordinateur, base_url, 'conseils-facture-impayee.html')
    assert page.locator('.repli-bouton').count() == 0 and visible(page, '.essentiel')
    assert erreurs == []


def test_calculateur_de_marge(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'calculateur-marge.html')
    modes = page.eval_on_selector_all('input[type="number"]', 'els => els.map(e => e.inputMode)')
    assert modes == ['decimal'] * 4
    assert page.evaluate("getComputedStyle(document.getElementById('prixVente')).fontSize") == '16px'
    assert page.locator('.repli-bouton').count() == 1  # l'étape 2 est repliée
    assert not visible(page, '#fraisFixes')
    page.fill('#prixVente', '20')
    page.fill('#coutRevient', '5')
    page.get_by_role('button', name='Calculer la marge →').click()
    expect(page.locator('#margeEuro')).to_have_text('15,00 € de marge')
    assert page.get_attribute('#resultatMarge', 'aria-live') == 'polite'
    # L'écran est descendu jusqu'au résultat, au-dessus de la barre d'onglets.
    page.wait_for_function("""() => document.getElementById('resultatMarge').getBoundingClientRect().bottom
        <= document.querySelector('.onglets').getBoundingClientRect().top""", timeout=3000)
    assert erreurs == []


def test_rendez_vous(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'contact.html')
    carte = page.locator('.rdv-carte')
    assert carte.is_visible()
    lien = carte.locator('a.btn')
    assert lien.get_attribute('href') == 'https://cal.com/pilotia/call'
    assert lien.get_attribute('target') == '_blank'
    assert page.locator('.duree').inner_text() == '15 min · gratuit'
    assert page.locator('.onglet-centre').get_attribute('aria-current') == 'page'
    assert not visible(page, '#contact-form')
    page.get_by_role('button', name='Ou laissez-nous un message').click()
    assert visible(page, '#contact-form')
    remplissage = page.eval_on_selector_all('#nom, #entreprise, #email', 'els => els.map(e => e.autocomplete)')
    assert remplissage == ['name', 'organization', 'email']
    page, _ = ouvrir(ordinateur, base_url, 'contact.html')
    assert visible(page, '#contact-form') and not page.locator('.duree').is_visible()
    assert erreurs == []


def test_accueil(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    acces = page.eval_on_selector_all('.acces-rapide a', 'els => els.map(a => a.getAttribute("href"))')
    assert acces == ['diagnostic.html', 'plan-tresorerie.html',
                     'facturation-electronique.html', 'independants.html']
    assert page.locator('.acces-rapide').is_visible()
    assert not page.locator('.hero-accueil .btn-row').is_visible()
    for sel in ('.triangle-grid', '.path-cards', '.avis'):
        defile = page.evaluate("""s => { const e = document.querySelector(s);
            return getComputedStyle(e).overflowX === 'auto' && e.scrollWidth > e.clientWidth; }""", sel)
        assert defile, sel  # cartes à faire glisser
    page, _ = ouvrir(ordinateur, base_url, 'index.html')
    assert not page.locator('.acces-rapide').is_visible()
    assert page.locator('.hero-accueil .btn-row').is_visible()
    assert erreurs == []
