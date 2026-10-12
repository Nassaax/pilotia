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


@pytest.fixture(scope='session')
def navigateur():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
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
