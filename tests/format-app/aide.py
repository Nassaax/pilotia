# -*- coding: utf-8 -*-
"""Constantes et fonctions partagées par les tests du format app.

Le tableau attendu des onglets recopie le § 3.2 de
brand/format-app-CONCEPTION.md : il ne lit pas le générateur, pour que les
tests vérifient le générateur au lieu de le répéter."""
import functools
import http.server
import pathlib
import socketserver
import subprocess
import threading
from html.parser import HTMLParser

RACINE = pathlib.Path(__file__).resolve().parents[2]
CHROME = '/opt/pw-browsers/chromium'  # lien stable vers le Chromium installé
# Le site avant le format app : référence du texte et du rendu sur ordinateur.
REFERENCE = '3433103'

TELEPHONE = dict(viewport={'width': 390, 'height': 844}, device_scale_factor=2,
                 is_mobile=True, has_touch=True)
ORDINATEUR = dict(viewport={'width': 1280, 'height': 900})
LARGEURS = [360, 390, 768, 1280]

ONGLETS = ['index.html', 'services.html', 'contact.html', 'outils.html', 'mon-espace.html']
SERVICES = ['entreprises.html', 'independants.html', 'facturation-electronique.html',
            'affacturage.html', 'marketing-digital.html', 'offres.html',
            'coaching-agent-immobilier.html', 'coaching-boulangerie.html',
            'coaching-coiffeur.html', 'coaching-esthetique.html', 'coaching-restaurant.html']
OUTILS = ['diagnostic.html', 'rapport-diagnostic.html', 'plan-tresorerie.html',
          'generateur-calendrier-contenu.html', 'calculateur-cotisations-independant.html',
          'calculateur-cout-salarie.html', 'calculateur-delai-encaissement.html',
          'calculateur-marge.html', 'calculateur-taux-horaire.html',
          'calculateur-tva-franchise.html']
ARTICLES = ['conseils-chiffrer-chantier.html', 'conseils-facture-electronique-peppol.html',
            'conseils-facture-impayee.html', 'conseils-independant-complementaire.html',
            'conseils-lancer-independant.html', 'conseils-marge-restaurant.html',
            'conseils-taux-horaire-independant.html']
PLUS = ['a-propos.html', 'methode.html', 'statistiques.html', 'parrainage.html',
        'mentions-legales.html', 'confidentialite.html', 'cookies.html', 'cgv.html',
        'accessibilite.html', '404.html', 'offline.html']


def attendu(nom):
    """(lien d'onglet allumé, valeur d'aria-current, (href, libellé) du retour)."""
    racines = {'index.html': 'index.html', 'services.html': 'services.html',
               'contact.html': 'contact.html', 'outils.html': 'outils.html',
               'conseils.html': 'outils.html', 'ressources.html': 'outils.html',
               'mon-espace.html': 'mon-espace.html'}
    if nom in racines:
        lien = racines[nom]
        return lien, ('page' if lien == nom else 'true'), None
    if nom in SERVICES:
        return 'services.html', 'true', ('services.html', 'Services')
    if nom in OUTILS:
        return 'outils.html', 'true', ('outils.html', 'Outils')
    if nom in ARTICLES:
        return 'outils.html', 'true', ('conseils.html', 'Conseils')
    if nom in PLUS:
        return None, None, None
    raise KeyError(f'{nom} : page absente du tableau du § 3.2 de la conception')


def pages_du_site():
    return sorted(p.name for p in RACINE.glob('*.html'))


def source(nom, ref=None):
    """Le texte d'un fichier du dépôt, dans la copie de travail ou à une révision."""
    if ref is None:
        return (RACINE / nom).read_text(encoding='utf-8')
    r = subprocess.run(['git', 'show', f'{ref}:{nom}'], cwd=RACINE,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def ouvrir(contexte, base_url, chemin):
    """Ouvre une page ; la liste rendue se remplit des erreurs JavaScript et
    des erreurs de la console (ressource introuvable comprise)."""
    page = contexte.new_page()
    erreurs = []
    page.on('pageerror', lambda e: erreurs.append(str(e)))
    page.on('console', lambda m: erreurs.append(m.text) if m.type == 'error' else None)
    page.goto(f'{base_url}/{chemin}', wait_until='load')
    return page, erreurs


class _Serveur(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


class _Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def servir(dossier):
    """Sert un dossier sur un port libre ; appeler .shutdown() à la fin."""
    gestionnaire = functools.partial(_Silencieux, directory=str(dossier))
    serveur = _Serveur(('127.0.0.1', 0), gestionnaire)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    return serveur


class _Texte(HTMLParser):
    """Texte d'une zone (<main> ou <body>), en morceaux sans espaces superflus."""
    VIDES = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'path', 'circle',
             'rect', 'line', 'polyline', 'polygon', 'ellipse', 'use', 'wbr'}

    def __init__(self, zone, exclure, seulement):
        super().__init__(convert_charrefs=True)
        self.zone, self.exclure, self.seulement = zone, set(exclure), seulement
        self.dedans, self.pile, self.exclu, self.retenu = False, [], 0, 0
        self.morceaux = []

    def handle_starttag(self, tag, attrs):
        if tag == self.zone:
            self.dedans = True
            return
        if not self.dedans or tag in self.VIDES:
            return
        classes = set((dict(attrs).get('class') or '').split())
        exclue = tag in ('script', 'style', 'template') or bool(classes & self.exclure)
        retenue = bool(self.seulement) and self.seulement in classes
        self.pile.append((tag, exclue, retenue))
        self.exclu += exclue
        self.retenu += retenue

    def handle_endtag(self, tag):
        if tag == self.zone:
            self.dedans = False
            return
        if not self.dedans or tag in self.VIDES:
            return
        while self.pile:
            t, exclue, retenue = self.pile.pop()
            self.exclu -= exclue
            self.retenu -= retenue
            if t == tag:
                break

    def handle_data(self, data):
        if not self.dedans or self.exclu or (self.seulement and not self.retenu):
            return
        t = ' '.join(data.split())
        if t:
            self.morceaux.append(t)


# Ajouts du format app, absents du site de référence : hors comparaison.
AJOUTS = ('essentiel', 'segment-cadre', 'acces-rapide', 'duree', 'plus')


def morceaux(source_html, zone='main', exclure=AJOUTS, seulement=None):
    p = _Texte(zone, exclure, seulement)
    p.feed(source_html)
    return p.morceaux
