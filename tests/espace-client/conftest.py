# -*- coding: utf-8 -*-
"""Fixtures des tests de l'espace client.

Lancer : python3 -m pytest tests/espace-client -q
Prérequis une fois par copie : (cd tests/espace-client && npm ci)"""
import pytest
from playwright.sync_api import sync_playwright

from aide_espace import CHROME, ORDINATEUR, TELEPHONE, Client, Serveur


@pytest.fixture(scope='session')
def serveur():
    s = Serveur()
    yield s
    s.arreter()


@pytest.fixture(autouse=True)
def propre(serveur):
    """Chaque test part d'une base vide, espace ouvert, Brevo en état de marche."""
    serveur.vider()
    serveur.env(ESPACE_CLIENT='ouvert', TEST_BREVO_ECHEC=None)
    yield


@pytest.fixture
def client(serveur):
    return Client(serveur)


@pytest.fixture(scope='session')
def navigateur():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        yield b
        b.close()


@pytest.fixture
def telephone(navigateur, serveur):
    ctx = navigateur.new_context(**TELEPHONE, base_url=serveur.url)
    yield ctx
    ctx.close()


@pytest.fixture
def ordinateur(navigateur, serveur):
    ctx = navigateur.new_context(**ORDINATEUR, base_url=serveur.url)
    yield ctx
    ctx.close()
