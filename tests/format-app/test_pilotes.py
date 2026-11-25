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
    # Rendez-vous en trois gestes (profil, sujet, moment) : le message WhatsApp
    # se remplit, et ne part qu'avec le consentement coché. Le formulaire par
    # email reste en secours, replié sur téléphone, ouvert d'un geste.
    page, erreurs = ouvrir(telephone, base_url, 'contact.html')
    assert page.locator('.onglet-centre').get_attribute('aria-current') == 'page'
    lien = page.locator('a[href*="wa.me"]')
    assert lien.count() == 1
    assert page.locator('#rdv-compteur').inner_text() == 'Étape 1 sur 3'
    assert not lien.is_visible()
    page.click('#rdv-suite')  # rien de choisi : on reste à l'étape 1
    assert page.locator('#rdv-alerte').inner_text() != ''
    page.check('input[name="rdv-profil"][value="Un futur indépendant"]')
    page.click('#rdv-suite')
    page.check('input[name="rdv-sujet"][value="Facture Peppol"]')
    page.click('#rdv-suite')
    page.check('input[name="rdv-moment"][value="le matin"]')
    assert lien.is_visible()
    href = lien.get_attribute('href')
    # Numéro belge au format international sans le +, message déjà rédigé.
    assert re.fullmatch(r'https://wa\.me/32\d{8,9}\?text=Bonjour.+', href)
    texte = page.evaluate('h => decodeURIComponent(h.split("text=")[1])', href)
    assert 'un futur indépendant' in texte and 'facture peppol' in texte and 'le matin' in texte
    # Sans consentement, le lien ne s'ouvre pas.
    lien.click()
    assert len(telephone.pages) == 1
    assert 'consentement' in page.locator('#rdv-alerte').inner_text()
    remplissage = page.eval_on_selector_all('#nom, #entreprise, #email', 'els => els.map(e => e.autocomplete)')
    assert remplissage == ['name', 'organization', 'email']
    page.locator('.repli-bouton').first.click()
    assert visible(page, '#contact-form')
    page, _ = ouvrir(ordinateur, base_url, 'contact.html')
    assert visible(page, '#contact-form')
    assert erreurs == []


def test_accueil(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    acces = page.eval_on_selector_all('.acces-rapide a', 'els => els.map(a => a.getAttribute("href"))')
    assert acces == ['diagnostic.html', 'plan-tresorerie.html',
                     'facturation-electronique.html', 'independants.html']
    assert page.locator('.acces-rapide').is_visible()
    assert page.locator('.appel-rapide').is_visible()
    assert not page.locator('.hero-accueil .btn-row').is_visible()
    assert not page.locator('.apercu-diag').is_visible()
    defile = page.evaluate("""() => { const e = document.querySelector('.path-cards');
        return getComputedStyle(e).overflowX === 'auto' && e.scrollWidth > e.clientWidth; }""")
    assert defile  # parcours en cartes à faire glisser
    # Aucun avis client : rien n'est inventé avant l'ouverture.
    assert page.locator('.avis, blockquote').count() == 0
    page, _ = ouvrir(ordinateur, base_url, 'index.html')
    assert not page.locator('.acces-rapide').is_visible()
    assert not page.locator('.appel-rapide').is_visible()
    assert page.locator('.hero-accueil .btn-row').is_visible()
    assert page.locator('.apercu-diag').is_visible()
    outils = page.eval_on_selector_all('.outils-grille a', 'els => els.map(a => a.getAttribute("href"))')
    assert len(outils) == 6 and all(page.evaluate('h => fetch(h).then(r => r.ok)', h) for h in outils)
    # Une réponse de l'aperçu ouvre le diagnostic à la deuxième question.
    page.click('.apercu-reponses a >> nth=1')
    page.wait_for_url('**/diagnostic.html?reponse=1')
    assert page.locator('#progress').inner_text() == 'Question 2 sur 8'
    assert erreurs == []


METIERS = ['coaching-restaurant.html', 'coaching-boulangerie.html', 'coaching-coiffeur.html',
           'coaching-esthetique.html', 'coaching-agent-immobilier.html']


def test_cas_types_des_pages_metier(telephone, base_url):
    # Pas d'avis client inventé : un cas type, présenté comme un exemple.
    for nom in METIERS:
        page, erreurs = ouvrir(telephone, base_url, nom)
        assert page.locator('.avis, blockquote').count() == 0, nom
        assert page.locator('.section-cas-type .cas-type-etape').count() == 3, nom
        note = page.text_content('.cas-type-note')
        assert "Ce n'est pas le témoignage d'un client." in note, nom
        assert page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth') == 0
        assert erreurs == [], nom
