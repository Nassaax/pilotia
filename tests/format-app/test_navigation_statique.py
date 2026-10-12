# -*- coding: utf-8 -*-
"""Le HTML de chaque page porte la navigation du format app (§ 3 de la conception)."""
import re
import subprocess

import pytest

from aide import ONGLETS, RACINE, attendu, pages_du_site, source

PAGES = pages_du_site()


def _liens_de_la_barre(html):
    nav = re.search(r'<nav class="onglets" aria-label="Navigation principale">(.*?)</nav>',
                    html, re.S)
    assert nav, "barre d'onglets absente"
    return re.findall(r'<a href="([^"]+)" class="(onglet[^"]*)"(?: aria-current="(page|true)")?>',
                      nav.group(1))


@pytest.mark.parametrize('nom', PAGES)
def test_barre_d_onglets(nom):
    liens = _liens_de_la_barre(source(nom))
    assert [h for h, _, _ in liens] == ONGLETS
    assert liens[2][1] == 'onglet onglet-centre'
    actif, valeur, _ = attendu(nom)
    actifs = [(h, v) for h, _, v in liens if v]
    assert actifs == ([] if actif is None else [(actif, valeur)])


@pytest.mark.parametrize('nom', PAGES)
def test_lien_retour_et_en_tete(nom):
    html = source(nom)
    _, _, retour = attendu(nom)
    bloc = re.search(r'<!-- app:retour -->(.*?)<!-- /app:retour -->', html, re.S)
    assert bloc, 'marqueurs du lien retour absents'
    if retour is None:
        assert bloc.group(1) == ''
        assert '<header class="site-header">' in html
    else:
        href, libelle = retour
        assert (f'<a class="app-retour" href="{href}" aria-label="Revenir à la page {libelle}">'
                in bloc.group(1))
        assert f'<span>{libelle}</span>' in bloc.group(1)
        assert '<header class="site-header a-retour">' in html


@pytest.mark.parametrize('nom', PAGES)
def test_panneau_plus_et_scripts(nom):
    html = source(nom)
    assert 'viewport-fit=cover' in html
    assert 'aria-controls="panneauPlus" aria-haspopup="dialog"' in html
    panneau = re.search(r'<dialog class="plus" id="panneauPlus" aria-labelledby="plusTitre">'
                        r'(.*?)</dialog>', html, re.S)
    assert panneau, 'panneau « Plus » absent'
    assert re.findall(r'<a href="([^"]+)"', panneau.group(1)) == [
        'a-propos.html', 'methode.html', 'statistiques.html', 'parrainage.html',
        'https://www.instagram.com/pilotia.be/', 'mentions-legales.html',
        'confidentialite.html', 'cookies.html', 'cgv.html', 'accessibilite.html']
    assert html.count('<script src="app.js" defer></script>') == 1
    assert (html.index('<script src="animations.js" defer></script>')
            < html.index('<script src="app.js" defer></script>'))


@pytest.mark.parametrize('nom', PAGES)
def test_menu_ordinateur_complete(nom):
    menu = re.search(r'<ul class="dropdown-menu">(.*?)</ul>', source(nom), re.S).group(1)
    liens = re.findall(r'<li><a href="([^"]+)"( class="active")?>([^<]+)</a></li>', menu)
    assert (liens[0][0], liens[0][2]) == ('services.html', 'Tous les services')
    assert (liens[-1][0], liens[-1][2]) == ('mon-espace.html', 'Mon espace')
    assert [h for h, _, _ in liens].count('services.html') == 1
    assert [h for h, _, _ in liens].count('mon-espace.html') == 1
    for href, actif, _ in (liens[0], liens[-1]):
        assert bool(actif) == (href == nom)


@pytest.mark.parametrize('nom', ['outils.html', 'conseils.html', 'ressources.html'])
def test_sous_onglets_outils(nom):
    seg = re.search(r'<nav class="segment" aria-label="Rubriques de l\'onglet Outils">(.*?)</nav>',
                    source(nom), re.S)
    assert seg
    liens = re.findall(r'<a href="([^"]+)"( aria-current="page")?>([^<]+)</a>', seg.group(1))
    assert [(h, l) for h, _, l in liens] == [('outils.html', 'Outils'),
                                            ('conseils.html', 'Conseils'),
                                            ('ressources.html', 'Guides')]
    assert [h for h, c, _ in liens if c] == [nom]


def test_le_generateur_est_a_jour():
    r = subprocess.run(['python3', 'scripts/navigation-app.py', '--verifier'], cwd=RACINE,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize('nom', PAGES)
def test_liens_internes_valides(nom):
    for href in re.findall(r'href="([^"#?:]+\.html)(?:[#?][^"]*)?"', source(nom)):
        assert (RACINE / href).exists(), href
