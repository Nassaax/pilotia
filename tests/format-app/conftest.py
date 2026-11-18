# -*- coding: utf-8 -*-
"""Fixtures des tests du format app.

Lancer : python3 -m pytest tests/format-app -q   (prérequis : pip install pytest)
Chromium est celui préinstallé : pas de « playwright install »."""
import pytest
from playwright.sync_api import sync_playwright

from aide import CHROME, ORDINATEUR, RACINE, TELEPHONE, servir


@pytest.fixture(scope='session')
def base_url():
    serveur = servir(RACINE)
    yield f'http://127.0.0.1:{serveur.server_address[1]}'
    serveur.shutdown()


# L'écran d'ouverture couvre la page ~3 s et intercepte les clics : chaque
# contexte des tests le marque comme déjà vu. Les tests de l'écran lui-même
# passent par navigateur.contexte_brut, qui ne pré-remplit rien.
SAUTER_INTRO = "try { sessionStorage.setItem('pilotia-intro', 'vue'); } catch (e) {}"


@pytest.fixture(scope='session')
def navigateur():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        brut = b.new_context

        def new_context(**options):
            ctx = brut(**options)
            ctx.add_init_script(SAUTER_INTRO)
            return ctx
        b.contexte_brut = brut
        b.new_context = new_context
        yield b
        b.close()


@pytest.fixture
def telephone(navigateur):
    ctx = navigateur.new_context(**TELEPHONE)
    yield ctx
    ctx.close()


@pytest.fixture
def ordinateur(navigateur):
    ctx = navigateur.new_context(**ORDINATEUR)
    yield ctx
    ctx.close()
