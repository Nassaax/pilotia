# -*- coding: utf-8 -*-
"""Site installable (manifest et service worker) et fichiers de travail non
publiés, sur le modèle de LALLAT."""
import json
import re

import pytest
from playwright.sync_api import expect

from aide import RACINE, ouvrir, pages_du_site, source


def test_le_manifest_est_complet_et_ses_icones_existent():
    m = json.loads(source('manifest.webmanifest'))
    assert m['short_name'] == 'Pilotia' and m['display'] == 'standalone' and m['lang'] == 'fr-BE'
    for icone in m['icons']:
        assert (RACINE / icone['src'].lstrip('/')).exists(), icone['src']
    assert {i['sizes'] for i in m['icons']} == {'192x192', '512x512'}
    for raccourci in m['shortcuts']:
        assert (RACINE / raccourci['url'].lstrip('/')).exists(), raccourci['url']


@pytest.mark.parametrize('nom', pages_du_site())
def test_chaque_page_annonce_le_manifest(nom):
    assert '<link rel="manifest" href="manifest.webmanifest">' in source(nom)


def test_le_service_worker_ne_garde_que_des_fichiers_qui_existent():
    sw = source('sw.js')
    coquille = re.search(r'COQUILLE = \[(.*?)\];', sw, re.S).group(1)
    for chemin in re.findall(r"'(/[^']+)'", coquille):
        assert (RACINE / chemin.lstrip('/')).exists(), chemin
    assert "url.pathname.startsWith('/api/')" in sw  # les fonctions ne sont jamais mises en cache


def test_le_service_worker_ne_s_inscrit_qu_en_https(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    page.wait_for_timeout(300)
    assert page.evaluate('navigator.serviceWorker.getRegistrations().then(r => r.length)') == 0
    assert erreurs == []


def test_la_page_hors_connexion(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'offline.html')
    expect(page.locator('h1')).to_have_text('Pas de réseau pour le moment.')
    expect(page.get_by_role('link', name='Réessayer →')).to_have_attribute('href', '')
    assert '<meta name="robots" content="noindex,follow">' in source('offline.html')
    assert 'offline.html' not in source('sitemap.xml')
    assert erreurs == []


def test_les_fichiers_de_travail_ne_sont_pas_publies():
    regles = source('.vercelignore').split()
    for regle in ('tests', 'scripts', 'README.md', 'brand/*', '!brand/avatar-pilotia.svg'):
        assert regle in regles, regle
    v = json.loads(source('vercel.json'))
    assert v['regions'] == ['fra1']
    assert {r['source'] for r in v['redirects']} == {'/package.json', '/package-lock.json'}
    # L'avatar est le seul fichier de brand/ dont le site a besoin.
    utilises = set()
    for nom in pages_du_site():
        utilises |= set(re.findall(r'(?:src|href)="(brand/[^"]+)"', source(nom)))
    assert utilises == {'brand/avatar-pilotia.svg'}
