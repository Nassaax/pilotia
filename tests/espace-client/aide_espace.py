# -*- coding: utf-8 -*-
"""Outils partagés par les tests de l'espace client.

Le serveur de test (serveur.js) fait tourner les vraies fonctions api/ sur une
base PostgreSQL en mémoire ; les emails sont interceptés. Le module porte un
nom propre (aide_espace) pour ne pas se confondre avec celui du format app
quand les deux suites tournent ensemble."""
import http.client
import json
import pathlib
import subprocess
import urllib.parse

RACINE = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = pathlib.Path(__file__).resolve().parent
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
TELEPHONE = dict(viewport={'width': 390, 'height': 844}, device_scale_factor=2,
                 is_mobile=True, has_touch=True)
ORDINATEUR = dict(viewport={'width': 1280, 'height': 900})
COOKIE = '__Host-pilotia-session'


class Serveur:
    """Le serveur de test, lancé une fois pour toute la session."""

    def __init__(self):
        self.processus = subprocess.Popen(['node', str(DOSSIER / 'serveur.js')], cwd=DOSSIER,
                                          stdout=subprocess.PIPE, text=True)
        ligne = self.processus.stdout.readline().strip()
        assert ligne.startswith('PORT='), f'le serveur de test n’a pas démarré : {ligne!r}'
        self.port = int(ligne[5:])
        self.url = f'http://127.0.0.1:{self.port}'

    def _appel(self, methode, chemin, corps=None):
        c = http.client.HTTPConnection('127.0.0.1', self.port, timeout=30)
        c.request(methode, chemin, body=json.dumps(corps) if corps is not None else None,
                  headers={'Content-Type': 'application/json'})
        r = c.getresponse()
        texte = r.read().decode('utf-8')
        c.close()
        assert r.status == 200, (chemin, r.status, texte)
        return json.loads(texte)

    def courriels(self):
        return self._appel('GET', '/__test/courriels')

    def journal(self):
        return self._appel('GET', '/__test/journal')

    def sql(self, texte, *valeurs):
        return self._appel('POST', '/__test/sql', {'texte': texte, 'valeurs': list(valeurs)})

    def vider(self):
        self._appel('POST', '/__test/vider', {})

    def env(self, **variables):
        self._appel('POST', '/__test/env', variables)

    def arreter(self):
        self.processus.terminate()
        self.processus.wait(timeout=10)


class Reponse:
    def __init__(self, statut, entetes, texte):
        self.statut, self.entetes, self.texte = statut, entetes, texte

    @property
    def json(self):
        return json.loads(self.texte)

    def entete(self, nom):
        nom = nom.lower()
        return [v for k, v in self.entetes if k.lower() == nom]


class Client:
    """Un appareil vu du serveur : il garde son cookie de connexion comme un
    navigateur, et envoie par défaut l'en-tête Origin du site."""

    def __init__(self, serveur, ip='203.0.113.10'):
        self.serveur, self.ip, self.cookie = serveur, ip, None

    def requete(self, methode, chemin, corps=None, origine=None, entetes=None, type_json=True):
        e = {'X-Real-IP': self.ip}
        if type_json and corps is not None:
            e['Content-Type'] = 'application/json'
        if methode != 'GET':
            e['Origin'] = self.serveur.url if origine is None else origine
        if self.cookie:
            e['Cookie'] = f'{COOKIE}={self.cookie}'
        e.update(entetes or {})
        if not e.get('Origin'):
            e.pop('Origin', None)
        brut = None if corps is None else (corps if isinstance(corps, (bytes, str)) else json.dumps(corps))
        c = http.client.HTTPConnection('127.0.0.1', self.serveur.port, timeout=30)
        c.request(methode, chemin, body=brut, headers=e)
        r = c.getresponse()
        reponse = Reponse(r.status, r.getheaders(), r.read().decode('utf-8'))
        c.close()
        for valeur in reponse.entete('Set-Cookie'):
            nom, _, reste = valeur.partition('=')
            if nom == COOKIE:
                jeton = reste.split(';')[0]
                self.cookie = jeton if jeton and 'Max-Age=0' not in valeur else None
        return reponse

    def get(self, chemin, **k):
        return self.requete('GET', chemin, **k)

    def post(self, chemin, corps=None, **k):
        return self.requete('POST', chemin, {} if corps is None else corps, **k)

    def put(self, chemin, corps=None, **k):
        return self.requete('PUT', chemin, corps, **k)


def compte_url(action):
    return '/api/compte?' + urllib.parse.urlencode({'action': action})


def dernier_code(serveur, email):
    """Le code à 6 chiffres du dernier email envoyé à cette adresse."""
    import re
    for c in reversed(serveur.courriels()):
        if c['to'][0]['email'] == email:
            return re.search(r'\d{3} \d{3}', c['subject']).group(0).replace(' ', '')
    raise AssertionError(f'aucun email envoyé à {email}')


def connecter(serveur, client, email, prenom=None):
    """Crée l'espace, ou s'y connecte, par le vrai parcours : code puis conditions."""
    serveur.sql("update codes set envoye_le = envoye_le - interval '2 minutes'")
    assert client.post(compte_url('demander-code'), {'email': email}).statut == 200
    corps = {'email': email, 'code': dernier_code(serveur, email), 'conditions': True}
    if prenom:
        corps['prenom'] = prenom
    r = client.post(compte_url('verifier-code'), corps)
    assert r.statut == 200 and r.json['connecte'], r.texte
    return r.json


# Contraste du texte sur son fond (WCAG), et taille des cibles à toucher,
# mesurés dans la page comme pour le format app.
CONTRASTE = r"""(sel) => {
  const lin = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = c => { const [r, g, b] = c.match(/[\d.]+/g).map(Number);
                     return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b); };
  const fond = el => {
    for (; el; el = el.parentElement) {
      const c = getComputedStyle(el).backgroundColor;
      const p = c.match(/[\d.]+/g).map(Number);
      if (p.length < 4 || p[3] > 0.99) return c;
    }
    return 'rgb(255, 255, 255)';
  };
  return [...document.querySelectorAll(sel)]
    .filter(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden')
    .map(e => { const a = lum(getComputedStyle(e).color), b = lum(fond(e));
                return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); });
}"""

BOITES = """(sel) => [...document.querySelectorAll(sel)].filter(e => e.getClientRects().length)
  .map(e => { const r = e.getBoundingClientRect(); return [r.width, r.height]; })"""


def ouvrir(contexte, chemin):
    """Ouvre une page ; la liste rendue se remplit des erreurs JavaScript et
    de la console (ressource introuvable ou politique de sécurité comprises)."""
    page = contexte.new_page()
    erreurs = []
    page.on('pageerror', lambda e: erreurs.append(str(e)))
    page.on('console', lambda m: erreurs.append(m.text) if m.type == 'error' else None)
    page.goto(chemin, wait_until='load')
    return page, erreurs


def lire_local(page, cle):
    return page.evaluate('(c) => JSON.parse(localStorage.getItem(c))', cle)


def poser_local(page, cle, valeur):
    page.evaluate('([c, v]) => localStorage.setItem(c, v)', [cle, json.dumps(valeur)])


def attendre(condition, delai=8.0):
    """Attend qu'une condition (sans argument) rende une valeur vraie, et la rend."""
    import time
    fin = time.time() + delai
    while True:
        valeur = condition()
        if valeur or time.time() > fin:
            assert valeur, 'condition jamais remplie'
            return valeur
        time.sleep(0.1)


def element(serveur, cle, email='marie@exemple.be'):
    """L'élément tel qu'il est dans l'espace : {valeur, version}, ou None."""
    lignes = serveur.sql(
        'select e.valeur, e.version from elements e join comptes c on c.id = e.compte_id '
        'where c.email = $1 and e.cle = $2', email, cle)
    return lignes[0] if lignes else None


APPEL = """async ([adresse, corps]) => {
  const r = await fetch(adresse, {method: 'POST', headers: {'Content-Type': 'application/json'},
                                  body: JSON.stringify(corps)});
  return {statut: r.status, json: await r.json()};
}"""


def appareil(navigateur, serveur, ip, email='marie@exemple.be', prenom=None):
    """Un téléphone déjà connecté à l'espace, comme après connexion.html : la
    connexion se fait dans la page, pour que le navigateur garde lui-même son
    cookie (Chromium refuse qu'on lui pose un cookie Secure sur http), puis
    l'appareil reçoit la marque de l'espace. Le Client rendu partage cette
    connexion, pour agir dans l'espace sans passer par la page."""
    ctx = navigateur.new_context(**TELEPHONE, base_url=serveur.url, extra_http_headers={'X-Real-IP': ip})
    page = ctx.new_page()
    page.goto('/conditions-espace.html')  # une page sans compte.js
    serveur.sql("update codes set envoye_le = envoye_le - interval '2 minutes'")
    assert page.evaluate(APPEL, [compte_url('demander-code'), {'email': email}])['statut'] == 200
    corps = {'email': email, 'code': dernier_code(serveur, email), 'conditions': True}
    if prenom:
        corps['prenom'] = prenom
    r = page.evaluate(APPEL, [compte_url('verifier-code'), corps])
    assert r['statut'] == 200 and r['json']['connecte'], r
    client = Client(serveur, ip=ip)
    client.cookie = next(c['value'] for c in ctx.cookies() if c['name'] == COOKIE)
    poser_local(page, 'pilotia-espace', {'compte': r['json']['compte'], 'prenom': r['json']['prenom'] or '',
                                          'fiche': {}, 'calculs': {}, 'sync': {}, 'expire': False})
    return ctx, page, client
