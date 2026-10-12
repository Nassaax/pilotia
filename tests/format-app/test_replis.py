# -*- coding: utf-8 -*-
"""Sections repliables : fermées sur téléphone, ouvertes sans bouton sur ordinateur."""
from aide import ouvrir, source

URL = 'tests/format-app/essais/replis.html'
CORPS = ('p1', 'p2', 'p3', 'p4')
# Le <main> tel que l'ordinateur doit le voir : le HTML d'origine, intact.
MAIN = "document.querySelector('main').innerHTML"


def visible(page, id_):
    return page.evaluate(f"document.getElementById('{id_}').checkVisibility()")


def test_tout_est_replie_sur_telephone(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, URL)
    boutons = page.locator('h2 > button.repli-bouton')
    assert boutons.count() == 4
    assert [boutons.nth(i).get_attribute('aria-expanded') for i in range(4)] == ['false'] * 4
    assert not any(visible(page, p) for p in CORPS)
    assert visible(page, 'intro')
    assert not visible(page, 'e1')  # le sur-titre suit son corps
    assert erreurs == []


def test_ouvrir_puis_fermer(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    b = page.get_by_role('button', name='Première section')
    b.click()
    assert b.get_attribute('aria-expanded') == 'true' and visible(page, 'p1') and visible(page, 'e1')
    b.click()
    assert b.get_attribute('aria-expanded') == 'false' and not visible(page, 'p1')


def test_au_clavier(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    page.get_by_role('button', name='Troisième partie').focus()
    page.keyboard.press('Enter')
    assert visible(page, 'p3')


def test_tout_ouvrir(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    tout = page.locator('.replis-tout')
    assert tout.count() == 1 and tout.inner_text() == 'Tout ouvrir'
    tout.click()
    assert all(visible(page, p) for p in CORPS) and tout.inner_text() == 'Tout fermer'
    tout.click()
    assert not any(visible(page, p) for p in CORPS) and tout.inner_text() == 'Tout ouvrir'


def test_section_sombre_eclaircie_puis_rendue(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    assert 'section-sombre' not in page.get_attribute('#s2', 'class')
    page.set_viewport_size({'width': 1280, 'height': 900})
    page.wait_for_timeout(150)
    assert 'section-sombre' in page.get_attribute('#s2', 'class')


def test_un_lien_vers_une_ancre_ouvre_sa_section(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL + '#ancre')
    assert visible(page, 'ancre')
    assert page.get_by_role('button', name='Deuxième section').get_attribute('aria-expanded') == 'true'


def test_un_titre_cible_ouvre_sa_section(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL + '#t4')
    assert visible(page, 'p4')


def test_la_recherche_dans_la_page_peut_ouvrir(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    corps = page.locator('#p3').locator('xpath=..')
    assert 'repli-corps' in corps.get_attribute('class')
    assert corps.get_attribute('hidden') == 'until-found'


def test_impression(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    assert all(visible(page, p) for p in CORPS)
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert not visible(page, 'p1')


def test_sur_ordinateur_le_html_reste_celui_d_origine(ordinateur, base_url):
    page, _ = ouvrir(ordinateur, base_url, URL)
    assert page.locator('.repli-bouton, .replis-outils, .repli-corps, .repli-groupe').count() == 0
    assert all(visible(page, p) for p in CORPS)


def test_passages_d_une_largeur_a_l_autre(telephone, ordinateur, base_url):
    reference, _ = ouvrir(ordinateur, base_url, URL)
    page, _ = ouvrir(telephone, base_url, URL)
    page.set_viewport_size({'width': 1280, 'height': 900})
    page.wait_for_timeout(150)
    assert page.evaluate(MAIN) == reference.evaluate(MAIN)
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_timeout(150)
    assert page.locator('.repli-bouton').count() == 4
    assert not visible(page, 'p3')
