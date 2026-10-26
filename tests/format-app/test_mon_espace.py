# -*- coding: utf-8 -*-
"""Mon espace : ce que les outils ont enregistré sur cet appareil (§ 4.2)."""
import pytest
from playwright.sync_api import expect

from aide import TELEPHONE, ouvrir, source
from test_coquille import CONTRASTE

DIAG = {'total': 11, 'pill': 'Des failles ciblées', 'date': '2026-10-08T10:00:00.000Z',
        'themes': {'Finances': 3, 'Personnel & organisation': 3,
                   'Présence digitale': 3, 'Trésorerie & résilience': 2}, 'reponses': []}
RESUME = {'montant': 1250, 'mois': 'mars', 'annee': 2027, 'maj': '2026-10-10T09:00:00.000Z'}


def espace(telephone, base_url, donnees=None):
    page, erreurs = ouvrir(telephone, base_url, 'mon-espace.html')
    for cle, valeur in (donnees or {}).items():
        page.evaluate('([c, v]) => localStorage.setItem(c, JSON.stringify(v))', [cle, valeur])
    if donnees:
        page.reload()
    return page, erreurs


def texte(page, sel):
    return ' '.join(page.locator(sel).inner_text().split())


def pas(page):
    return page.eval_on_selector_all('#prochain-pas a', 'els => els.map(a => a.getAttribute("href"))')


def test_premiere_visite(telephone, base_url):
    page, erreurs = espace(telephone, base_url)
    assert page.locator('#espace-vide').is_visible()
    assert not page.locator('#espace-resultats').is_visible()
    assert page.locator('.depart').count() == 3
    assert page.locator('.onglet[aria-current="page"] .onglet-libelle').inner_text() == 'Mon espace'
    assert erreurs == []


def test_avec_un_diagnostic(telephone, base_url):
    page, erreurs = espace(telephone, base_url, {'pilotia-diagnostic': DIAG})
    assert not page.locator('#espace-vide').is_visible()
    assert texte(page, '#diag-total') == '11'
    assert page.locator('#diag-libelle').text_content() == 'Des failles ciblées'  # affiché en capitales
    assert texte(page, '#diag-date') == 'Fait le 8 octobre'
    assert page.locator('#diag-themes li').count() == 4
    assert 'Trésorerie & résilience 2/4' in texte(page, '#diag-themes')
    assert not page.locator('#carte-tresorerie').is_visible()
    assert pas(page) == ['plan-tresorerie.html', 'contact.html']
    assert erreurs == []


def test_avec_un_diagnostic_et_un_plan(telephone, base_url):
    page, _ = espace(telephone, base_url, {'pilotia-diagnostic': DIAG,
                                           'pilotia-tresorerie-resume': RESUME})
    assert texte(page, '#carte-tresorerie .espace-kpi') == 'Point bas : 1 250 € fin mars 2027'
    assert texte(page, '#plan-date') == 'Mis à jour le 10 octobre'
    assert pas(page) == ['calculateur-delai-encaissement.html', 'contact.html']


def test_avec_un_plan_seulement(telephone, base_url):
    page, _ = espace(telephone, base_url, {'pilotia-tresorerie-resume': RESUME})
    assert not page.locator('#carte-diagnostic').is_visible()
    assert pas(page) == ['diagnostic.html', 'contact.html']


def test_ancien_diagnostic_sans_date(telephone, base_url):
    ancien = dict(DIAG)
    del ancien['date']
    page, _ = espace(telephone, base_url, {'pilotia-diagnostic': ancien})
    assert texte(page, '#diag-date') == ''


@pytest.mark.parametrize('themes,attendu', [
    ({'Finances': 2, 'Personnel & organisation': 2, 'Présence digitale': 2,
      'Trésorerie & résilience': 2}, 'Trésorerie & résilience'),
    ({'Finances': 1, 'Présence digitale': 1}, 'Finances'),
    ({'Personnel & organisation': 0, 'Finances': 3}, 'Personnel & organisation'),
    ({}, None),
])
def test_theme_le_plus_faible(themes, attendu, telephone, base_url):
    page, _ = espace(telephone, base_url)
    assert page.evaluate('t => window.PilotiaMonEspace.themeLePlusFaible(t)', themes) == attendu


def test_effacer(telephone, base_url):
    page, _ = espace(telephone, base_url, {'pilotia-diagnostic': DIAG,
                                           'pilotia-tresorerie-resume': RESUME,
                                           'pilotia-tresorerie': {'version': 3}})
    page.once('dialog', lambda d: d.accept())
    page.click('#espace-effacer')
    assert page.evaluate("['pilotia-diagnostic', 'pilotia-tresorerie', 'pilotia-tresorerie-resume']"
                         ".every(c => localStorage.getItem(c) === null)")
    assert page.locator('#espace-vide').is_visible()
    expect(page.locator('#espace-titre')).to_be_focused()


def test_mon_espace_reference():
    assert 'https://www.pilotia.be/mon-espace.html' in source('sitemap.xml')
    assert 'https://www.pilotia.be/mon-espace.html' in source('llms.txt')


@pytest.mark.parametrize('schema', ['light', 'dark'])
def test_contrastes_de_mon_espace(schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, _ = espace(ctx, base_url, {'pilotia-diagnostic': DIAG, 'pilotia-tresorerie-resume': RESUME})
        for sel in ('.espace-actions .btn', '.lien-fleche', '.effacer', '.espace-date', '.pill',
                    '.ligne-titre', '.ligne-sous', '.espace-prive', '.theme-nom'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
    finally:
        ctx.close()
