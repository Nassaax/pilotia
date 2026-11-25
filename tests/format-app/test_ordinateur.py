# -*- coding: utf-8 -*-
"""Sur ordinateur (1 280 px), le rendu reste identique au pixel près à celui
du site de référence, sauf sur les pages où un changement est prévu (§ 5.3)."""
import pathlib
import shutil
import subprocess
import tempfile

import pytest
from PIL import Image, ImageChops

from aide import ORDINATEUR, RACINE, REFERENCE, pages_du_site, servir

# Le site de référence est l'écran d'ouverture (novembre 2026) : les changements
# prévus d'avant sont tous dedans. Ajouter ici une page dont le rendu doit changer.
CHANGEMENTS_PREVUS = {'contact.html', 'index.html', 'entreprises.html', 'cookies.html', 'mentions-legales.html',
                      'offres.html', 'marketing-digital.html',
                      # Planche « Pilotia améliorations » (novembre 2026) : diagnostic une
                      # question par écran, et témoignages d'exemple retirés des pages métier.
                      'diagnostic.html', 'coaching-agent-immobilier.html', 'coaching-boulangerie.html',
                      'coaching-coiffeur.html', 'coaching-esthetique.html', 'coaching-restaurant.html'}


@pytest.fixture(scope='module')
def reference_url():
    dossier = pathlib.Path(tempfile.mkdtemp(prefix='pilotia-reference-')) / 'site'
    subprocess.run(['git', 'worktree', 'add', '--detach', str(dossier), REFERENCE],
                   cwd=RACINE, check=True, capture_output=True)
    serveur = servir(dossier)
    yield f'http://127.0.0.1:{serveur.server_address[1]}'
    serveur.shutdown()
    subprocess.run(['git', 'worktree', 'remove', '--force', str(dossier)],
                   cwd=RACINE, check=True, capture_output=True)
    shutil.rmtree(dossier.parent, ignore_errors=True)


def capturer(navigateur, url, chemin):
    ctx = navigateur.new_context(**ORDINATEUR, reduced_motion='reduce')
    try:
        page = ctx.new_page()
        page.goto(url, wait_until='networkidle')
        page.evaluate('document.fonts.ready.then(() => true)')
        # Les commandes des lecteurs vidéo dessinent par moments une icône de
        # chargement : le site de référence ne serait même pas identique à
        # lui-même. Elles sont retirées des deux captures.
        page.evaluate("document.querySelectorAll('video').forEach(v => v.removeAttribute('controls'))")
        # Le bandeau de pré-lancement est temporaire et le même sur toutes les
        # pages : il est retiré de la capture, le reste doit rester identique.
        page.evaluate("document.querySelectorAll('.prelancement, .credit-site').forEach(e => e.remove())")
        # Le menu du haut a été simplifié sur toutes les pages (novembre 2026) : il
        # est masqué dans les deux captures (sa place reste), le reste doit rester identique.
        page.evaluate("document.querySelectorAll('.nav-links').forEach(e => e.style.visibility = 'hidden')")
        page.screenshot(path=str(chemin), full_page=True, animations='disabled')
    finally:
        ctx.close()


@pytest.mark.parametrize('nom', [n for n in pages_du_site() if n not in CHANGEMENTS_PREVUS])
def test_le_rendu_sur_ordinateur_ne_change_pas(nom, navigateur, base_url, reference_url, tmp_path):
    avant, apres = tmp_path / 'avant.png', tmp_path / 'apres.png'
    capturer(navigateur, f'{reference_url}/{nom}', avant)
    capturer(navigateur, f'{base_url}/{nom}', apres)
    a, b = Image.open(avant).convert('RGB'), Image.open(apres).convert('RGB')
    assert a.size == b.size, (a.size, b.size)
    assert ImageChops.difference(a, b).getbbox() is None, f'différences dans {ImageChops.difference(a, b).getbbox()}'
