# -*- coding: utf-8 -*-
"""Ce que le diagnostic et le plan de trésorerie laissent pour Mon espace (§ 4.2)."""
from aide import ouvrir

RESUME = "JSON.parse(localStorage.getItem('pilotia-tresorerie-resume'))"


def test_le_diagnostic_enregistre_sa_date(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'diagnostic.html')
    for _ in range(8):
        page.check('input[name="opt"][value="0"]')
        page.click('#btnNext')
    d = page.evaluate("JSON.parse(localStorage.getItem('pilotia-diagnostic'))")
    assert d['total'] == 16
    assert page.evaluate('d => !isNaN(Date.parse(d))', d['date'])


def test_le_plan_d_exemple_ne_cree_pas_de_resume(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'plan-tresorerie.html')
    assert page.evaluate("localStorage.getItem('pilotia-tresorerie-resume')") is None


def test_modifier_le_plan_cree_le_resume(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'plan-tresorerie.html')
    page.fill('#p-solde', '2000')
    r = page.evaluate(RESUME)
    assert isinstance(r['montant'], int) and r['mois'] and r['annee'] and r['maj']
    page.evaluate("localStorage.removeItem('pilotia-tresorerie-resume')")
    page.reload()
    assert page.evaluate(RESUME) is not None  # le plan reste « modifié » après rechargement


def test_effacer_le_plan_efface_le_resume(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'plan-tresorerie.html')
    page.fill('#p-solde', '2000')
    page.once('dialog', lambda d: d.accept())
    page.click('#treso-reset')
    assert page.evaluate("localStorage.getItem('pilotia-tresorerie-resume')") is None
