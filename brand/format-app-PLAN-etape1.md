# Format app, étape 1 : plan de travail

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**But :** donner au site la navigation d'une app sur téléphone (barre d'onglets, retour, panneau « Plus »), créer les écrans Services et Mon espace, réorganiser l'onglet Outils et passer six pages pilotes au format app, avec une version de test Vercel à valider sur téléphone.

**Architecture :** le site reste en HTML, CSS et JavaScript simples, sans outil de construction. Un script Python répétable (`scripts/navigation-app.py`) écrit la navigation dans le HTML de chaque page, pour qu'elle fonctionne sans JavaScript. `app.js` ajoute les comportements : panneau, masquage pendant la saisie, sections repliables, défilement vers un résultat. Les styles vont dans une section « Format app » de `style.css`, limitée à 1 080 px pour ne pas toucher l'ordinateur.

**Pile :** HTML, CSS, JavaScript ES5 (comme `animations.js`) ; Python 3 pour le générateur et les tests ; pytest et Playwright (Chromium préinstallé dans `/opt/pw-browsers`).

**Conception :** `brand/format-app-CONCEPTION.md` (validée, mise à jour avec les décisions ci-dessous) ; maquettes dans `brand/format-app/`.

**Plan vérifié :** ce document est produit à partir d'un déroulé complet à blanc (copie de travail séparée, rien de publié). Chaque bloc de code ci-dessous a été exécuté, puis le plan entier a été rejoué tel qu'il est écrit sur une copie neuve de la branche : toutes les vérifications passent et le résultat est identique fichier par fichier.

## Contraintes globales

- Dépôt `/home/user/pilotis`, branche `format-app`. Aucun push sur `main` dans cette étape.
- Mode app : largeur de 1 080 px ou moins. Sections repliables : 760 px ou moins.
- Rendu sur ordinateur (1 280 px) identique au pixel près, sauf : l'encadré « L'essentiel » sur `facturation-electronique.html` et `conseils-facture-impayee.html`, les trois clés déclarées sur `cookies.html` et `confidentialite.html`, et les deux pages nouvelles.
- Texte d'origine conservé mot pour mot : comparaison automatique avec la révision `3433103` (le site avant le format app). Seules exceptions, listées une à une dans le test : les phrases des pages Cookies et Confidentialité qui parlaient d'une seule clé de stockage.
- Aucun tiret long « — » dans le texte visible ajouté. Aucun chiffre inventé : chaque nombre d'un encadré « L'essentiel » figure ailleurs dans la page (test automatique).
- Zones à toucher d'au moins 48 × 48 px. Contraste du texte d'au moins 4,5:1, en clair et en sombre.
- Pas de bibliothèque, pas de manifeste ni de service worker, pas de cookie ni de traceur. La politique de sécurité (`vercel.json`) ne change pas.
- Les adresses des pages existantes ne changent pas. Les calculs des outils ne changent pas.
- Commits en français, terminés par :
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC
  ```
- Tests : `cd /home/user/pilotis && python3 -m pytest tests/format-app -q` (environ 4 minutes en tout). Prérequis une fois par conteneur : `pip install -q pytest`. Pendant une tâche, on peut ne lancer que son fichier de test, mais la suite complète doit passer avant chaque commit.

## Décisions prises en rédigeant ce plan

Le déroulé à blanc a précisé quelques points de la conception ; elle est mise à jour en conséquence (§ 3.3, 4.2, 4.3, 5.1 et 5.2).

1. **Le résumé du plan de trésorerie** n'est écrit que si la personne a modifié son plan. Sinon, Mon espace afficherait comme le sien le plan d'exemple chargé à la première visite.
2. **« cet appareil » plutôt que « ce téléphone »** sur Mon espace : la page s'affiche aussi sur ordinateur.
3. **L'encadré « L'essentiel » se place juste avant les boutons du haut de page**, qui portent déjà l'action principale : pas de bouton en double. Sur la page Peppol, ses trois points reprennent le corps de la page plutôt que la phrase d'introduction affichée juste au-dessus.
4. **Sur ordinateur, les sections repliables n'existent pas** : le script ne crée ses enveloppes que sous 760 px et les retire au-delà. Le HTML reste exactement celui d'origine (testé).
5. **Le sur-titre d'une section repliée** (« Mauvais payeurs », « Questions fréquentes »…) s'affiche à l'ouverture, en tête du contenu.
6. **Accueil en mode app :** les deux boutons du haut cèdent la place aux quatre accès rapides, comme sur la maquette.
7. **Guides (`ressources.html`) :** chaque document garde son formulaire d'envoi ; il devient une ligne compacte, pas un lien sur toute la ligne.
8. **Menu « Découvrir » sur ordinateur :** « Tous les services » en tête, « Mon espace » en fin, actifs sur leur propre page.
9. **Débordement corrigé au passage :** deux calculateurs (cotisations, coût d'un salarié) débordaient de l'écran en 360 et 390 px à cause d'une liste déroulante.
10. **Remarque pour l'étape 2 (famille Outils) :** le calculateur de marge affiche « 75.0 % » avec un point. Les calculs restent hors de cette étape ; à corriger avec la famille Outils si vous le souhaitez.

---

## Fichiers

| Fichier | Rôle |
|---|---|
| `.vercelignore` (nouveau) | Ne publie pas le dossier `tests`. |
| `.gitignore` | Ignore les caches Python des tests. |
| `tests/format-app/aide.py` (nouveau) | Constantes, tableau attendu des onglets (copie du § 3.2 de la conception), serveur local, extraction du texte. |
| `tests/format-app/conftest.py` (nouveau) | Fixtures pytest : serveur, Chromium, contextes téléphone et ordinateur. |
| `tests/format-app/test_*.py` (nouveaux) | Un fichier par livrable, dont `test_ordinateur.py` (comparaison au pixel près). |
| `tests/format-app/essais/replis.html` (nouveau) | Page d'essai des sections repliables. |
| `scripts/navigation-app.py` (nouveau) | Écrit barre d'onglets, lien retour, panneau « Plus », sous-onglets et menu ordinateur dans chaque page. |
| `scripts/nouvelle-page.py` (nouveau) | Crée une page à partir du gabarit d'`outils.html`. |
| `app.js` (nouveau) | Comportements du format app. |
| `mon-espace.js` (nouveau) | Lecture et effacement des données locales, sur `mon-espace.html` seulement. |
| `services.html`, `mon-espace.html` (nouveaux) | Les deux nouveaux écrans. |
| `style.css` | Section « Format app » ajoutée en fin de fichier, tâche par tâche. |
| `animations.js` | Retrait de l'ancien menu mobile (le bouton ☰ ouvre le panneau). |
| `diagnostic.html`, `tresorerie.js` | Date du diagnostic, résumé du point bas pour Mon espace. |
| `outils.html`, `conseils.html`, `ressources.html` | Grilles transformées en listes sur téléphone. |
| Pilotes : `index.html`, `facturation-electronique.html`, `conseils-facture-impayee.html`, `calculateur-marge.html`, `contact.html`, `mentions-legales.html` | Format app. |
| `cookies.html`, `confidentialite.html` | Les trois clés de stockage local. |
| `sitemap.xml`, `llms.txt`, `README.md`, `brand/charte-app.md` (nouveau) | Référencement et documentation. |
| Toutes les autres pages `*.html` | Seulement la navigation générée. |

---

### Tâche 0 : outillage de test

**Fichiers :**
- Créer : `.vercelignore`, `tests/format-app/aide.py`, `tests/format-app/conftest.py`, `tests/format-app/test_outillage.py`, `tests/format-app/test_texte.py`
- Modifier : `.gitignore` (caches Python des tests)

**Interfaces :**
- Produit (`aide.py`) : `RACINE`, `CHROME`, `REFERENCE = '3433103'`, `TELEPHONE`, `ORDINATEUR`, `LARGEURS`, `ONGLETS`, `SERVICES`, `OUTILS`, `ARTICLES`, `PLUS` ; `attendu(nom) -> (lien_actif | None, 'page' | 'true' | None, (href, libellé) | None)` ; `pages_du_site() -> list[str]` ; `source(nom, ref=None) -> str | None` ; `ouvrir(contexte, base_url, chemin) -> (page, erreurs)` où `erreurs` reçoit les erreurs JavaScript et les erreurs de la console ; `servir(dossier) -> serveur` ; `morceaux(html, zone='main', exclure=AJOUTS, seulement=None) -> list[str]` ; `AJOUTS` (classes des ajouts du format app, hors comparaison du texte).
- Produit (fixtures) : `base_url`, `navigateur`, `telephone`, `ordinateur`.
- Produit (`test_texte.py`) : le dictionnaire `REECRITS` des passages réécrits volontairement, complété par la tâche 9.

- [ ] **Étape 1 : installer pytest et écrire le test d'outillage**

```bash
pip install -q pytest
mkdir -p tests/format-app/essais
```

`tests/format-app/test_outillage.py` :

```python
# -*- coding: utf-8 -*-
from aide import attendu, ouvrir, pages_du_site


def test_le_serveur_sert_le_site(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    assert page.title().startswith('Pilotia')
    assert erreurs == []


def test_chaque_page_est_classee_dans_la_conception():
    for nom in pages_du_site():
        attendu(nom)  # KeyError si une page manque au tableau du § 3.2
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_outillage.py -q`
Attendu : échec à l'import (`ModuleNotFoundError: No module named 'aide'`).

- [ ] **Étape 3 : écrire `aide.py`, `conftest.py`, `.vercelignore` et ignorer les caches Python**

`tests/format-app/aide.py` :

```python
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
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
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
        'accessibilite.html', '404.html']


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
```

`tests/format-app/conftest.py` :

```python
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
```

`.vercelignore` :

```text
# Les tests et leurs pages d'essai ne sont pas publiés.
tests
```

Ajouter à la fin de `.gitignore` :

```text

# Caches Python des tests
__pycache__/
```

- [ ] **Étape 4 : écrire le garde-fou du texte**

`tests/format-app/test_texte.py` :

```python
# -*- coding: utf-8 -*-
"""Le texte validé reste mot pour mot ; les ajouts n'inventent rien."""
import re

import pytest

from aide import REFERENCE, morceaux, pages_du_site, source

# Passages réécrits volontairement (tâche 9 : le stockage local passe d'une
# clé à trois). Chacun est un morceau exact du texte d'origine.
REECRITS = {}


def _sans_espaces(t):
    return re.sub(r'\s+', '', t)


@pytest.mark.parametrize('nom', pages_du_site())
def test_le_texte_d_origine_est_conserve(nom):
    ancien = source(nom, REFERENCE)
    if ancien is None:
        pytest.skip('page créée par le format app')
    apres = ' '.join(morceaux(source(nom)))
    reecrits = REECRITS.get(nom, [])
    manquants = [m for m in morceaux(ancien) if m not in apres and m not in reecrits]
    assert not manquants, f'{len(manquants)} passage(s) perdu(s), dont : {manquants[:3]}'


@pytest.mark.parametrize('nom', pages_du_site())
def test_les_nombres_de_l_essentiel_viennent_de_la_page(nom):
    html = source(nom)
    encadre = ' '.join(morceaux(html, exclure=(), seulement='essentiel'))
    if not encadre:
        pytest.skip("pas d'encadré « L'essentiel »")
    reste = _sans_espaces(' '.join(morceaux(html)))
    for nombre in re.findall(r'\d+(?:[\s.,]\d+)*', encadre):
        assert _sans_espaces(nombre) in reste, f'{nombre} absent du reste de la page'


@pytest.mark.parametrize('nom', pages_du_site())
def test_aucun_tiret_long_dans_les_ajouts(nom):
    html = source(nom)
    ajouts = []
    for classe in ('essentiel', 'onglets', 'plus', 'app-retour', 'segment-cadre',
                   'acces-rapide', 'duree'):
        ajouts += morceaux(html, zone='body', exclure=(), seulement=classe)
    if nom in ('services.html', 'mon-espace.html'):
        ajouts += morceaux(html, exclure=())
    assert '\u2014' not in ' '.join(ajouts)  # tiret long
```

- [ ] **Étape 5 : lancer, constater le succès**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe (aucune page n'a encore changé) ; les tests de l'encadré « L'essentiel » sont ignorés (`skipped`).

- [ ] **Étape 6 : commit**

```bash
git add .gitignore .vercelignore tests/format-app
git commit -q -m "Format app : outillage de test (serveur local, Chromium, garde-fou du texte)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 1 : générateur de la navigation

**Fichiers :**
- Créer : `scripts/navigation-app.py`, `app.js` (squelette), `tests/format-app/test_navigation_statique.py`
- Modifier (par le script) : les 43 pages `*.html`

**Interfaces :**
- Consomme : `aide.attendu`, `aide.pages_du_site`, `aide.source`, `aide.ONGLETS`, `aide.RACINE`.
- Produit, dans chaque page : les blocs `<!-- app:retour -->`, `<!-- app:onglets -->`, `<!-- app:plus -->` (et `<!-- app:segment -->` sur `outils.html`, `conseils.html`, `ressources.html`) ; le menu « Découvrir » complété de « Tous les services » (en tête) et « Mon espace » (en fin) ; les classes et identifiants `.onglets`, `.onglet`, `.onglet-centre`, `.onglet-icone`, `.onglet-rond`, `.onglet-libelle`, `.app-retour`, `header.a-retour`, `dialog#panneauPlus.plus`, `.plus-poignee`, `.plus-tete`, `.plus-titre#plusTitre`, `.plus-fermer`, `.plus-groupe`, `.plus-liste`, `.segment-cadre`, `.segment` ; `#navToggle[aria-controls=panneauPlus][aria-haspopup=dialog]` ; `app.js` chargé juste après `animations.js`.
- Commande : `python3 scripts/navigation-app.py [--verifier]`.

- [ ] **Étape 1 : écrire les tests statiques**

`tests/format-app/test_navigation_statique.py` :

```python
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
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_navigation_statique.py -q`
Attendu : échecs « barre d'onglets absente », « marqueurs du lien retour absents », etc.

- [ ] **Étape 3 : écrire le générateur et le squelette d'`app.js`**

`scripts/navigation-app.py` :

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit la navigation « format app » dans chaque page du site.

    python3 scripts/navigation-app.py             # met les pages à jour
    python3 scripts/navigation-app.py --verifier  # échoue si une page n'est pas à jour

À relancer après toute création de page ou tout changement de navigation.
Chaque bloc généré est délimité par <!-- app:nom --> et <!-- /app:nom -->,
puis remplacé à chaque passage : relancer le script ne change rien de plus.
Correspondance des pages et des onglets : brand/format-app-CONCEPTION.md, § 3.2."""
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent

# Icônes au trait (grille de 24, trait de 2). Sources reprises dans brand/charte-app.md.
ICONES = {
    'accueil': '<path d="M3.5 10.5 12 3.5l8.5 7V20a1 1 0 0 1-1 1h-4.5v-6h-6v6H4.5a1 1 0 0 1-1-1z"/>',
    'services': '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8.5 7V5.5a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2V7M3 12.5h18"/>',
    'rdv': '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17M12 12.5v5M9.5 15h5"/>',
    'outils': '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7h7M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01M8.5 15h.01M12 15h.01M15.5 15h.01M8.5 18h.01M12 18h.01M15.5 18h.01"/>',
    'espace': '<circle cx="12" cy="8.5" r="4"/><path d="M4.5 20.5c.8-3.6 3.9-6 7.5-6s6.7 2.4 7.5 6"/>',
    'retour': '<path d="M15 5l-7 7 7 7"/>',
    'chevron': '<path d="m9 6 6 6-6 6"/>',
    'externe': '<path d="M7 17 17 7M9 7h8v8"/>',
    'fermer': '<path d="M6 6l12 12M18 6L6 18"/>',
}


def svg(nom):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false">{ICONES[nom]}</svg>')


ONGLETS = [('accueil', 'index.html', 'Accueil'),
           ('services', 'services.html', 'Services'),
           ('rdv', 'contact.html', 'Rendez-vous'),
           ('outils', 'outils.html', 'Outils'),
           ('espace', 'mon-espace.html', 'Mon espace')]
SERVICES = ('entreprises.html', 'independants.html', 'facturation-electronique.html',
            'affacturage.html', 'marketing-digital.html', 'offres.html')
OUTILS = ('diagnostic.html', 'rapport-diagnostic.html', 'plan-tresorerie.html',
          'generateur-calendrier-contenu.html')
RETOURS = {'services': ('services.html', 'Services'),
           'outils': ('outils.html', 'Outils'),
           'conseils': ('conseils.html', 'Conseils')}
PLUS_PILOTIA = [('a-propos.html', 'À propos'), ('methode.html', 'Notre méthode'),
                ('statistiques.html', 'Statistiques'), ('parrainage.html', 'Parrainage')]
PLUS_INFOS = [('mentions-legales.html', 'Mentions légales'),
              ('confidentialite.html', 'Confidentialité'), ('cookies.html', 'Cookies'),
              ('cgv.html', 'Conditions générales'), ('accessibilite.html', 'Accessibilité')]
SEGMENT = [('outils.html', 'Outils'), ('conseils.html', 'Conseils'),
           ('ressources.html', 'Guides')]


def placer(nom):
    """(onglet allumé, lien retour) d'une page ; None quand il n'y en a pas."""
    if nom == 'index.html':
        return 'accueil', None
    if nom == 'services.html':
        return 'services', None
    if nom in SERVICES or nom.startswith('coaching-'):
        return 'services', 'services'
    if nom == 'contact.html':
        return 'rdv', None
    if nom in ('outils.html', 'conseils.html', 'ressources.html'):
        return 'outils', None
    if nom in OUTILS or nom.startswith('calculateur-'):
        return 'outils', 'outils'
    if nom.startswith('conseils-'):
        return 'outils', 'conseils'
    if nom == 'mon-espace.html':
        return 'espace', None
    return None, None


def barre(nom, onglet):
    liens = []
    for cle, page, libelle in ONGLETS:
        courant = ''
        if cle == onglet:
            courant = ' aria-current="page"' if page == nom else ' aria-current="true"'
        if cle == 'rdv':
            liens.append(f'<a href="{page}" class="onglet onglet-centre"{courant}>'
                         f'<span class="onglet-rond">{svg(cle)}</span>'
                         f'<span class="onglet-libelle">{libelle}</span></a>')
        else:
            liens.append(f'<a href="{page}" class="onglet"{courant}>'
                         f'<span class="onglet-icone">{svg(cle)}</span>'
                         f'<span class="onglet-libelle">{libelle}</span></a>')
    return ('\n<nav class="onglets" aria-label="Navigation principale">\n  '
            + '\n  '.join(liens) + '\n</nav>\n')


def retour(cle):
    if cle is None:
        return ''
    href, libelle = RETOURS[cle]
    return (f'<a class="app-retour" href="{href}" aria-label="Revenir à la page {libelle}">'
            f'{svg("retour")}<span>{libelle}</span></a>')


def panneau(nom):
    def ligne(href, libelle):
        courant = ' aria-current="page"' if href == nom else ''
        return f'<li><a href="{href}"{courant}>{libelle}{svg("chevron")}</a></li>'
    pilotia = ''.join(ligne(h, l) for h, l in PLUS_PILOTIA)
    insta = ('<li><a href="https://www.instagram.com/pilotia.be/" target="_blank" '
             'rel="noopener noreferrer">Instagram<span class="sr-only"> (ouvre un nouvel '
             f'onglet)</span>{svg("externe")}</a></li>')
    infos = ''.join(ligne(h, l) for h, l in PLUS_INFOS)
    return ('\n<dialog class="plus" id="panneauPlus" aria-labelledby="plusTitre">\n'
            '  <div class="plus-poignee" aria-hidden="true"></div>\n'
            '  <div class="plus-tete"><h2 class="plus-titre" id="plusTitre">Plus</h2>'
            f'<button type="button" class="plus-fermer" aria-label="Fermer">{svg("fermer")}'
            '</button></div>\n'
            f'  <h3 class="plus-groupe">Pilotia</h3>\n  <ul class="plus-liste">{pilotia}{insta}</ul>\n'
            f'  <h3 class="plus-groupe">Informations</h3>\n  <ul class="plus-liste">{infos}</ul>\n'
            '</dialog>\n')


def segment(nom):
    liens = ''.join(f'<a href="{h}"' + (' aria-current="page"' if h == nom else '') + f'>{l}</a>'
                    for h, l in SEGMENT)
    return ('\n<div class="wrap segment-cadre"><nav class="segment" '
            f'aria-label="Rubriques de l\'onglet Outils">{liens}</nav></div>\n')


def menu(t, nom):
    """Menu « Découvrir » (ordinateur) : « Tous les services » en tête et
    « Mon espace » en fin, actifs sur leur propre page. Les deux entrées sont
    retirées puis reposées, ce qui rend l'opération répétable."""
    m = re.search(r'(<ul class="dropdown-menu">)(.*?)(\n[ \t]*</ul>)', t, re.S)
    retrait = re.search(r'\n([ \t]*)<li>', m.group(2)).group(1)
    entrees = [li for li in re.findall(r'<li>.*?</li>', m.group(2))
               if 'href="services.html"' not in li and 'href="mon-espace.html"' not in li]

    def entree(href, libelle):
        actif = ' class="active"' if href == nom else ''
        return f'<li><a href="{href}"{actif}>{libelle}</a></li>'
    entrees = ([entree('services.html', 'Tous les services')] + entrees
               + [entree('mon-espace.html', 'Mon espace')])
    bloc = m.group(1) + ''.join('\n' + retrait + li for li in entrees) + m.group(3)
    t = t[:m.start()] + bloc + t[m.end():]
    if nom in ('services.html', 'mon-espace.html'):
        t = t.replace('class="dropdown-trigger" ', 'class="dropdown-trigger active" ', 1)
    return t


def poser(html, nom, contenu, apres=None, avant=None):
    """Remplace le bloc s'il existe, sinon l'insère après (ou avant) l'ancre."""
    motif = re.compile(rf'<!-- app:{nom} -->.*?<!-- /app:{nom} -->', re.S)
    neuf = f'<!-- app:{nom} -->{contenu}<!-- /app:{nom} -->'
    if motif.search(html):
        return motif.sub(lambda m: neuf, html, count=1)
    ancre = apres if apres is not None else avant
    i = html.index(ancre)
    debut = html.rfind('\n', 0, i) + 1
    retrait = re.match(r'[ \t]*', html[debut:]).group(0)
    if apres is not None:
        j = i + len(ancre)
        return html[:j] + '\n' + retrait + neuf + html[j:]
    return html[:i] + neuf + '\n' + retrait + html[i:]


def traiter(texte, nom):
    onglet, cle_retour = placer(nom)
    t = texte.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">')
    classe = 'site-header a-retour' if cle_retour else 'site-header'
    t = re.sub(r'<header class="site-header[^"]*">', f'<header class="{classe}">', t, count=1)
    t = t.replace('aria-controls="navLinks" aria-label="Ouvrir le menu"',
                  'aria-controls="panneauPlus" aria-haspopup="dialog" aria-label="Ouvrir le menu"')
    t = menu(t, nom)
    marque = re.search(r'<a href="index.html" class="brand">.*?</a>', t, re.S).group(0)
    t = poser(t, 'retour', retour(cle_retour), apres=marque)
    t = poser(t, 'onglets', barre(nom, onglet), apres='</header>')
    t = poser(t, 'plus', panneau(nom), avant='<script src="animations.js"')
    if '<script src="app.js" defer></script>' not in t:
        t = t.replace('<script src="animations.js" defer></script>',
                      '<script src="animations.js" defer></script>\n'
                      '<script src="app.js" defer></script>', 1)
    if nom in ('outils.html', 'conseils.html', 'ressources.html'):
        principal = re.search(r'<main id="contenu"[^>]*>', t).group(0)
        t = poser(t, 'segment', segment(nom), apres=principal)
    return t


def main():
    verifier = '--verifier' in sys.argv[1:]
    a_jour = []
    for chemin in sorted(RACINE.glob('*.html')):
        avant = chemin.read_text(encoding='utf-8')
        apres = traiter(avant, chemin.name)
        if apres != avant:
            a_jour.append(chemin.name)
            if not verifier:
                chemin.write_text(apres, encoding='utf-8')
    if verifier:
        if a_jour:
            print('Pages à régénérer :', ', '.join(a_jour))
            sys.exit(1)
        print('Toutes les pages sont à jour.')
    else:
        print(f'{len(a_jour)} page(s) mise(s) à jour.')
        for n in a_jour:
            print('  ', n)


if __name__ == '__main__':
    main()
```

`app.js` (squelette ; la tâche 3 le remplit, il évite d'ici là une erreur 404) :

```js
/* Format app (brand/format-app-CONCEPTION.md). Chargé après animations.js
   sur toutes les pages. Comportements ajoutés par les tâches suivantes. */
(function () {
  "use strict";
})();
```

- [ ] **Étape 4 : générer, puis relancer pour prouver que le script est répétable**

```bash
python3 scripts/navigation-app.py
python3 scripts/navigation-app.py --verifier
```

Attendu : « 43 page(s) mise(s) à jour. » puis « Toutes les pages sont à jour. »

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe (la navigation est hors de `<main>` : le garde-fou du texte reste vert).

- [ ] **Étape 6 : commit**

```bash
git add scripts/navigation-app.py app.js tests/format-app/test_navigation_statique.py *.html
git commit -q -m "Format app : navigation générée dans toutes les pages

Barre d'onglets (Accueil, Services, Rendez-vous, Outils, Mon espace), lien
retour sur les pages de détail, panneau « Plus », sous-onglets d'Outils et
entrées « Tous les services » et « Mon espace » dans le menu ordinateur.
Écrits par scripts/navigation-app.py (répétable, option --verifier).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 2 : styles de la coquille (barre d'onglets, en-tête, panneau)

**Fichiers :**
- Modifier : `style.css` (ajout en fin de fichier)
- Créer : `tests/format-app/test_coquille.py`

**Interfaces :**
- Consomme : les classes produites par la tâche 1.
- Produit : la variable CSS `--hauteur-onglets` ; la classe `html.saisie` (masque la barre, posée par la tâche 3) ; les règles qui masquent sur ordinateur `.onglets`, `.app-retour`, `.segment-cadre`, `.acces-rapide`, `.duree` ; dans `test_coquille.py`, les scripts de mesure `CONTRASTE` et `BOITES`, réutilisés par les tâches suivantes.

- [ ] **Étape 1 : écrire les tests**

`tests/format-app/test_coquille.py` :

```python
# -*- coding: utf-8 -*-
"""La coquille d'app s'affiche en mode app et seulement là (§ 3 de la conception)."""
import pytest

from aide import LARGEURS, TELEPHONE, attendu, ouvrir, pages_du_site

PAGES = pages_du_site()

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


@pytest.mark.parametrize('nom', PAGES)
def test_barre_en_mode_app_seulement(nom, telephone, ordinateur, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    assert page.locator('.onglets').is_visible()
    assert not page.locator('.nav-links').is_visible()
    page, _ = ouvrir(ordinateur, base_url, nom)
    assert not page.locator('.onglets').is_visible()
    assert not page.locator('.app-retour').is_visible()
    assert page.locator('.nav-links').is_visible()


@pytest.mark.parametrize('nom', PAGES)
def test_retour_ou_logo(nom, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    retour = attendu(nom)[2]
    assert page.locator('.app-retour').is_visible() == (retour is not None)
    assert page.locator('.site-header .brand').is_visible() == (retour is None)


@pytest.mark.parametrize('largeur', LARGEURS)
@pytest.mark.parametrize('nom', PAGES)
def test_pas_de_defilement_horizontal(nom, largeur, navigateur, base_url):
    ctx = navigateur.new_context(viewport={'width': largeur, 'height': 800})
    try:
        page, _ = ouvrir(ctx, base_url, nom)
        assert page.evaluate('document.documentElement.scrollWidth') <= largeur
    finally:
        ctx.close()


@pytest.mark.parametrize('nom', PAGES)
def test_la_barre_ne_cache_pas_le_bas_de_page(nom, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    # « instant » : le site défile en douceur (scroll-behavior), le test n'attend pas.
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_timeout(100)
    # Le pied de page, ou le contenu principal sur la page 404 qui n'en a pas.
    bas = page.evaluate("(document.querySelector('.site-footer') || document.querySelector('main'))"
                        ".getBoundingClientRect().bottom")
    barre = page.evaluate("document.querySelector('.onglets').getBoundingClientRect().top")
    assert bas <= barre + 1


@pytest.mark.parametrize('nom', ['index.html', 'calculateur-marge.html',
                                 'conseils-facture-impayee.html', 'contact.html'])
def test_zones_a_toucher(nom, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    for sel in ('.onglet', '.app-retour', '#navToggle'):
        for largeur, hauteur in page.evaluate(BOITES, sel):
            assert largeur >= 48 and hauteur >= 48, (sel, largeur, hauteur)


@pytest.mark.parametrize('schema', ['light', 'dark'])
@pytest.mark.parametrize('nom', ['index.html', 'calculateur-marge.html',
                                 'facturation-electronique.html', 'conseils-facture-impayee.html',
                                 'contact.html'])
def test_contrastes_de_la_navigation(nom, schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, _ = ouvrir(ctx, base_url, nom)
        for sel in ('.onglet-libelle', '.app-retour span'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
    finally:
        ctx.close()
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_coquille.py -q -x`
Attendu : échec de `test_barre_en_mode_app_seulement` (la barre n'a pas encore de style).

- [ ] **Étape 3 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` (le correctif des deux calculateurs qui débordaient en 360 et 390 px en fait partie) :

```css

/* ─── Format app (téléphone et tablette) ──────────────────────────────────
   brand/format-app-CONCEPTION.md. Le mode app commence à 1 080 px, le seuil
   où le menu du haut se repliait déjà. Rien dans cette section ne change le
   rendu sur ordinateur, sauf l'encadré « L'essentiel ». */
:root{--hauteur-onglets:64px}
.onglets,.app-retour,.segment-cadre,.acces-rapide,.duree{display:none}

@media (max-width:1080px){
  body{padding-bottom:calc(var(--hauteur-onglets) + env(safe-area-inset-bottom))}

  /* En-tête : logo, ou lien retour sur les pages de détail, et bouton ☰. */
  .nav-links{display:none !important}
  .nav-toggle{width:48px;height:48px;padding:12px}
  .site-header{view-transition-name:entete}
  .site-header.a-retour .brand{display:none}
  .app-retour{
    display:inline-flex;align-items:center;gap:2px;min-height:48px;padding:0 12px 0 2px;margin-left:-10px;
    color:var(--accent);font-family:var(--font-body);font-size:17px;font-weight:600;text-decoration:none;
  }
  .app-retour svg{flex:none;width:26px;height:26px}

  /* Barre d'onglets. Elle garde les couleurs de la marque sur toutes les
     pages, même celles qui prennent la couleur d'un service (valeurs des
     jetons de :root, clair puis sombre). */
  .onglets{
    --accent:#0369A1;--accent-soft:#E1EEF6;--accent-ink:#FFFFFF;
    display:flex;justify-content:space-around;align-items:flex-start;
    position:fixed;left:0;right:0;bottom:0;z-index:30;
    height:calc(var(--hauteur-onglets) + env(safe-area-inset-bottom));
    padding:6px max(4px, env(safe-area-inset-right)) env(safe-area-inset-bottom) max(4px, env(safe-area-inset-left));
    background:var(--card);border-top:1px solid var(--line);
    font-family:var(--font-body);view-transition-name:onglets;
  }
  .onglet{
    flex:1 1 0;min-width:48px;max-width:96px;min-height:52px;
    display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:3px;
    color:var(--ink-soft);text-decoration:none;font-size:11.5px;font-weight:600;line-height:16px;
    -webkit-tap-highlight-color:transparent;
  }
  .onglet-icone{width:56px;height:30px;border-radius:15px;display:flex;align-items:center;justify-content:center;transition:background .18s ease}
  .onglet svg{width:24px;height:24px}
  .onglet[aria-current]{color:var(--accent)}
  .onglet[aria-current] .onglet-icone{background:var(--accent-soft)}
  .onglet-libelle{white-space:nowrap}
  .onglet-centre{position:relative;color:var(--ink);font-weight:700}
  .onglet-rond{
    position:absolute;top:-24px;left:50%;margin-left:-30px;width:60px;height:60px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    background:var(--accent);color:var(--accent-ink);border:2px solid var(--trait);box-shadow:3px 3px 0 var(--trait);
  }
  .onglet-rond svg{width:28px;height:28px}
  .onglet-centre[aria-current]{color:var(--accent)}
  .onglet-centre[aria-current] .onglet-rond{box-shadow:3px 3px 0 var(--trait),0 0 0 5px var(--accent-soft)}
  .onglet:focus-visible{outline:3px solid var(--accent);outline-offset:-3px;border-radius:12px}
  .saisie .onglets{display:none}

  /* Panneau « Plus » : un <dialog> qui monte du bas de l'écran. */
  .plus{
    position:fixed;inset:auto 0 0 0;margin:0;width:100%;max-width:100%;max-height:min(85vh,640px);
    border:none;border-radius:24px 24px 0 0;padding:10px 0 calc(20px + env(safe-area-inset-bottom));
    background:var(--card);color:var(--ink);overflow-y:auto;font-family:var(--font-body);
    box-shadow:0 -10px 40px rgba(15,23,42,.25);
  }
  .plus::backdrop{background:rgba(15,23,42,.45)}
  .plus[open]{animation:plus-monte .22s cubic-bezier(.2,.8,.2,1)}
  .plus-poignee{width:40px;height:5px;border-radius:3px;background:var(--line-strong);opacity:.6;margin:0 auto 6px}
  .plus-tete{display:flex;align-items:center;justify-content:space-between;padding:0 10px 4px 22px}
  .plus-titre{margin:0;font-family:var(--font-body);font-size:20px;font-weight:700}
  .plus-fermer{width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:none;border:none;border-radius:12px;color:var(--ink);cursor:pointer}
  .plus-fermer svg{width:24px;height:24px}
  .plus-groupe{margin:14px 22px 2px;font-family:var(--font-body);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft)}
  .plus-liste{list-style:none;margin:0;padding:0 22px}
  .plus-liste li{border-bottom:1px solid var(--line)}
  .plus-liste li:last-child{border-bottom:none}
  .plus-liste a{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:50px;color:var(--ink);text-decoration:none;font-size:16.5px;font-weight:500}
  .plus-liste a[aria-current]{color:var(--accent);font-weight:600}
  .plus-liste svg{flex:none;width:18px;height:18px;color:var(--ink-soft)}

  /* Correctif : une liste déroulante au libellé long élargissait le
     formulaire au-delà de l'écran (calculateurs de cotisations et du coût
     d'un salarié, en 360 et 390 px). */
  form{grid-template-columns:minmax(0,1fr)}
  select{max-width:100%}
}
@media (max-width:1080px) and (prefers-color-scheme: dark){
  .onglets{--accent:#4CA9E0;--accent-soft:#16283D;--accent-ink:#08131F}
}
@keyframes plus-monte{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}

/* Fondu entre deux pages ; les deux barres restent en place. */
@view-transition{navigation:auto}
::view-transition-old(root),::view-transition-new(root){animation-duration:.18s}
@media (prefers-reduced-motion: reduce){
  @view-transition{navigation:none}
  .plus[open]{animation:none}
}
@media print{
  .onglets,.plus,.app-retour,.segment-cadre,.replis-outils{display:none !important}
  body{padding-bottom:0}
}
```

- [ ] **Étape 4 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe (environ 2 minutes pour `test_coquille.py`, qui ouvre chaque page à quatre largeurs).

- [ ] **Étape 5 : commit**

```bash
git add style.css tests/format-app/test_coquille.py
git commit -q -m "Format app : styles de la barre d'onglets, de l'en-tête et du panneau

Barre fixe en mode app (1 080 px ou moins), zone de sécurité de l'iPhone,
couleurs de la marque sur toutes les pages, fondu entre les pages.
Corrige au passage le débordement de deux calculateurs en 360 et 390 px.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 3 : panneau « Plus » et barre masquée pendant la saisie

**Fichiers :**
- Modifier : `app.js` (remplacer le squelette), `animations.js:52-101`
- Créer : `tests/format-app/test_comportements.py`

**Interfaces :**
- Produit : `window.PilotiaApp.versResultat(idOuElement)` (utilisé par la tâche 13) ; la classe `html.saisie` ; dans `app.js`, les variables `modeApp`, `modeTelephone` et `mouvementReduit`, que la tâche 4 réutilise.

- [ ] **Étape 1 : écrire les tests**

`tests/format-app/test_comportements.py` :

```python
# -*- coding: utf-8 -*-
"""Panneau « Plus », barre masquée pendant la saisie, aucune erreur JavaScript."""
import pytest
from playwright.sync_api import expect

from aide import TELEPHONE, ouvrir, pages_du_site
from test_coquille import CONTRASTE

OUVERT = "document.getElementById('panneauPlus').open"


def test_le_panneau_s_ouvre_et_se_ferme(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    bouton = page.locator('#navToggle')
    bouton.click()
    assert page.evaluate(OUVERT)
    expect(bouton).to_have_attribute('aria-expanded', 'true')
    page.keyboard.press('Escape')
    assert not page.evaluate(OUVERT)
    # L'évènement « close » d'un <dialog> arrive juste après : expect attend.
    expect(bouton).to_have_attribute('aria-expanded', 'false')
    expect(bouton).to_be_focused()
    bouton.click()
    page.locator('.plus-fermer').click()
    assert not page.evaluate(OUVERT)
    bouton.click()
    page.mouse.click(195, 60)  # sur le voile, au-dessus du panneau
    assert not page.evaluate(OUVERT)
    assert erreurs == []


def test_le_panneau_signale_la_page_courante(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'cgv.html')
    page.locator('#navToggle').click()
    assert page.locator('.plus-liste a[aria-current="page"]').inner_text().strip() == 'Conditions générales'
    page.locator('.plus-liste a', has_text='À propos').click()
    page.wait_for_url('**/a-propos.html')


@pytest.mark.parametrize('schema', ['light', 'dark'])
def test_contrastes_du_panneau(schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, _ = ouvrir(ctx, base_url, 'index.html')
        page.locator('#navToggle').click()
        for sel in ('.plus-titre', '.plus-groupe', '.plus-liste a'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
    finally:
        ctx.close()


def test_la_saisie_masque_la_barre(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, 'calculateur-marge.html')
    page.focus('#prixVente')
    page.wait_for_timeout(100)
    assert not page.locator('.onglets').is_visible()
    page.evaluate('document.activeElement.blur()')
    page.wait_for_timeout(150)
    assert page.locator('.onglets').is_visible()


@pytest.mark.parametrize('nom', pages_du_site())
def test_aucune_erreur_javascript(nom, telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, nom)
    page.wait_for_timeout(200)
    assert erreurs == []
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_comportements.py -q`
Attendu : échecs de `test_le_panneau_s_ouvre_et_se_ferme` (le panneau ne s'ouvre pas) et de `test_la_saisie_masque_la_barre`.

- [ ] **Étape 3 : retirer l'ancien menu mobile d'`animations.js`**

Dans `animations.js`, remplacer :

```js
/* Menu mobile (hamburger) + menu déroulant "Découvrir" — navigation de base,
   ne dépend pas de prefers-reduced-motion (ce n'est pas une animation décorative). */
(function () {
  "use strict";

  var toggle = document.getElementById("navToggle");
  var navLinks = document.getElementById("navLinks");

  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      var open = navLinks.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var dropdowns = document.querySelectorAll(".dropdown");
```

par :

```js
/* Menu déroulant "Découvrir" (ordinateur) : navigation de base, qui ne dépend
   pas de prefers-reduced-motion. Sur les écrans étroits, le bouton ☰ ouvre le
   panneau « Plus » : voir app.js. */
(function () {
  "use strict";

  var dropdowns = document.querySelectorAll(".dropdown");
```

puis remplacer :

```js
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    });
    if (navLinks && navLinks.classList.contains("is-open")) {
      navLinks.classList.remove("is-open");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    }
  });
```

par :

```js
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    });
  });
```

- [ ] **Étape 4 : écrire `app.js`**

`app.js` :

```js
/* Format app (brand/format-app-CONCEPTION.md) : panneau « Plus », barre
   d'onglets masquée pendant la saisie, sections repliables sur téléphone et
   défilement vers un résultat de calcul. Chargé après animations.js sur
   toutes les pages. Sans JavaScript, la barre d'onglets fonctionne et tout
   le contenu reste ouvert. */
(function () {
  "use strict";

  var racine = document.documentElement;
  var modeApp = window.matchMedia("(max-width: 1080px)");
  var modeTelephone = window.matchMedia("(max-width: 760px)");
  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ───── Panneau « Plus » : un <dialog> natif, qui garde le focus et se
     ferme à la touche Échap sans code supplémentaire. */
  var bouton = document.getElementById("navToggle");
  var panneau = document.getElementById("panneauPlus");
  if (bouton && panneau && typeof panneau.showModal === "function") {
    bouton.addEventListener("click", function () {
      panneau.showModal();
      bouton.setAttribute("aria-expanded", "true");
    });
    panneau.addEventListener("close", function () {
      bouton.setAttribute("aria-expanded", "false");
      bouton.focus();
    });
    panneau.querySelector(".plus-fermer").addEventListener("click", function () {
      panneau.close();
    });
    // Un toucher sur le voile, hors du panneau, le ferme.
    panneau.addEventListener("click", function (e) {
      if (e.target !== panneau) return;
      var r = panneau.getBoundingClientRect();
      if (e.clientY < r.top || e.clientY > r.bottom || e.clientX < r.left || e.clientX > r.right) {
        panneau.close();
      }
    });
    // Le panneau n'existe qu'en mode app : s'il est ouvert quand l'écran
    // s'élargit, on le referme.
    modeApp.addEventListener("change", function (e) {
      if (!e.matches && panneau.open) panneau.close();
    });
  }

  /* ───── Barre d'onglets masquée pendant la saisie : le clavier du
     téléphone occupe déjà le bas de l'écran. */
  var CHAMPS = "input:not([type=checkbox]):not([type=radio]):not([type=button])" +
    ":not([type=submit]):not([type=reset]):not([type=range]):not([type=file])" +
    ":not([type=color]), select, textarea";
  function estChamp(n) { return !!(n && n.matches && n.matches(CHAMPS)); }
  document.addEventListener("focusin", function (e) {
    if (modeApp.matches && estChamp(e.target)) racine.classList.add("saisie");
  });
  document.addEventListener("focusout", function () {
    // Le focus passe parfois d'un champ à l'autre : on attend la cible suivante.
    setTimeout(function () {
      if (!estChamp(document.activeElement)) racine.classList.remove("saisie");
    }, 60);
  });

  /* ───── Défilement vers un résultat de calcul (appelé par les calculateurs). */
  function versResultat(cible) {
    var el = typeof cible === "string" ? document.getElementById(cible) : cible;
    if (!el || !modeApp.matches) return;
    el.scrollIntoView({ block: "nearest", behavior: mouvementReduit.matches ? "auto" : "smooth" });
  }
  window.PilotiaApp = { versResultat: versResultat };
})();
```

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 6 : commit**

```bash
git add app.js animations.js tests/format-app/test_comportements.py
git commit -q -m "Format app : panneau « Plus » et barre masquée pendant la saisie

Le bouton ☰ ouvre un <dialog> natif (Échap, voile, retour du focus) ;
l'ancien menu mobile d'animations.js est retiré. PilotiaApp.versResultat
prépare le défilement vers les résultats des calculateurs.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 4 : sections repliables

**Fichiers :**
- Modifier : `app.js` (ajout avant la dernière ligne), `style.css` (ajout en fin de fichier)
- Créer : `tests/format-app/essais/replis.html`, `tests/format-app/test_replis.py`

**Interfaces :**
- Consomme : `modeTelephone` (déclaré dans `app.js` par la tâche 3).
- Produit, pour le balisage des pages :
  - `data-repli` sur un élément qui contient un `h2` : son premier `h2` devient le titre, tout ce qui le suit dans le même parent devient le corps ; un sur-titre (`.eyebrow`) placé juste avant passe en tête du corps ;
  - `data-replis-h2` sur un conteneur : chaque `h2` enfant direct ouvre un groupe qui va jusqu'au `h2` suivant ;
  - `data-replis` sur un conteneur (en pratique `<main>`) : bouton « Tout ouvrir / Tout fermer » dès deux replis.
- Produit, côté rendu (sur téléphone seulement, retiré au-delà de 760 px) : `div.repli-groupe`, `div.repli-corps#repli-corps-N`, `.repli-actif`, `.repli-ouvert`, `h2.repli-titre > button.repli-bouton[aria-expanded][aria-controls] > span.repli-texte + svg.repli-chevron`, `.replis-outils > button.replis-tout`, l'attribut `data-sombre` (section sombre éclaircie).

- [ ] **Étape 1 : écrire la page d'essai**

`tests/format-app/essais/replis.html` :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Essai des sections repliables</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/style.css">
<script>document.documentElement.classList.add("js");</script>
</head>
<body>
<main id="contenu" data-replis>
<section class="hero"><div class="wrap"><h1>Essai</h1></div></section>
<section data-repli id="s1">
  <div class="wrap">
    <div class="eyebrow" id="e1">Sur-titre un</div>
    <h2 class="section-title">Première section</h2>
    <p id="p1">Texte de la première section.</p>
  </div>
</section>
<section class="section-sombre" data-repli id="s2">
  <div class="wrap">
    <h2 class="section-title">Deuxième section</h2>
    <p id="p2">Texte de la deuxième section, avec <span id="ancre">une ancre</span>.</p>
  </div>
</section>
<section>
  <div class="wrap" data-replis-h2>
    <p id="intro">Introduction hors des groupes.</p>
    <h2 id="t3">Troisième partie</h2>
    <p id="p3">Texte trois, avec le mot zéphyrin.</p>
    <h2 id="t4">Quatrième partie</h2>
    <p id="p4">Texte quatre.</p>
  </div>
</section>
</main>
<script src="/animations.js" defer></script>
<script src="/app.js" defer></script>
</body>
</html>
```

- [ ] **Étape 2 : écrire les tests**

`tests/format-app/test_replis.py` :

```python
# -*- coding: utf-8 -*-
"""Sections repliables : fermées sur téléphone, ouvertes sans bouton sur ordinateur."""
from aide import ouvrir, source

URL = 'tests/format-app/essais/replis.html'
CORPS = ('p1', 'p2', 'p3', 'p4')
# Le <main> tel que l'ordinateur doit le voir : le HTML d'origine, intact.
MAIN = "document.querySelector('main').innerHTML"


def visible(page, id_):
    return page.evaluate(f"document.getElementById('{id_}').checkVisibility()")


def test_tout_est_replie_sur_telephone(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, URL)
    boutons = page.locator('h2 > button.repli-bouton')
    assert boutons.count() == 4
    assert [boutons.nth(i).get_attribute('aria-expanded') for i in range(4)] == ['false'] * 4
    assert not any(visible(page, p) for p in CORPS)
    assert visible(page, 'intro')
    assert not visible(page, 'e1')  # le sur-titre suit son corps
    assert erreurs == []


def test_ouvrir_puis_fermer(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    b = page.get_by_role('button', name='Première section')
    b.click()
    assert b.get_attribute('aria-expanded') == 'true' and visible(page, 'p1') and visible(page, 'e1')
    b.click()
    assert b.get_attribute('aria-expanded') == 'false' and not visible(page, 'p1')


def test_au_clavier(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    page.get_by_role('button', name='Troisième partie').focus()
    page.keyboard.press('Enter')
    assert visible(page, 'p3')


def test_tout_ouvrir(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    tout = page.locator('.replis-tout')
    assert tout.count() == 1 and tout.inner_text() == 'Tout ouvrir'
    tout.click()
    assert all(visible(page, p) for p in CORPS) and tout.inner_text() == 'Tout fermer'
    tout.click()
    assert not any(visible(page, p) for p in CORPS) and tout.inner_text() == 'Tout ouvrir'


def test_section_sombre_eclaircie_puis_rendue(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    assert 'section-sombre' not in page.get_attribute('#s2', 'class')
    page.set_viewport_size({'width': 1280, 'height': 900})
    page.wait_for_timeout(150)
    assert 'section-sombre' in page.get_attribute('#s2', 'class')


def test_un_lien_vers_une_ancre_ouvre_sa_section(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL + '#ancre')
    assert visible(page, 'ancre')
    assert page.get_by_role('button', name='Deuxième section').get_attribute('aria-expanded') == 'true'


def test_un_titre_cible_ouvre_sa_section(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL + '#t4')
    assert visible(page, 'p4')


def test_la_recherche_dans_la_page_peut_ouvrir(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    corps = page.locator('#p3').locator('xpath=..')
    assert 'repli-corps' in corps.get_attribute('class')
    assert corps.get_attribute('hidden') == 'until-found'


def test_impression(telephone, base_url):
    page, _ = ouvrir(telephone, base_url, URL)
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    assert all(visible(page, p) for p in CORPS)
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert not visible(page, 'p1')


def test_sur_ordinateur_le_html_reste_celui_d_origine(ordinateur, base_url):
    page, _ = ouvrir(ordinateur, base_url, URL)
    assert page.locator('.repli-bouton, .replis-outils, .repli-corps, .repli-groupe').count() == 0
    assert all(visible(page, p) for p in CORPS)


def test_passages_d_une_largeur_a_l_autre(telephone, ordinateur, base_url):
    reference, _ = ouvrir(ordinateur, base_url, URL)
    page, _ = ouvrir(telephone, base_url, URL)
    page.set_viewport_size({'width': 1280, 'height': 900})
    page.wait_for_timeout(150)
    assert page.evaluate(MAIN) == reference.evaluate(MAIN)
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_timeout(150)
    assert page.locator('.repli-bouton').count() == 4
    assert not visible(page, 'p3')
```

- [ ] **Étape 3 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_replis.py -q`
Attendu : échec de `test_tout_est_replie_sur_telephone` (aucun bouton).

- [ ] **Étape 4 : compléter `app.js`**

Dans `app.js`, remplacer :

```js
  window.PilotiaApp = { versResultat: versResultat };
})();
```

par :

```js
  window.PilotiaApp = { versResultat: versResultat };

  /* ───── Sections repliables (760 px ou moins).
     - [data-repli] : le premier h2 devient un bouton, ce qui le suit le corps ;
     - [data-replis-h2] : chaque h2 enfant direct ouvre un groupe repliable ;
     - [data-replis] : « Tout ouvrir / Tout fermer » dès deux replis.
     Groupes, corps et boutons n'existent que sur téléphone : au-delà de
     760 px, la page retrouve exactement son HTML d'origine. Le corps est
     masqué par hidden="until-found" quand le navigateur le connaît : la
     recherche dans la page peut alors l'ouvrir. */
  if (!document.querySelector("[data-repli], [data-replis-h2]")) return;

  var CACHE = "onbeforematch" in document.body ? "until-found" : "";
  var CHEVRON = '<svg class="repli-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" ' +
    'focusable="false"><path d="M6 9l6 6 6-6"/></svg>';
  var replis = [];
  var compteur = 0;
  function tous(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }
  // Retire des classes sans laisser d'attribut class="" vide derrière soi.
  function retirer(el) {
    el.classList.remove.apply(el.classList, Array.prototype.slice.call(arguments, 1));
    if (!el.className) el.removeAttribute("class");
  }

  function grouper() {
    tous("[data-replis-h2]").forEach(function (conteneur) {
      Array.prototype.slice.call(conteneur.children).forEach(function (enfant) {
        if (enfant.tagName !== "H2") return;
        var groupe = document.createElement("div");
        groupe.className = "repli-groupe";
        groupe.setAttribute("data-repli", "");
        conteneur.insertBefore(groupe, enfant);
        var n = enfant;
        do {
          var suivant = n.nextSibling;
          groupe.appendChild(n);
          n = suivant;
        } while (n && n.nodeName !== "H2");
      });
    });
  }

  function degrouper() {
    tous(".repli-groupe").forEach(function (groupe) {
      while (groupe.firstChild) groupe.parentNode.insertBefore(groupe.firstChild, groupe);
      groupe.parentNode.removeChild(groupe);
    });
  }

  function ouvrir(r) {
    r.corps.removeAttribute("hidden");
    r.item.classList.add("repli-ouvert");
    r.bouton.setAttribute("aria-expanded", "true");
    majTout();
  }
  function fermer(r) {
    r.corps.setAttribute("hidden", CACHE);
    r.item.classList.remove("repli-ouvert");
    r.bouton.setAttribute("aria-expanded", "false");
    majTout();
  }
  function estFerme(r) { return r.corps.hasAttribute("hidden"); }

  function envelopper(item) {
    var titre = item.querySelector("h2");
    if (!titre) return null;
    var r = { item: item, titre: titre, surtitre: null, place: null };
    r.corps = document.createElement("div");
    r.corps.className = "repli-corps";
    r.corps.id = "repli-corps-" + (++compteur);
    titre.parentNode.insertBefore(r.corps, titre.nextSibling);
    while (r.corps.nextSibling) r.corps.appendChild(r.corps.nextSibling);
    // Le sur-titre passe en tête du corps : il s'affiche à l'ouverture.
    var avant = titre.previousElementSibling;
    if (avant && avant.classList.contains("eyebrow")) {
      r.surtitre = avant;
      r.place = avant.nextSibling;
      r.corps.insertBefore(avant, r.corps.firstChild);
    }
    r.bouton = document.createElement("button");
    r.bouton.type = "button";
    r.bouton.className = "repli-bouton";
    r.bouton.setAttribute("aria-controls", r.corps.id);
    var texte = document.createElement("span");
    texte.className = "repli-texte";
    while (titre.firstChild) texte.appendChild(titre.firstChild);
    r.bouton.appendChild(texte);
    r.bouton.insertAdjacentHTML("beforeend", CHEVRON);
    titre.appendChild(r.bouton);
    titre.classList.add("repli-titre");
    r.bouton.addEventListener("click", function () {
      if (estFerme(r)) ouvrir(r); else fermer(r);
    });
    r.corps.addEventListener("beforematch", function () { ouvrir(r); });
    // Une section sombre devient une carte claire comme les autres.
    if (item.classList.contains("section-sombre")) {
      item.classList.remove("section-sombre");
      item.setAttribute("data-sombre", "");
    }
    item.classList.add("repli-actif");
    fermer(r);
    return r;
  }

  function desenvelopper(r) {
    var texte = r.bouton.firstChild;
    while (texte.firstChild) r.titre.insertBefore(texte.firstChild, r.bouton);
    r.titre.removeChild(r.bouton);
    retirer(r.titre, "repli-titre");
    if (r.surtitre) r.titre.parentNode.insertBefore(r.surtitre, r.place);
    while (r.corps.firstChild) r.corps.parentNode.insertBefore(r.corps.firstChild, r.corps);
    r.corps.parentNode.removeChild(r.corps);
    if (r.item.hasAttribute("data-sombre")) {
      r.item.classList.add("section-sombre");
      r.item.removeAttribute("data-sombre");
    }
    retirer(r.item, "repli-actif", "repli-ouvert");
  }

  function majTout() {
    tous(".replis-tout").forEach(function (b) {
      var siens = b.replisConcernes;
      var toutOuvert = siens.every(function (r) { return !estFerme(r); });
      b.textContent = toutOuvert ? "Tout fermer" : "Tout ouvrir";
    });
  }

  function ajouterBoutonsTout() {
    tous("[data-replis]").forEach(function (conteneur) {
      var siens = replis.filter(function (r) { return conteneur.contains(r.item); });
      if (siens.length < 2) return;
      var outils = document.createElement("div");
      outils.className = "replis-outils";
      var b = document.createElement("button");
      b.type = "button";
      b.className = "replis-tout";
      b.replisConcernes = siens;
      outils.appendChild(b);
      siens[0].item.parentNode.insertBefore(outils, siens[0].item);
      b.addEventListener("click", function () {
        var toutOuvert = siens.every(function (r) { return !estFerme(r); });
        siens.forEach(function (r) { if (toutOuvert) fermer(r); else ouvrir(r); });
      });
    });
    majTout();
  }

  function ouvrirCibleDuLien() {
    if (!location.hash) return;
    var cible = null;
    try { cible = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) {}
    if (!cible) return;
    var touche = false;
    replis.forEach(function (r) {
      if (r.item.contains(cible) || r.item === cible) { ouvrir(r); touche = true; }
    });
    if (touche) cible.scrollIntoView({ block: "start" });
  }

  function activer() {
    if (replis.length) return;
    grouper();
    replis = tous("[data-repli]").map(envelopper).filter(Boolean);
    ajouterBoutonsTout();
    ouvrirCibleDuLien();
  }

  function desactiver() {
    replis.forEach(desenvelopper);
    replis = [];
    tous(".replis-outils").forEach(function (o) { o.parentNode.removeChild(o); });
    degrouper();
  }

  function appliquer() { if (modeTelephone.matches) activer(); else desactiver(); }

  appliquer();
  modeTelephone.addEventListener("change", appliquer);
  window.addEventListener("hashchange", ouvrirCibleDuLien);
  // À l'impression, tout s'ouvre ; ensuite, chaque section retrouve son état.
  var fermesAvantImpression = null;
  window.addEventListener("beforeprint", function () {
    fermesAvantImpression = replis.filter(estFerme);
    replis.forEach(function (r) { r.corps.removeAttribute("hidden"); });
  });
  window.addEventListener("afterprint", function () {
    (fermesAvantImpression || []).forEach(function (r) {
      if (replis.indexOf(r) >= 0) r.corps.setAttribute("hidden", CACHE);
    });
    fermesAvantImpression = null;
  });
})();
```

- [ ] **Étape 5 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Sections repliables (app.js), sur téléphone seulement : au-delà de 760 px
   le script retire ses enveloppes et la page reste celle d'origine. */
@media (max-width:760px){
  section.repli-actif{padding:0 !important;background:none !important;border:none !important}
  section.repli-actif > .wrap{padding:0;margin:0 24px 10px;background:var(--card);border-radius:16px}
  .repli-actif:not(section){padding:0;margin:0 0 10px;background:var(--card);border-radius:16px}
  /* h2.… : passe devant « .legal-page h2 » et « .card h2 », de même poids mais plus anciennes. */
  h2.repli-titre{margin:0;max-width:none;font-family:var(--font-body);font-size:17px;font-weight:600;line-height:1.3;letter-spacing:-.01em}
  .repli-titre .mot{opacity:1;transform:none;transition:none}
  .repli-bouton{display:flex;align-items:center;justify-content:space-between;gap:12px;width:100%;min-height:56px;padding:12px 16px;background:none;border:none;border-radius:16px;color:inherit;font:inherit;text-align:left;cursor:pointer}
  .repli-chevron{flex:none;width:20px;height:20px;color:var(--ink-soft);transition:transform .2s ease}
  .repli-ouvert .repli-bouton{color:var(--accent)}
  .repli-ouvert .repli-chevron{transform:rotate(180deg);color:var(--accent)}
  .repli-corps:not([hidden]){padding:0 16px 16px}
  .repli-corps > .eyebrow{margin:2px 0 14px}
  .repli-corps .card{padding:18px;background:var(--paper-alt)}
  .repli-actif [id]{scroll-margin-top:72px}
  .replis-outils{display:flex;justify-content:flex-end;margin:0 24px 4px}
  .wrap > .replis-outils{margin:0 0 4px}
  .replis-tout{min-height:48px;padding:0 4px;background:none;border:none;color:var(--accent);font:600 14.5px var(--font-body);cursor:pointer}
}
@media (max-width:760px) and (prefers-reduced-motion: reduce){.repli-chevron{transition:none}}
```

- [ ] **Étape 6 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe. `test_passages_d_une_largeur_a_l_autre` prouve qu'après un passage par le téléphone, l'ordinateur retrouve exactement le HTML d'origine.

- [ ] **Étape 7 : commit**

```bash
git add app.js style.css tests/format-app/essais/replis.html tests/format-app/test_replis.py
git commit -q -m "Format app : sections repliables sur téléphone

data-repli, data-replis-h2 et data-replis ; titres h2 conservés avec un
bouton, corps en hidden=until-found, « Tout ouvrir », ancres, impression.
Au-delà de 760 px, le script retire ses enveloppes : HTML d'origine.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 5 : écran Services

**Fichiers :**
- Créer : `scripts/nouvelle-page.py`, `services.html`, `tests/format-app/test_services.py`
- Modifier : `style.css` (ajout en fin de fichier), `sitemap.xml`, `llms.txt`

**Interfaces :**
- Consomme : `BOITES` et `CONTRASTE` (tâche 2).
- Produit : `python3 scripts/nouvelle-page.py <nom.html> "<titre>" "<description>" < contenu` ; les classes `.hero-app`, `.section-app`, `.titre-groupe`, `.tuiles`, `.tuile`, `.tuile-icone`, `.tuile-titre`, `.tuile-texte`, `.liste-app`, `.ligne-app`, `.ligne-icone`, `.ligne-texte`, `.ligne-titre`, `.ligne-sous`, `.puces`, `.carte-pas-sur`, réutilisées par la tâche 8.

- [ ] **Étape 1 : écrire les tests**

`tests/format-app/test_services.py` :

```python
# -*- coding: utf-8 -*-
"""Écran Services (§ 4.1 de la conception)."""
import re

import pytest

from aide import RACINE, TELEPHONE, ouvrir, source
from test_coquille import BOITES, CONTRASTE

LIENS = ['entreprises.html', 'independants.html', 'facturation-electronique.html',
         'affacturage.html', 'marketing-digital.html', 'offres.html',
         'coaching-restaurant.html', 'coaching-boulangerie.html', 'coaching-coiffeur.html',
         'coaching-esthetique.html', 'coaching-agent-immobilier.html', 'diagnostic.html']


def test_les_liens_de_services():
    principal = re.search(r'<main id="contenu">(.*?)</main>', source('services.html'), re.S).group(1)
    liens = re.findall(r'href="([^"]+)"', principal)
    assert liens == LIENS
    assert all((RACINE / l).exists() for l in liens)


def test_services_reference():
    html = source('services.html')
    assert '<link rel="canonical" href="https://pilotis-murex.vercel.app/services.html">' in html
    assert '<meta property="og:url" content="https://pilotis-murex.vercel.app/services.html">' in html
    assert 'https://pilotis-murex.vercel.app/services.html' in source('sitemap.xml')
    assert 'https://pilotis-murex.vercel.app/services.html' in source('llms.txt')


def test_services_sur_telephone(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'services.html')
    assert page.locator('.onglet[aria-current="page"] .onglet-libelle').inner_text() == 'Services'
    for sel in ('.tuile', '.ligne-app', '.puces a', '.carte-pas-sur .btn'):
        for largeur, hauteur in page.evaluate(BOITES, sel):
            assert largeur >= 48 and hauteur >= 48, (sel, largeur, hauteur)
    assert erreurs == []


def test_services_en_grille_sur_ordinateur(ordinateur, base_url):
    page, _ = ouvrir(ordinateur, base_url, 'services.html')
    colonnes = page.evaluate("getComputedStyle(document.querySelector('.liste-app')).gridTemplateColumns")
    assert len(colonnes.split()) == 2


@pytest.mark.parametrize('schema', ['light', 'dark'])
def test_contrastes_de_services(schema, navigateur, base_url):
    ctx = navigateur.new_context(**TELEPHONE, color_scheme=schema)
    try:
        page, _ = ouvrir(ctx, base_url, 'services.html')
        for sel in ('.titre-groupe', '.tuile-titre', '.tuile-texte', '.ligne-titre', '.ligne-sous',
                    '.puces a', '.carte-pas-sur p', '.carte-pas-sur .btn'):
            for ratio in page.evaluate(CONTRASTE, sel):
                assert ratio >= 4.5, (sel, schema, round(ratio, 2))
    finally:
        ctx.close()
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_services.py -q`
Attendu : `FileNotFoundError` sur `services.html`.

- [ ] **Étape 3 : écrire `scripts/nouvelle-page.py`**

`scripts/nouvelle-page.py` :

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crée une page du site à partir du gabarit d'outils.html.

    python3 scripts/nouvelle-page.py services.html "Services | Pilotia" "Description" < contenu.html

Reprend l'en-tête, le pied de page et les scripts d'outils.html ; remplace le
titre, la description, l'adresse et le contenu de <main> (lu sur l'entrée
standard), et retire les marques « page active » propres à outils.html.
Lancer ensuite scripts/navigation-app.py pour la navigation."""
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://pilotis-murex.vercel.app/'


def creer(nom, titre, description, contenu):
    t = (RACINE / 'outils.html').read_text(encoding='utf-8')
    t = re.sub(r'<title>.*?</title>', lambda m: f'<title>{titre}</title>', t, count=1)
    for cle, valeur in (('name="description"', description),
                        ('property="og:description"', description),
                        ('name="twitter:description"', description),
                        ('property="og:title"', titre), ('name="twitter:title"', titre)):
        t = re.sub(rf'<meta {cle} content="[^"]*">',
                   lambda m: f'<meta {cle} content="{valeur}">', t, count=1)
    t = t.replace(SITE + 'outils.html', SITE + nom)
    t = re.sub(r'<body[^>]*>', '<body>', t, count=1)
    t = t.replace('<a href="outils.html" class="active">', '<a href="outils.html">')
    t = t.replace('class="dropdown-trigger active"', 'class="dropdown-trigger"')
    t = re.sub(r'<main id="contenu"[^>]*>.*?</main>',
               lambda m: '<main id="contenu">\n\n' + contenu.strip() + '\n\n</main>',
               t, count=1, flags=re.S)
    (RACINE / nom).write_text(t, encoding='utf-8')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    creer(sys.argv[1], sys.argv[2], sys.argv[3], sys.stdin.read())
    print(f'{sys.argv[1]} créée. Lancez maintenant : python3 scripts/navigation-app.py')
```

- [ ] **Étape 4 : créer `services.html`, puis régénérer la navigation**

```bash
python3 scripts/nouvelle-page.py services.html "Services | Pilotia" "Les services Pilotia en un coup d'œil : entreprises en activité et futurs indépendants, facture électronique Peppol, affacturage, présence digitale, offres et tarifs." <<'EOF'
<section class="hero hero-app">
  <div class="wrap">
    <h1>Services</h1>
    <p class="lead">Partez de votre situation, ou d'un service.</p>
  </div>
</section>

<section class="section-app">
  <div class="wrap">
    <h2 class="titre-groupe">Votre situation</h2>
    <ul class="tuiles">
      <li><a class="tuile svc svc-pilotage" href="entreprises.html">
        <span class="tuile-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 21V9l8-5 8 5v12"/><path d="M9 21v-6h6v6M3 21h18"/></svg></span>
        <span class="tuile-titre">Entreprise en activité</span>
        <span class="tuile-texte">Diagnostic, personnel, marges et visibilité</span>
      </a></li>
      <li><a class="tuile svc svc-independant" href="independants.html">
        <span class="tuile-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5.5 21V4M5.5 4h11.5l-2.5 4 2.5 4H5.5"/></svg></span>
        <span class="tuile-titre">Futur indépendant</span>
        <span class="tuile-texte">Démarches, visibilité, premiers clients</span>
      </a></li>
    </ul>

    <h2 class="titre-groupe">Nos services</h2>
    <ul class="liste-app">
      <li><a class="ligne-app svc svc-peppol" href="facturation-electronique.html"><span class="ligne-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M9.5 12h6M9.5 15.5h6M9.5 9h2.5"/></svg></span><span class="ligne-texte"><span class="ligne-titre">Facture électronique Peppol</span><span class="ligne-sous">Obligatoire depuis janvier 2026</span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m9 6 6 6-6 6"/></svg></a></li>
      <li><a class="ligne-app svc svc-affacturage" href="affacturage.html"><span class="ligne-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6.5 9.5h.01M17.5 14.5h.01"/></svg></span><span class="ligne-texte"><span class="ligne-titre">Affacturage</span><span class="ligne-sous">Être payé sans attendre l'échéance</span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m9 6 6 6-6 6"/></svg></a></li>
      <li><a class="ligne-app svc svc-presence" href="marketing-digital.html"><span class="ligne-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M12 21s-6.5-5.4-6.5-11a6.5 6.5 0 0 1 13 0c0 5.6-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.5"/></svg></span><span class="ligne-texte"><span class="ligne-titre">Présence digitale</span><span class="ligne-sous">Fiche Google, réseaux, avis clients</span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m9 6 6 6-6 6"/></svg></a></li>
      <li><a class="ligne-app svc svc-pilotage" href="offres.html"><span class="ligne-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3.5 12.5V4.5a1 1 0 0 1 1-1h8l8 8-9 9z"/><circle cx="8.5" cy="8.5" r="1.5"/></svg></span><span class="ligne-texte"><span class="ligne-titre">Offres et tarifs</span><span class="ligne-sous">Diagnostic, coaching, suivi mensuel</span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m9 6 6 6-6 6"/></svg></a></li>
    </ul>

    <h2 class="titre-groupe">Votre métier</h2>
    <ul class="puces">
      <li><a href="coaching-restaurant.html">Restaurant</a></li>
      <li><a href="coaching-boulangerie.html">Boulangerie</a></li>
      <li><a href="coaching-coiffeur.html">Coiffure</a></li>
      <li><a href="coaching-esthetique.html">Esthétique</a></li>
      <li><a href="coaching-agent-immobilier.html">Agent immobilier</a></li>
    </ul>

    <div class="carte-pas-sur">
      <p><strong>Pas sûr&nbsp;?</strong> Faites le diagnostic express&nbsp;: il situe votre entreprise en 3 minutes.</p>
      <a href="diagnostic.html" class="btn btn-primary">Faire le diagnostic →</a>
    </div>
  </div>
</section>
EOF
python3 scripts/navigation-app.py
```

Attendu : « services.html créée… » puis « 1 page(s) mise(s) à jour. services.html ».

- [ ] **Étape 5 : référencer la page**

Dans `sitemap.xml`, remplacer :

```xml
  <url><loc>https://pilotis-murex.vercel.app/outils.html</loc><priority>0.85</priority></url>
```

par :

```xml
  <url><loc>https://pilotis-murex.vercel.app/outils.html</loc><priority>0.85</priority></url>
  <url><loc>https://pilotis-murex.vercel.app/services.html</loc><priority>0.85</priority></url>
```

Dans `llms.txt`, remplacer :

```text
- [Entreprises](https://pilotis-murex.vercel.app/entreprises.html) : accompagnement des PME et commerces déjà en activité.
```

par :

```text
- [Entreprises](https://pilotis-murex.vercel.app/entreprises.html) : accompagnement des PME et commerces déjà en activité.
- [Services](https://pilotis-murex.vercel.app/services.html) : tous les services Pilotia, par situation (entreprise en activité, futur indépendant), par service et par métier.
```

- [ ] **Étape 6 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Écrans Services et Mon espace : tuiles, lignes à toucher, pastilles. Sur
   ordinateur, la même page en grille. */
.hero-app{padding:clamp(36px,6vw,88px) 0 clamp(16px,3vw,32px)}
.hero-app h1{font-size:clamp(32px,5vw,56px);margin-bottom:8px}
.hero-app .lead{margin-top:6px}
/* section.… : plus précis que « .hero + section », qui ajouterait un grand vide. */
section.section-app{padding:0 0 clamp(48px,7vw,96px)}
.titre-groupe{margin:22px 0 10px;font-family:var(--font-body);font-size:12.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft)}
.tuiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tuile{display:flex;flex-direction:column;gap:5px;height:100%;padding:16px 14px 18px;background:var(--card);border-radius:var(--radius);border-top:4px solid var(--svc-vif,var(--accent));color:var(--ink);text-decoration:none;font-family:var(--font-body)}
.tuile-icone{width:40px;height:40px;margin-bottom:6px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:var(--accent-soft);color:var(--accent)}
.tuile-icone svg{width:22px;height:22px}
.tuile-titre{font-size:16px;font-weight:700;line-height:1.25}
.tuile-texte{font-size:13.5px;line-height:1.4;color:var(--ink-soft)}
.liste-app{list-style:none;margin:0;padding:0;background:var(--card);border-radius:var(--radius);overflow:hidden}
.liste-app li + li{border-top:1px solid var(--line)}
.ligne-app{display:flex;align-items:center;gap:13px;min-height:64px;padding:10px 16px;color:var(--ink);text-decoration:none;font-family:var(--font-body)}
.ligne-icone{flex:none;width:40px;height:40px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:var(--accent-soft);color:var(--accent)}
.ligne-icone svg{width:21px;height:21px}
.ligne-texte{flex:1;min-width:0}
.ligne-titre{display:block;font-size:16px;font-weight:600;line-height:1.3}
.ligne-sous{display:block;margin-top:2px;font-size:13.5px;line-height:1.4;color:var(--ink-soft)}
.ligne-app > svg{flex:none;width:18px;height:18px;color:var(--ink-soft)}
.puces{list-style:none;margin:0;padding:0 0 4px;display:flex;flex-wrap:wrap;gap:8px}
.puces a{display:inline-flex;align-items:center;min-height:48px;padding:0 18px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--ink);text-decoration:none;font:600 15px var(--font-body)}
.carte-pas-sur{margin-top:28px;padding:20px;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);font-family:var(--font-body)}
.carte-pas-sur p{margin:0 0 12px}
@media (min-width:761px){
  .liste-app{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:none;border-radius:0;overflow:visible}
  .liste-app li{background:var(--card);border-radius:var(--radius)}
  .liste-app li + li{border-top:none}
  .carte-pas-sur{display:flex;align-items:center;justify-content:space-between;gap:20px}
  .carte-pas-sur p{margin:0}
}
@media (max-width:760px){
  .puces{flex-wrap:nowrap;overflow-x:auto;margin:0 -24px;padding:0 24px 6px;scrollbar-width:none}
  .puces::-webkit-scrollbar{display:none}
  .puces li{flex:none}
}
```

- [ ] **Étape 7 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe (les tests sur toutes les pages couvrent maintenant `services.html`).

- [ ] **Étape 8 : commit**

```bash
git add scripts/nouvelle-page.py services.html style.css sitemap.xml llms.txt tests/format-app/test_services.py
git commit -q -m "Format app : écran Services

Deux tuiles par situation, une ligne par service à sa couleur, les métiers
en pastilles et un renvoi vers le diagnostic ; en grille sur ordinateur.
Page créée par scripts/nouvelle-page.py, référencée dans le plan du site
et llms.txt.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 6 : sous-onglets d'Outils et listes à toucher

**Fichiers :**
- Modifier : `outils.html` (deux grilles `grid-2` et la grille `grid-fill`), `conseils.html` (grille `grid-3`), `ressources.html` (deux grilles `grid-2`), `style.css` (ajout en fin de fichier)
- Créer : `tests/format-app/test_outils.py`

**Interfaces :**
- Consomme : `.segment-cadre` et `.segment` (tâche 1), `BOITES` (tâche 2).
- Produit : la classe `.grille-liste`, une grille de cartes qui devient une liste sur téléphone (réutilisable à l'étape 2).

- [ ] **Étape 1 : écrire les tests**

`tests/format-app/test_outils.py` :

```python
# -*- coding: utf-8 -*-
"""Onglet Outils : sous-onglets et listes à toucher (§ 4.3 de la conception)."""
import pytest

from aide import ouvrir
from test_coquille import BOITES


@pytest.mark.parametrize('nom', ['outils.html', 'conseils.html', 'ressources.html'])
def test_sous_onglets_en_mode_app_seulement(nom, telephone, ordinateur, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    assert page.locator('.segment').is_visible()
    for largeur, hauteur in page.evaluate(BOITES, '.segment a'):
        assert hauteur >= 48 and largeur >= 48
    page, _ = ouvrir(ordinateur, base_url, nom)
    assert not page.locator('.segment').is_visible()


@pytest.mark.parametrize('nom,liens,documents', [('outils.html', 8, 1), ('conseils.html', 7, 0),
                                                 ('ressources.html', 0, 8)])
def test_cartes_en_lignes(nom, liens, documents, telephone, base_url):
    page, _ = ouvrir(telephone, base_url, nom)
    lignes = page.locator('.grille-liste > a.card')
    assert lignes.count() == liens
    for i in range(liens):
        assert page.evaluate('e => getComputedStyle(e).display', lignes.nth(i).element_handle()) == 'grid'
        assert lignes.nth(i).bounding_box()['height'] >= 56
    if liens:
        serre = page.evaluate("getComputedStyle(document.querySelector('.grille-liste > a.card > p')).webkitLineClamp")
        assert serre == '2'
    assert page.locator('.grille-liste > div.card').count() == documents
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_outils.py -q`
Attendu : échecs (`.segment` non visible, aucune `.grille-liste`).

- [ ] **Étape 3 : marquer les grilles**

Dans `outils.html`, remplacer les deux occurrences de :

```html
    <div class="grid grid-2" style="margin-top:24px">
```

par :

```html
    <div class="grid grid-2 grille-liste" style="margin-top:24px">
```

puis :

```html
    <div class="grid grid-fill" style="margin-top:24px">
```

par :

```html
    <div class="grid grid-fill grille-liste" style="margin-top:24px">
```

Dans `conseils.html`, remplacer :

```html
    <div class="grid grid-3">
```

par :

```html
    <div class="grid grid-3 grille-liste">
```

Dans `ressources.html`, remplacer les deux occurrences de :

```html
    <div class="grid grid-2" style="margin-top:24px">
```

par :

```html
    <div class="grid grid-2 grille-liste" style="margin-top:24px">
```

Sur `ressources.html`, chaque document garde son formulaire d'envoi par email : la ligne entière ne peut pas être un lien, elle devient une ligne compacte.

- [ ] **Étape 4 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Sous-onglets d'Outils (Outils, Conseils, Guides), en mode app. */
@media (max-width:1080px){
  .segment-cadre{display:block;padding-top:14px}
  .segment{display:grid;grid-template-columns:repeat(3,1fr);padding:3px;border-radius:12px;background:var(--paper-alt);font-family:var(--font-body)}
  .segment a{display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:10px;color:var(--ink-soft);text-decoration:none;font-size:15px;font-weight:600}
  .segment a[aria-current]{background:var(--card);color:var(--ink);box-shadow:0 1px 3px rgba(15,23,42,.14)}
  .segment-cadre + section.hero{padding-top:28px !important}
}

/* Grille de cartes qui devient une liste sur téléphone. Carte-lien : icône à
   la couleur de la page, titre, description limitée à deux lignes (le texte
   complet reste dans la page et s'affiche sur ordinateur), chevron. Carte
   avec un formulaire (guides à télécharger) : une ligne compacte. Les
   !important l'emportent sur le style="display:block" des cartes-liens. */
@media (max-width:760px){
  .grille-liste{gap:0;background:var(--card);border-radius:var(--radius);overflow:hidden}
  .grille-liste > .card{border-radius:0;border-bottom:1px solid var(--line);padding:16px}
  .grille-liste > .card:last-child{border-bottom:none}
  .grille-liste > .card h2,.grille-liste > .card h3{margin:0 0 4px;font-size:16px;line-height:1.3}
  .grille-liste > a.card{display:grid !important;grid-template-columns:40px minmax(0,1fr) 12px;column-gap:13px;align-items:start;padding:14px}
  .grille-liste > a.card > .card-icon{grid-column:1;grid-row:1 / span 3;width:40px;height:40px;margin:0;background:var(--accent-soft);color:var(--accent)}
  .grille-liste > a.card > :not(.card-icon){grid-column:2;margin:0}
  .grille-liste > a.card > p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:13.5px;line-height:1.4;color:var(--ink-soft)}
  .grille-liste > a.card > .pill{margin:0 0 5px;justify-self:start}
  .grille-liste > a.card::after{content:"";grid-column:3;grid-row:1 / span 3;align-self:center;width:8px;height:8px;border-right:2px solid var(--ink-soft);border-bottom:2px solid var(--ink-soft);transform:rotate(-45deg)}
  .grille-liste > a.card:not(:has(> .card-icon)){grid-template-columns:minmax(0,1fr) 12px}
  .grille-liste > a.card:not(:has(> .card-icon)) > *{grid-column:1}
  .grille-liste > a.card:not(:has(> .card-icon))::after{grid-column:2}
  .grille-liste > div.card > p{font-size:14px;margin-bottom:8px}
}
```

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 6 : commit**

```bash
git add outils.html conseils.html ressources.html style.css tests/format-app/test_outils.py
git commit -q -m "Format app : sous-onglets d'Outils et cartes en lignes à toucher

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 7 : données lues par Mon espace

**Fichiers :**
- Modifier : `diagnostic.html` (sauvegarde du résultat), `tresorerie.js` (six endroits)
- Créer : `tests/format-app/test_donnees.py`

**Interfaces :**
- Produit : `pilotia-diagnostic` reçoit `date` (ISO 8601) ; `pilotia-tresorerie-resume` = `{"montant": entier, "mois": "mars", "annee": 2027, "maj": ISO}`, écrit seulement si `etat.modifie` ; `etat.modifie` (booléen) est enregistré avec le plan dans `pilotia-tresorerie`.

- [ ] **Étape 1 : écrire les tests**

`tests/format-app/test_donnees.py` :

```python
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
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_donnees.py -q`
Attendu : `KeyError: 'date'` et résumé absent.

- [ ] **Étape 3 : dater le diagnostic**

Dans `diagnostic.html`, remplacer :

```html
    localStorage.setItem('pilotia-diagnostic', JSON.stringify({
      total: total,
```

par :

```html
    localStorage.setItem('pilotia-diagnostic', JSON.stringify({
      date: new Date().toISOString(),
      total: total,
```

- [ ] **Étape 4 : résumer le plan de trésorerie**

Dans `tresorerie.js`, six remplacements. Le quatrième vaut pour les deux calculs du point bas (`rendre()` et `rendreSansLignes()`).

Remplacer :

```js
  var CLE = "pilotia-tresorerie";
```

par :

```js
  var CLE = "pilotia-tresorerie";
  // Résumé lu par « Mon espace » (mon-espace.js). Écrit seulement quand la
  // personne a modifié son plan : le plan d'exemple chargé à la première
  // visite ne doit pas s'afficher comme si c'était le sien.
  var CLE_RESUME = "pilotia-tresorerie-resume";
```

Remplacer :

```js
  var etat = charger();
  var prochainId = calculerProchainId();
```

par :

```js
  var etat = charger();
  var prochainId = calculerProchainId();

  // Toute saisie ou action dans le plan le rend « modifié » (voir noterResume).
  // Exporter n'est pas modifier ; effacer repart de l'exemple.
  function marquerModifie(e) {
    var bouton = e.target.closest && e.target.closest("button");
    if (e.type === "click" && (!bouton || /^treso-(export|csv|reset)$/.test(bouton.id))) return;
    etat.modifie = true;
  }
  racine.addEventListener("input", marquerModifie, true);
  racine.addEventListener("change", marquerModifie, true);
  racine.addEventListener("click", marquerModifie, true);
```

Remplacer :

```js
  function sauver() {
    try { localStorage.setItem(CLE, JSON.stringify(etat)); } catch (e) {}
  }
```

par :

```js
  function sauver() {
    try { localStorage.setItem(CLE, JSON.stringify(etat)); } catch (e) {}
  }

  function noterResume(bas) {
    if (!etat.modifie) return;
    try {
      localStorage.setItem(CLE_RESUME, JSON.stringify({
        montant: Math.round(bas.fin),
        mois: MOIS_LONGS[bas.mois],
        annee: bas.annee,
        maj: new Date().toISOString()
      }));
    } catch (e) {}
  }
```

Remplacer les deux occurrences de :

```js
    var bas = mois[0];
    mois.forEach(function (m) { if (m.fin < bas.fin) bas = m; });
```

par :

```js
    var bas = mois[0];
    mois.forEach(function (m) { if (m.fin < bas.fin) bas = m; });
    noterResume(bas);
```

Remplacer :

```js
        etat = d;
        prochainId = calculerProchainId();
```

par :

```js
        etat = d;
        etat.modifie = true;
        prochainId = calculerProchainId();
```

Remplacer :

```js
    try { localStorage.removeItem(CLE); } catch (e) {}
```

par :

```js
    try { localStorage.removeItem(CLE); localStorage.removeItem(CLE_RESUME); } catch (e) {}
```

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 6 : commit**

```bash
git add diagnostic.html tresorerie.js tests/format-app/test_donnees.py
git commit -q -m "Format app : date du diagnostic et résumé du point bas pour Mon espace

Le résumé n'est écrit que si la personne a modifié son plan : le plan
d'exemple de la première visite ne s'affichera pas comme le sien.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 8 : écran Mon espace

**Fichiers :**
- Créer : `mon-espace.html` (par `scripts/nouvelle-page.py`), `mon-espace.js`, `tests/format-app/test_mon_espace.py`
- Modifier : `style.css` (ajout en fin de fichier), `sitemap.xml`, `llms.txt`, `tests/format-app/test_navigation_statique.py` (liens internes)

**Interfaces :**
- Consomme : `pilotia-diagnostic`, `pilotia-tresorerie-resume` (tâche 7) ; les classes `.hero-app`, `.section-app`, `.titre-groupe`, `.liste-app`, `.ligne-app`, `.ligne-texte`, `.ligne-titre`, `.ligne-sous` (tâche 5).
- Produit : `window.PilotiaMonEspace.themeLePlusFaible(themes) -> str | null` et `window.PilotiaMonEspace.outilPour(theme, aUnPlan) -> {href, titre, sous}`.

- [ ] **Étape 1 : écrire les tests, dont celui des liens internes (les deux nouvelles pages existent désormais)**

`tests/format-app/test_mon_espace.py` :

```python
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
    assert 'https://pilotis-murex.vercel.app/mon-espace.html' in source('sitemap.xml')
    assert 'https://pilotis-murex.vercel.app/mon-espace.html' in source('llms.txt')


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
```

Ajouter à la fin de `tests/format-app/test_navigation_statique.py` :

```python


@pytest.mark.parametrize('nom', PAGES)
def test_liens_internes_valides(nom):
    for href in re.findall(r'href="([^"#?:]+\.html)(?:[#?][^"]*)?"', source(nom)):
        assert (RACINE / href).exists(), href
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_mon_espace.py::test_premiere_visite tests/format-app/test_navigation_statique.py -q -k "visite or liens_internes"`
Attendu : échec : la page n'existe pas encore et la barre d'onglets pointe vers elle.

- [ ] **Étape 3 : créer `mon-espace.html`, régénérer la navigation, charger `mon-espace.js`**

```bash
python3 scripts/nouvelle-page.py mon-espace.html "Mon espace | Pilotia" "Vos résultats Pilotia sur cet appareil : dernier diagnostic express et point bas de votre plan de trésorerie. Rien n'est envoyé." <<'EOF'
<section class="hero hero-app">
  <div class="wrap">
    <h1 id="espace-titre" tabindex="-1">Mon espace</h1>
    <p class="espace-prive"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>Enregistré sur cet appareil uniquement. Rien n'est envoyé.</p>
  </div>
</section>

<section class="section-app">
  <div class="wrap">
    <div id="espace-vide">
      <p class="lead espace-intro">Vos résultats s'afficheront ici. Ils restent sur cet appareil, sans compte à créer.</p>
      <ul class="departs">
        <li class="depart svc svc-diagnostic">
          <div class="espace-tete"><span class="espace-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg></span><h2>Faire le diagnostic express</h2></div>
          <p>8 questions, 3 minutes. Votre score par thème, gratuit et visible par vous seul.</p>
          <a href="diagnostic.html" class="btn btn-primary">Commencer →</a>
        </li>
        <li class="depart svc svc-outils">
          <div class="espace-tete"><span class="espace-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3.5 19.5h17"/><path d="m5 15 4.5-4.5 3.5 3 6-6.5"/><path d="M15.5 7H19v3.5"/></svg></span><h2>Créer mon plan de trésorerie</h2></div>
          <p>Voyez votre point bas avant qu'il n'arrive.</p>
          <a href="plan-tresorerie.html" class="lien-fleche">Créer mon plan →</a>
        </li>
        <li class="depart">
          <div class="espace-tete"><span class="espace-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17M12 12.5v5M9.5 15h5"/></svg></span><h2>Premier appel gratuit</h2></div>
          <p>15 minutes pour voir ensemble où vous en êtes.</p>
          <a href="contact.html" class="lien-fleche">Réserver un créneau →</a>
        </li>
      </ul>
    </div>

    <div id="espace-resultats" hidden>
      <article class="espace-carte svc svc-diagnostic" id="carte-diagnostic" hidden>
        <div class="espace-tete"><span class="espace-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg></span><div><h2>Diagnostic express</h2><p class="espace-date" id="diag-date"></p></div></div>
        <p class="espace-score"><strong id="diag-total"></strong> / 16 <span class="pill" id="diag-libelle"></span></p>
        <ul class="espace-themes" id="diag-themes"></ul>
        <div class="espace-actions">
          <a href="diagnostic.html" class="btn btn-secondary">Refaire</a>
          <a href="rapport-diagnostic.html" class="btn btn-primary">Rapport détaillé</a>
        </div>
      </article>
      <article class="espace-carte svc svc-outils" id="carte-tresorerie" hidden>
        <div class="espace-tete"><span class="espace-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3.5 19.5h17"/><path d="m5 15 4.5-4.5 3.5 3 6-6.5"/><path d="M15.5 7H19v3.5"/></svg></span><div><h2>Plan de trésorerie</h2><p class="espace-date" id="plan-date"></p></div></div>
        <p class="espace-kpi">Point bas&nbsp;: <strong id="plan-montant"></strong> <span id="plan-mois"></span></p>
        <a href="plan-tresorerie.html" class="lien-fleche">Ouvrir mon plan →</a>
      </article>
      <h2 class="titre-groupe">Votre prochain pas</h2>
      <ul class="liste-app" id="prochain-pas"></ul>
      <button type="button" class="effacer" id="espace-effacer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 7h16M10 11v6M14 11v6M5.5 7l1 13h11l1-13M9 7V4h6v3"/></svg>Effacer les données de cet appareil</button>
    </div>
  </div>
</section>
EOF
python3 scripts/navigation-app.py
```

Attendu : « mon-espace.html créée… » puis « 1 page(s) mise(s) à jour. mon-espace.html ».

Puis, dans `mon-espace.html`, remplacer :

```html
<script src="app.js" defer></script>
```

par :

```html
<script src="app.js" defer></script>
<script src="mon-espace.js" defer></script>
```

- [ ] **Étape 4 : écrire `mon-espace.js`**

`mon-espace.js` :

```js
/* Mon espace (mon-espace.html) : affiche ce que les outils ont enregistré
   sur cet appareil. Rien n'est envoyé : tout se lit dans le stockage local.
   Sans JavaScript ou sans résultat, la page montre ses trois points de départ. */
(function () {
  "use strict";

  var CLE_DIAG = "pilotia-diagnostic";
  var CLE_PLAN = "pilotia-tresorerie";
  var CLE_RESUME = "pilotia-tresorerie-resume";
  // Ordre de priorité en cas d'égalité (conception, § 4.2).
  var THEMES = ["Trésorerie & résilience", "Finances", "Personnel & organisation", "Présence digitale"];
  var CHEVRON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
    '<path d="m9 6 6 6-6 6"/></svg>';

  function lire(cle) {
    try {
      var brut = localStorage.getItem(cle);
      return brut ? JSON.parse(brut) : null;
    } catch (e) { return null; }
  }

  function themeLePlusFaible(themes) {
    var choix = null, min = Infinity;
    THEMES.forEach(function (t) {
      if (themes && typeof themes[t] === "number" && themes[t] < min) { min = themes[t]; choix = t; }
    });
    return choix;
  }

  function outilPour(theme, aUnPlan) {
    var sous = theme + " : votre thème le plus faible";
    if (theme === "Finances") return { href: "calculateur-marge.html", titre: "Calculer votre marge", sous: sous };
    if (theme === "Personnel & organisation") return { href: "calculateur-cout-salarie.html", titre: "Calculer le coût réel d'un salarié", sous: sous };
    if (theme === "Présence digitale") return { href: "generateur-calendrier-contenu.html", titre: "Générer votre calendrier de contenu", sous: sous };
    if (theme === "Trésorerie & résilience") {
      return aUnPlan
        ? { href: "calculateur-delai-encaissement.html", titre: "Mesurer votre délai d'encaissement", sous: sous }
        : { href: "plan-tresorerie.html", titre: "Créer votre plan de trésorerie", sous: sous };
    }
    return null;
  }

  function el(tag, classe, texte) {
    var e = document.createElement(tag);
    if (classe) e.className = classe;
    if (texte !== undefined) e.textContent = texte;
    return e;
  }

  function dateCourte(iso) {
    var d = new Date(iso);
    return isNaN(d) ? "" : d.toLocaleDateString("fr-BE", { day: "numeric", month: "long" });
  }

  function euros(n) {
    return Math.round(n).toLocaleString("fr-BE").replace(/[  ]/g, " ") + " €";
  }

  function afficherDiagnostic(d) {
    var carte = document.getElementById("carte-diagnostic");
    if (!d || typeof d.total !== "number") { carte.hidden = true; return false; }
    document.getElementById("diag-total").textContent = d.total;
    document.getElementById("diag-libelle").textContent = d.pill || "";
    var date = d.date ? dateCourte(d.date) : "";
    document.getElementById("diag-date").textContent = date ? "Fait le " + date : "";
    var liste = document.getElementById("diag-themes");
    liste.textContent = "";
    Object.keys(d.themes || {}).forEach(function (t) {
      var score = d.themes[t];
      var li = el("li");
      li.appendChild(el("span", "theme-nom", t));
      li.appendChild(el("span", "theme-score", score + "/4"));
      var jauge = el("span", "jauge");
      var barre = el("span");
      barre.style.width = Math.max(0, Math.min(100, score / 4 * 100)) + "%";
      jauge.appendChild(barre);
      li.appendChild(jauge);
      liste.appendChild(li);
    });
    carte.hidden = false;
    return true;
  }

  function afficherPlan(r) {
    var carte = document.getElementById("carte-tresorerie");
    if (!r || typeof r.montant !== "number") { carte.hidden = true; return false; }
    document.getElementById("plan-montant").textContent = euros(r.montant);
    document.getElementById("plan-mois").textContent = "fin " + r.mois + (r.annee ? " " + r.annee : "");
    var date = r.maj ? dateCourte(r.maj) : "";
    document.getElementById("plan-date").textContent = date ? "Mis à jour le " + date : "";
    carte.hidden = false;
    return true;
  }

  function ligne(item) {
    var li = el("li");
    var a = el("a", "ligne-app");
    a.href = item.href;
    var txt = el("span", "ligne-texte");
    txt.appendChild(el("span", "ligne-titre", item.titre));
    txt.appendChild(el("span", "ligne-sous", item.sous));
    a.appendChild(txt);
    a.insertAdjacentHTML("beforeend", CHEVRON);
    li.appendChild(a);
    return li;
  }

  function afficherProchainPas(d, aUnPlan) {
    var liste = document.getElementById("prochain-pas");
    liste.textContent = "";
    var premier = d
      ? outilPour(themeLePlusFaible(d.themes), aUnPlan)
      : { href: "diagnostic.html", titre: "Faire le diagnostic express", sous: "8 questions, 3 minutes" };
    if (premier) liste.appendChild(ligne(premier));
    liste.appendChild(ligne({ href: "contact.html", titre: "Parler de votre situation", sous: "Appel gratuit de 15 minutes" }));
  }

  function afficher() {
    var d = lire(CLE_DIAG);
    var aDiag = afficherDiagnostic(d);
    var aPlan = afficherPlan(lire(CLE_RESUME));
    var vide = !aDiag && !aPlan;
    document.getElementById("espace-vide").hidden = !vide;
    document.getElementById("espace-resultats").hidden = vide;
    if (!vide) afficherProchainPas(aDiag ? d : null, aPlan);
  }

  document.getElementById("espace-effacer").addEventListener("click", function () {
    if (!window.confirm("Effacer de cet appareil votre diagnostic et votre plan de trésorerie ? Cette action est définitive.")) return;
    [CLE_DIAG, CLE_PLAN, CLE_RESUME].forEach(function (c) {
      try { localStorage.removeItem(c); } catch (e) {}
    });
    afficher();
    document.getElementById("espace-titre").focus();
  });

  window.PilotiaMonEspace = { themeLePlusFaible: themeLePlusFaible, outilPour: outilPour };
  afficher();
})();
```

- [ ] **Étape 5 : référencer la page**

Dans `sitemap.xml`, remplacer :

```xml
  <url><loc>https://pilotis-murex.vercel.app/services.html</loc><priority>0.85</priority></url>
```

par :

```xml
  <url><loc>https://pilotis-murex.vercel.app/services.html</loc><priority>0.85</priority></url>
  <url><loc>https://pilotis-murex.vercel.app/mon-espace.html</loc><priority>0.4</priority></url>
```

Dans `llms.txt`, remplacer :

```text
- [Services](https://pilotis-murex.vercel.app/services.html) : tous les services Pilotia, par situation (entreprise en activité, futur indépendant), par service et par métier.
```

par :

```text
- [Services](https://pilotis-murex.vercel.app/services.html) : tous les services Pilotia, par situation (entreprise en activité, futur indépendant), par service et par métier.
- [Mon espace](https://pilotis-murex.vercel.app/mon-espace.html) : les résultats du visiteur (dernier diagnostic express, point bas de son plan de trésorerie), enregistrés sur son appareil uniquement.
```

- [ ] **Étape 6 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Mon espace. */
.espace-prive{display:flex;align-items:center;gap:8px;margin:6px 0 0;font:500 14px var(--font-body);color:var(--ink-soft)}
.espace-prive svg{flex:none;width:17px;height:17px}
#espace-titre:focus{outline:none}
.espace-intro{margin-top:0}
.departs{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:12px}
.depart,.espace-carte{padding:18px;background:var(--card);border-radius:var(--radius);font-family:var(--font-body)}
.espace-tete{display:flex;align-items:center;gap:12px}
.espace-icone{flex:none;width:40px;height:40px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:var(--accent-soft);color:var(--accent)}
.espace-icone svg{width:22px;height:22px}
.depart h2,.espace-carte h2{margin:0;font-family:var(--font-body);font-size:17px;font-weight:700;letter-spacing:-.01em}
.depart p{margin:10px 0 8px;font-size:14.5px;color:var(--ink-soft)}
.espace-date{margin:2px 0 0;font-size:13px;color:var(--ink-soft)}
.espace-score{margin:14px 0 10px;font-size:15px;color:var(--ink-soft)}
.espace-score strong{margin-right:2px;font-size:36px;letter-spacing:-.02em;color:var(--ink)}
.espace-score .pill{margin:0 0 0 8px;vertical-align:8px}
.espace-themes{list-style:none;margin:0 0 6px;padding:0}
.espace-themes li{display:grid;grid-template-columns:1fr auto;gap:2px 8px;margin-bottom:8px;font-size:13.5px}
.espace-themes .jauge{grid-column:1 / -1;height:7px;border-radius:4px;background:var(--paper-alt);overflow:hidden}
.espace-themes .jauge span{display:block;height:100%;border-radius:4px;background:var(--accent)}
.espace-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}
.espace-kpi{margin:14px 0 4px;font-size:15px;color:var(--ink-soft)}
.espace-kpi strong{font-size:26px;letter-spacing:-.02em;color:var(--ink)}
.lien-fleche{display:inline-flex;align-items:center;min-height:48px;font:600 15px var(--font-body);color:var(--accent);text-decoration:none}
#espace-resultats{display:grid;gap:12px;align-items:start}
#espace-resultats[hidden]{display:none}
#espace-resultats .titre-groupe{margin-bottom:0}
.effacer{display:flex;align-items:center;justify-content:center;gap:8px;min-height:48px;margin-top:8px;background:none;border:none;color:#B91C1C;font:600 14.5px var(--font-body);cursor:pointer}
.effacer svg{width:18px;height:18px}
@media (prefers-color-scheme: dark){.effacer{color:#F87171}}
@media (min-width:761px){
  .departs{grid-template-columns:repeat(3,1fr)}
  #espace-resultats{grid-template-columns:1fr 1fr}
  #espace-resultats > .titre-groupe,#espace-resultats > .liste-app,#espace-resultats > .effacer{grid-column:1 / -1}
  #espace-resultats > .effacer{justify-self:start}
}
```

- [ ] **Étape 7 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 8 : commit**

```bash
git add mon-espace.html mon-espace.js style.css sitemap.xml llms.txt tests/format-app/test_mon_espace.py tests/format-app/test_navigation_statique.py
git commit -q -m "Format app : écran Mon espace

Dernier diagnostic (score par thème), point bas du plan de trésorerie,
prochain pas selon le thème le plus faible, effacement des données de
l'appareil. Trois points de départ à la première visite ou sans JavaScript.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 9 : pages Cookies et Confidentialité

**Fichiers :**
- Modifier : `cookies.html` (§ 2 et 3, date), `confidentialite.html` (§ 4, date), `tests/format-app/test_texte.py` (passages réécrits)
- Créer : `tests/format-app/test_vie_privee.py`

**Interfaces :**
- Consomme : `REECRITS` (tâche 0).

- [ ] **Étape 1 : écrire le test**

`tests/format-app/test_vie_privee.py` :

```python
# -*- coding: utf-8 -*-
"""Les trois clés du stockage local sont déclarées (conception, § 6)."""
import pytest

from aide import source


@pytest.mark.parametrize('nom', ['cookies.html', 'confidentialite.html'])
def test_les_trois_cles_sont_declarees(nom):
    html = source(nom)
    for cle in ('pilotia-diagnostic', 'pilotia-tresorerie', 'pilotia-tresorerie-resume'):
        assert f'<td><code>{cle}</code></td>' in html, cle
    assert 'href="mon-espace.html"' in html
    assert 'Dernière mise à jour : 20 septembre 2026' not in html
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_vie_privee.py -q`
Attendu : `AssertionError: pilotia-tresorerie`.

- [ ] **Étape 3 : mettre à jour `cookies.html`**

La date de mise à jour est celle du jour de la modification : si l'exécution a lieu après le 12 octobre 2026, écrire la date du jour (et la même dans `confidentialite.html`).

Dans `cookies.html`, remplacer :

```html
      Une seule information est conservée dans le stockage local
      (<code>localStorage</code>) de votre navigateur. Ce n&rsquo;est pas un cookie : elle n&rsquo;est
      jamais jointe aux requêtes réseau et ne quitte jamais votre appareil.
```

par :

```html
      Trois informations peuvent être conservées dans le stockage local
      (<code>localStorage</code>) de votre navigateur, jusqu&rsquo;à ce que vous les effaciez. Ce ne
      sont pas des cookies : elles ne sont jamais jointes aux requêtes réseau et ne quittent
      jamais votre appareil. La page <a href="mon-espace.html">Mon espace</a> vous les montre.
```

Remplacer :

```html
        <tr>
          <td><code>pilotia-diagnostic</code></td>
          <td>Vos réponses au diagnostic express et le score obtenu</td>
          <td>Reporter vos réponses sur la page de rapport détaillé sans vous faire tout ressaisir</td>
          <td>Non, strictement nécessaire au service que vous venez de demander</td>
        </tr>
```

par :

```html
        <tr>
          <td><code>pilotia-diagnostic</code></td>
          <td>Vos réponses au diagnostic express, le score obtenu et la date du test</td>
          <td>Reporter vos réponses sur la page de rapport détaillé sans vous faire tout ressaisir, et afficher votre score dans Mon espace</td>
          <td>Non, strictement nécessaire au service que vous venez de demander</td>
        </tr>
        <tr>
          <td><code>pilotia-tresorerie</code></td>
          <td>Votre plan de trésorerie : soldes, encaissements, décaissements et factures</td>
          <td>Retrouver votre plan d&rsquo;une visite à l&rsquo;autre</td>
          <td>Non, strictement nécessaire au service que vous venez de demander</td>
        </tr>
        <tr>
          <td><code>pilotia-tresorerie-resume</code></td>
          <td>Le point bas de votre plan (montant et mois) et sa date de mise à jour, enregistrés seulement si vous avez modifié le plan</td>
          <td>Afficher ce point bas dans Mon espace</td>
          <td>Non, strictement nécessaire au service que vous venez de demander</td>
        </tr>
```

Remplacer :

```html
      Vous pouvez la supprimer à tout moment, sans autre conséquence que l&rsquo;oubli de vos
      réponses au diagnostic :
```

par :

```html
      Le plus simple : le bouton « Effacer les données de cet appareil » de la page
      <a href="mon-espace.html">Mon espace</a> les supprime toutes les trois. Vous pouvez aussi
      les supprimer depuis votre navigateur, sans autre conséquence que l&rsquo;oubli de vos
      réponses au diagnostic et de votre plan de trésorerie :
```

Remplacer :

```html
Dernière mise à jour : 20 septembre 2026.
```

par :

```html
Dernière mise à jour : 12 octobre 2026.
```

- [ ] **Étape 4 : mettre à jour `confidentialite.html`**

Dans `confidentialite.html`, remplacer :

```html
      Le site n&rsquo;utilise aucun cookie. Il enregistre en revanche un élément dans le
      stockage local (<code>localStorage</code>) de votre navigateur :
```

par :

```html
      Le site n&rsquo;utilise aucun cookie. Il peut en revanche enregistrer trois éléments dans
      le stockage local (<code>localStorage</code>) de votre navigateur, que la page
      <a href="mon-espace.html">Mon espace</a> vous montre et permet d&rsquo;effacer :
```

Remplacer :

```html
        <tr>
          <td><code>pilotia-diagnostic</code></td>
          <td>Vos réponses au diagnostic express et votre score</td>
          <td>Reporter vos réponses sur la page de rapport sans vous faire tout ressaisir</td>
          <td>Jusqu&rsquo;à effacement par vos soins</td>
        </tr>
```

par :

```html
        <tr>
          <td><code>pilotia-diagnostic</code></td>
          <td>Vos réponses au diagnostic express, votre score et la date du test</td>
          <td>Reporter vos réponses sur la page de rapport sans vous faire tout ressaisir, et afficher votre score dans Mon espace</td>
          <td>Jusqu&rsquo;à effacement par vos soins</td>
        </tr>
        <tr>
          <td><code>pilotia-tresorerie</code></td>
          <td>Votre plan de trésorerie</td>
          <td>Retrouver votre plan d&rsquo;une visite à l&rsquo;autre</td>
          <td>Jusqu&rsquo;à effacement par vos soins</td>
        </tr>
        <tr>
          <td><code>pilotia-tresorerie-resume</code></td>
          <td>Le point bas de votre plan et sa date de mise à jour, si vous avez modifié le plan</td>
          <td>Afficher ce point bas dans Mon espace</td>
          <td>Jusqu&rsquo;à effacement par vos soins</td>
        </tr>
```

Remplacer :

```html
Dernière mise à jour : 20 septembre 2026.
```

par :

```html
Dernière mise à jour : 12 octobre 2026.
```

- [ ] **Étape 5 : déclarer les passages réécrits au garde-fou du texte**

Ces corrections de fond changent volontairement quelques phrases d'origine. Le garde-fou les accepte une par une, à l'identique, et continue de refuser toute autre perte.

Dans `tests/format-app/test_texte.py`, remplacer :

```python
# Passages réécrits volontairement (tâche 9 : le stockage local passe d'une
# clé à trois). Chacun est un morceau exact du texte d'origine.
REECRITS = {}
```

par :

```python
# Passages réécrits volontairement (tâche 9 : le stockage local passe d'une
# clé à trois). Chacun est un morceau exact du texte d'origine.
REECRITS = {
    'cookies.html': [
        'Une seule information est conservée dans le stockage local (',
        ') de votre navigateur. Ce n’est pas un cookie : elle n’est jamais jointe aux requêtes'
        ' réseau et ne quitte jamais votre appareil.',
        'Vos réponses au diagnostic express et le score obtenu',
        'Vous pouvez la supprimer à tout moment, sans autre conséquence que l’oubli de vos'
        ' réponses au diagnostic :',
        'Dernière mise à jour : 20 septembre 2026. Voir aussi la',
    ],
    'confidentialite.html': [
        'Le site n’utilise aucun cookie. Il enregistre en revanche un élément dans le stockage'
        ' local (',
        ') de votre navigateur :',
        'Vos réponses au diagnostic express et votre score',
        'Dernière mise à jour : 20 septembre 2026.',
    ],
}
```

- [ ] **Étape 6 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 7 : commit**

```bash
git add cookies.html confidentialite.html tests/format-app/test_vie_privee.py tests/format-app/test_texte.py
git commit -q -m "Format app : stockage local déclaré pour Mon espace

Les pages Cookies et Confidentialité listent les trois clés (dont
pilotia-tresorerie, déjà utilisée mais absente de la page Cookies) et
renvoient vers le bouton d'effacement de Mon espace.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 10 : pilote « page légale » (mentions légales)

**Fichiers :**
- Modifier : `mentions-legales.html` (`<main>` et le conteneur du texte)
- Créer : `tests/format-app/test_pilotes.py`

**Interfaces :**
- Consomme : `data-replis`, `data-replis-h2` (tâche 4).
- Produit : `tests/format-app/test_pilotes.py`, complété par les tâches 11 à 15.

- [ ] **Étape 1 : écrire le test**

`tests/format-app/test_pilotes.py` :

```python
# -*- coding: utf-8 -*-
"""Les six pages pilotes au format app (§ 5 de la conception)."""
import re

from playwright.sync_api import expect

from aide import ouvrir, source


def visible(page, sel):
    return page.evaluate(f"document.querySelector({sel!r}).checkVisibility()")


def test_mentions_legales(telephone, ordinateur, base_url):
    titres = len(re.findall(r'<h2 id="', source('mentions-legales.html')))
    page, erreurs = ouvrir(telephone, base_url, 'mentions-legales.html')
    assert page.locator('.repli-bouton').count() == titres == 10
    assert page.locator('.replis-tout').count() == 1
    assert visible(page, 'h1') and visible(page, '.note')
    assert not visible(page, '#hebergeur + .repli-corps p')
    page, _ = ouvrir(telephone, base_url, 'mentions-legales.html#hebergeur')
    assert visible(page, '#hebergeur + .repli-corps p')
    page, _ = ouvrir(ordinateur, base_url, 'mentions-legales.html')
    assert page.locator('.repli-bouton, .repli-groupe').count() == 0
    assert erreurs == []
```

`#hebergeur + .repli-corps` désigne le corps qui suit le titre « 5. Hébergeur » une fois les groupes créés.

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_pilotes.py -q`
Attendu : `assert 0 == 10` (aucun bouton).

- [ ] **Étape 3 : marquer la page**

Dans `mentions-legales.html`, remplacer :

```html
<main id="contenu">
```

par :

```html
<main id="contenu" data-replis>
```

et :

```html
  <div class="wrap" style="max-width:74ch">
```

par :

```html
  <div class="wrap" style="max-width:74ch" data-replis-h2>
```

- [ ] **Étape 4 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 5 : commit**

```bash
git add mentions-legales.html tests/format-app/test_pilotes.py
git commit -q -m "Format app : pilote page légale (mentions légales repliables)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 11 : pilote « page de service » (Peppol)

**Fichiers :**
- Modifier : `facturation-electronique.html` (`<main>`, haut de page, quatre sections), `style.css` (ajout en fin de fichier), `tests/format-app/test_pilotes.py` (ajout)

**Interfaces :**
- Produit : le composant `aside.essentiel[aria-labelledby] > p.essentiel-titre + ul > li > svg + span`, réutilisé par la tâche 12 et à l'étape 2.

- [ ] **Étape 1 : écrire le test**

Ajouter à la fin de `tests/format-app/test_pilotes.py` :

```python


def test_page_de_service_peppol(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'facturation-electronique.html')
    assert page.locator('.essentiel li').count() == 3
    # L'encadré vient juste avant les boutons du haut de page : « puis le bouton d'action ».
    assert page.evaluate("document.querySelector('.hero .essentiel').nextElementSibling.className") == 'btn-row'
    assert page.locator('.repli-bouton').count() == 4
    assert page.locator('.replis-tout').count() == 1
    assert visible(page, '.annonce') and visible(page, '.banner')
    assert not visible(page, '.faq details')
    page, _ = ouvrir(ordinateur, base_url, 'facturation-electronique.html')
    assert visible(page, '.essentiel') and visible(page, '.faq details')
    assert erreurs == []
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_pilotes.py -q -k peppol`
Attendu : `assert 0 == 3`.

- [ ] **Étape 3 : ajouter l'encadré et marquer les sections**

L'encadré se place juste avant les boutons du haut de page : ce sont eux qui portent l'action principale (« Me mettre en règle »), sans doublon. Ses trois points reprennent le corps de la page, pas la phrase d'introduction déjà affichée juste au-dessus.

Dans `facturation-electronique.html`, remplacer :

```html
<main id="contenu">
```

par :

```html
<main id="contenu" data-replis>
```

Remplacer :

```html
    <p class="lead">Depuis le 1<sup>er</sup> janvier 2026, une facture envoyée en PDF à une entreprise belge ne suffit plus. Pilotia vous met en règle avec Peppol, puis organise votre facturation pour que vos clients paient à l'heure. Sans jargon, et sans toucher à ce qui reste le travail de votre comptable.</p>
    <div class="btn-row">
```

par :

```html
    <p class="lead">Depuis le 1<sup>er</sup> janvier 2026, une facture envoyée en PDF à une entreprise belge ne suffit plus. Pilotia vous met en règle avec Peppol, puis organise votre facturation pour que vos clients paient à l'heure. Sans jargon, et sans toucher à ce qui reste le travail de votre comptable.</p>
    <aside class="essentiel" aria-labelledby="essentiel-titre">
      <p class="essentiel-titre" id="essentiel-titre"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8h.01"/></svg>L'essentiel</p>
      <ul>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><span>Entre entreprises, un PDF joint à un email n'est plus une facture&nbsp;: elle passe en principe par le réseau Peppol.</span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><span>L'obligation vaut dans les deux sens&nbsp;: émettre vos factures et recevoir celles de vos fournisseurs.</span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><span>Pilotia choisit l'outil avec vous, vous inscrit, puis met en place vos conditions de paiement et le suivi de vos encaissements.</span></li>
      </ul>
    </aside>
    <div class="btn-row">
```

Remplacer :

```html
<section class="section-sombre">
```

par :

```html
<section class="section-sombre" data-repli>
```

Remplacer :

```html
<section style="background:var(--paper-alt)">
  <div class="wrap">
    <div class="eyebrow">Ce que Pilotia met en place</div>
```

par :

```html
<section style="background:var(--paper-alt)" data-repli>
  <div class="wrap">
    <div class="eyebrow">Ce que Pilotia met en place</div>
```

Remplacer :

```html
<section>
  <div class="wrap">
    <div class="eyebrow">Mauvais payeurs</div>
```

par :

```html
<section data-repli>
  <div class="wrap">
    <div class="eyebrow">Mauvais payeurs</div>
```

Remplacer :

```html
<section class="faq" style="background:var(--paper-alt)">
```

par :

```html
<section class="faq" style="background:var(--paper-alt)" data-repli>
```

- [ ] **Étape 4 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Encadré « L'essentiel » (pages de service et articles) : trois points au
   plus, tirés de la page, juste avant les boutons du haut de page s'il y en
   a. Visible partout, y compris sur ordinateur. */
.essentiel{margin:26px 0 0;max-width:62ch;padding:16px 18px 14px;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--svc-vif,var(--accent));border-radius:var(--radius);font-family:var(--font-body)}
.essentiel-titre{display:flex;align-items:center;gap:7px;margin:0 0 6px;color:var(--accent);font-size:12px;font-weight:800;letter-spacing:.09em;text-transform:uppercase}
.essentiel-titre svg{flex:none;width:17px;height:17px}
.essentiel ul{list-style:none;margin:0;padding:0}
.essentiel li{display:flex;gap:9px;padding:5px 0;color:var(--ink);font-size:15px;line-height:1.45}
.essentiel li svg{flex:none;width:18px;height:18px;margin-top:2px;color:var(--accent)}
.js .hero .essentiel{animation:hero-fade-in .5s ease-out .15s both}
@media (prefers-reduced-motion: reduce){.js .hero .essentiel{animation:none}}
```

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe, y compris `test_les_nombres_de_l_essentiel_viennent_de_la_page[facturation-electronique.html]` (l'encadré ne contient aucun nombre).

- [ ] **Étape 6 : commit**

```bash
git add facturation-electronique.html style.css tests/format-app/test_pilotes.py
git commit -q -m "Format app : pilote page de service (Peppol)

Encadré « L'essentiel » en trois points tirés de la page, juste avant les
boutons du haut, puis quatre sections (dont la FAQ) repliables sur
téléphone. Rien n'est supprimé.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 12 : pilote « article » (facture impayée)

**Fichiers :**
- Modifier : `conseils-facture-impayee.html` (`<main>`, haut de page, corps de l'article, FAQ), `tests/format-app/test_pilotes.py` (ajout)

**Interfaces :**
- Consomme : `.essentiel` (tâche 11), `data-replis-h2`, `data-repli`, `data-replis` (tâche 4).

- [ ] **Étape 1 : écrire le test**

Ajouter à la fin de `tests/format-app/test_pilotes.py` :

```python


def test_article_facture_impayee(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'conseils-facture-impayee.html')
    assert page.locator('.essentiel li').count() == 3
    assert page.locator('.repli-bouton').count() == 7  # 6 parties et la FAQ
    assert page.locator('.replis-tout').count() == 1
    assert page.locator('.app-retour span').inner_text() == 'Conseils'
    page.locator('.replis-tout').click()
    assert visible(page, 'table') and visible(page, '.faq details')
    page, _ = ouvrir(ordinateur, base_url, 'conseils-facture-impayee.html')
    assert page.locator('.repli-bouton').count() == 0 and visible(page, '.essentiel')
    assert erreurs == []
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_pilotes.py -q -k impayee`
Attendu : `assert 0 == 3`.

- [ ] **Étape 3 : ajouter l'encadré et marquer l'article**

Chaque point commence par le type de client, comme les deux parties de l'article : un lecteur pressé ne prend pas une règle du professionnel pour une règle du particulier.

Dans `conseils-facture-impayee.html`, remplacer :

```html
<main id="contenu">
```

par :

```html
<main id="contenu" data-replis>
```

Remplacer :

```html
    <p class="lead">Relancer trop tard coûte cher. Relancer mal, en facturant des frais auxquels vous n'avez pas droit, coûte encore plus cher. Et les règles ne sont pas les mêmes selon que votre client est une entreprise ou un particulier.</p>
  </div>
</section>
```

par :

```html
    <p class="lead">Relancer trop tard coûte cher. Relancer mal, en facturant des frais auxquels vous n'avez pas droit, coûte encore plus cher. Et les règles ne sont pas les mêmes selon que votre client est une entreprise ou un particulier.</p>
    <aside class="essentiel" aria-labelledby="essentiel-titre">
      <p class="essentiel-titre" id="essentiel-titre"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8h.01"/></svg>L'essentiel</p>
      <ul>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><span>Client professionnel&nbsp;: facture payable à 30 jours sans accord écrit, 60 jours au maximum.</span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><span>Client professionnel en retard&nbsp;: intérêts et indemnité forfaitaire de 40&nbsp;€, dus sans mise en demeure.</span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><span>Client particulier&nbsp;: premier rappel gratuit, puis au moins 14 jours avant le moindre frais.</span></li>
      </ul>
    </aside>
  </div>
</section>
```

Remplacer :

```html
<section style="padding-top:0">
  <div class="wrap" style="max-width:70ch">
```

par :

```html
<section style="padding-top:0">
  <div class="wrap" style="max-width:70ch" data-replis-h2>
```

Remplacer :

```html
<section class="faq" style="background:var(--paper-alt)">
```

par :

```html
<section class="faq" style="background:var(--paper-alt)" data-repli>
```

- [ ] **Étape 4 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe ; 30, 60, 40 et 14 se retrouvent bien dans le corps de l'article.

- [ ] **Étape 5 : commit**

```bash
git add conseils-facture-impayee.html tests/format-app/test_pilotes.py
git commit -q -m "Format app : pilote article (facture impayée)

Encadré « L'essentiel » (30 et 60 jours, 40 €, 14 jours, tous tirés de
l'article), puis chaque partie repliable sous son titre exact.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 13 : pilote « calculateur » (marge)

**Fichiers :**
- Modifier : `calculateur-marge.html` (`<main>`, quatre champs, deux boutons, deux résultats, la carte de l'étape 2), `style.css` (ajout en fin de fichier), `tests/format-app/test_pilotes.py` (ajout)

**Interfaces :**
- Consomme : `PilotiaApp.versResultat` (tâche 3), `data-repli` (tâche 4).
- Produit : la classe `.resultat`, réutilisable par tous les calculateurs à l'étape 2.

- [ ] **Étape 1 : écrire le test**

Ajouter à la fin de `tests/format-app/test_pilotes.py` :

```python


def test_calculateur_de_marge(telephone, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'calculateur-marge.html')
    modes = page.eval_on_selector_all('input[type="number"]', 'els => els.map(e => e.inputMode)')
    assert modes == ['decimal'] * 4
    assert page.evaluate("getComputedStyle(document.getElementById('prixVente')).fontSize") == '16px'
    assert page.locator('.repli-bouton').count() == 1  # l'étape 2 est repliée
    assert not visible(page, '#fraisFixes')
    page.fill('#prixVente', '20')
    page.fill('#coutRevient', '5')
    page.get_by_role('button', name='Calculer la marge →').click()
    expect(page.locator('#margeEuro')).to_have_text('15,00 € de marge')
    assert page.get_attribute('#resultatMarge', 'aria-live') == 'polite'
    # L'écran est descendu jusqu'au résultat, au-dessus de la barre d'onglets.
    page.wait_for_function("""() => document.getElementById('resultatMarge').getBoundingClientRect().bottom
        <= document.querySelector('.onglets').getBoundingClientRect().top""", timeout=3000)
    assert erreurs == []
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_pilotes.py -q -k marge`
Attendu : `assert ['', '', '', ''] == ['decimal', 'decimal', 'decimal', 'decimal']`.

- [ ] **Étape 3 : adapter la page (les calculs ne changent pas)**

Dans `calculateur-marge.html`, remplacer :

```html
<main id="contenu">
```

par :

```html
<main id="contenu" data-replis>
```

Remplacer :

```html
<input type="number" id="prixVente" min="0" step="0.01" value="18">
```

par :

```html
<input type="number" id="prixVente" min="0" step="0.01" value="18" inputmode="decimal">
```

Remplacer :

```html
<input type="number" id="coutRevient" min="0" step="0.01" value="6">
```

par :

```html
<input type="number" id="coutRevient" min="0" step="0.01" value="6" inputmode="decimal">
```

Remplacer :

```html
          <button class="btn btn-primary" onclick="calculerMarge()" style="justify-self:start">Calculer la marge →</button>
        </form>
        <div id="resultatMarge" style="margin-top:18px">
```

par :

```html
          <button class="btn btn-primary" onclick="calculerMarge();window.PilotiaApp&&PilotiaApp.versResultat('resultatMarge')" style="justify-self:start">Calculer la marge →</button>
        </form>
        <div id="resultatMarge" class="resultat" aria-live="polite" style="margin-top:18px">
```

Remplacer :

```html
      <div class="card">
        <h2>2. Seuil de rentabilité mensuel</h2>
```

par :

```html
      <div class="card" data-repli>
        <h2>2. Seuil de rentabilité mensuel</h2>
```

Remplacer :

```html
<input type="number" id="fraisFixes" min="0" step="10" value="4500">
```

par :

```html
<input type="number" id="fraisFixes" min="0" step="10" value="4500" inputmode="decimal">
```

Remplacer :

```html
<input type="number" id="margeUnitaire" min="0" step="0.01" value="12">
```

par :

```html
<input type="number" id="margeUnitaire" min="0" step="0.01" value="12" inputmode="decimal">
```

Remplacer :

```html
          <button class="btn btn-primary" onclick="calculerSeuil()" style="justify-self:start">Calculer le seuil →</button>
        </form>
        <div id="resultatSeuil" style="margin-top:18px">
```

par :

```html
          <button class="btn btn-primary" onclick="calculerSeuil();window.PilotiaApp&&PilotiaApp.versResultat('resultatSeuil')" style="justify-self:start">Calculer le seuil →</button>
        </form>
        <div id="resultatSeuil" class="resultat" aria-live="polite" style="margin-top:18px">
```

Les attributs `onclick` existaient déjà : la politique de sécurité du site (`script-src 'self' 'unsafe-inline'`) les autorise.

- [ ] **Étape 4 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Formulaires au pouce et résultats de calcul mis en valeur (mode app).
   16 px au moins : l'iPhone ne zoome plus à la saisie. */
@media (max-width:1080px){
  input:not([type="radio"]):not([type="checkbox"]),select,textarea{font-size:16px;min-height:48px}
  .resultat{padding:14px 16px;border-radius:14px;background:var(--accent-soft);scroll-margin-top:72px;scroll-margin-bottom:calc(var(--hauteur-onglets) + 24px)}
  .resultat > p:last-child{margin-bottom:0}
}
```

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 6 : commit**

```bash
git add calculateur-marge.html style.css tests/format-app/test_pilotes.py
git commit -q -m "Format app : pilote calculateur (marge)

Clavier en chiffres avec la virgule, champs de 16 px, résultat mis en
valeur et annoncé, l'écran descend jusqu'à lui ; l'étape 2 se déplie.
Les calculs ne changent pas.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 14 : pilote « Rendez-vous » (contact)

**Fichiers :**
- Modifier : `contact.html` (`<main>` et les deux colonnes), `style.css` (ajout en fin de fichier), `tests/format-app/test_pilotes.py` (ajout)

- [ ] **Étape 1 : écrire le test**

Ajouter à la fin de `tests/format-app/test_pilotes.py` :

```python


def test_rendez_vous(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'contact.html')
    carte = page.locator('.rdv-carte')
    assert carte.is_visible()
    lien = carte.locator('a.btn')
    assert lien.get_attribute('href') == 'https://cal.com/pilotia/call'
    assert lien.get_attribute('target') == '_blank'
    assert page.locator('.duree').inner_text() == '15 min · gratuit'
    assert page.locator('.onglet-centre').get_attribute('aria-current') == 'page'
    assert not visible(page, '#contact-form')
    page.get_by_role('button', name='Ou laissez-nous un message').click()
    assert visible(page, '#contact-form')
    remplissage = page.eval_on_selector_all('#nom, #entreprise, #email', 'els => els.map(e => e.autocomplete)')
    assert remplissage == ['name', 'organization', 'email']
    page, _ = ouvrir(ordinateur, base_url, 'contact.html')
    assert visible(page, '#contact-form') and not page.locator('.duree').is_visible()
    assert erreurs == []
```

Le test vérifie aussi le remplissage automatique (`autocomplete`) du formulaire, déjà en place sur le nom, l'entreprise et l'email.

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_pilotes.py -q -k rendez`
Attendu : `.rdv-carte` introuvable.

- [ ] **Étape 3 : adapter la page**

Dans `contact.html`, remplacer :

```html
<main id="contenu">
```

par :

```html
<main id="contenu" data-replis>
```

Remplacer :

```html
      <div>
        <h2 class="section-title">Réserver un créneau</h2>
```

par :

```html
      <div class="rdv-carte">
        <p class="duree">15 min · gratuit</p>
        <h2 class="section-title">Réserver un créneau</h2>
```

Remplacer :

```html
      <div>
        <h2 class="section-title">Ou laissez-nous un message</h2>
```

par :

```html
      <div data-repli>
        <h2 class="section-title">Ou laissez-nous un message</h2>
```

- [ ] **Étape 4 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Rendez-vous (contact.html) : la réservation passe en premier. */
@media (max-width:1080px){
  .rdv-carte{padding:20px 18px;background:var(--card);border:2px solid var(--trait);border-radius:var(--radius);box-shadow:4px 4px 0 var(--trait)}
  .rdv-carte .section-title{margin-bottom:8px;font-size:22px}
  .rdv-carte .btn{width:100%}
  .duree{display:inline-flex;align-items:center;margin:0 0 10px;padding:5px 11px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font:700 12.5px var(--font-body)}
}
```

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 6 : commit**

```bash
git add contact.html style.css tests/format-app/test_pilotes.py
git commit -q -m "Format app : pilote Rendez-vous (contact)

La réservation de créneau en carte, le formulaire de message dans un repli.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 15 : pilote « accueil »

**Fichiers :**
- Modifier : `index.html` (`<body>`, accès rapides après le haut de page, avis), `style.css` (ajout en fin de fichier), `tests/format-app/test_pilotes.py` (ajout)

- [ ] **Étape 1 : écrire le test**

Ajouter à la fin de `tests/format-app/test_pilotes.py` :

```python


def test_accueil(telephone, ordinateur, base_url):
    page, erreurs = ouvrir(telephone, base_url, 'index.html')
    acces = page.eval_on_selector_all('.acces-rapide a', 'els => els.map(a => a.getAttribute("href"))')
    assert acces == ['diagnostic.html', 'plan-tresorerie.html',
                     'facturation-electronique.html', 'independants.html']
    assert page.locator('.acces-rapide').is_visible()
    assert not page.locator('.hero-accueil .btn-row').is_visible()
    for sel in ('.triangle-grid', '.path-cards', '.avis'):
        defile = page.evaluate("""s => { const e = document.querySelector(s);
            return getComputedStyle(e).overflowX === 'auto' && e.scrollWidth > e.clientWidth; }""", sel)
        assert defile, sel  # cartes à faire glisser
    page, _ = ouvrir(ordinateur, base_url, 'index.html')
    assert not page.locator('.acces-rapide').is_visible()
    assert page.locator('.hero-accueil .btn-row').is_visible()
    assert erreurs == []
```

- [ ] **Étape 2 : lancer, constater l'échec**

Commande : `python3 -m pytest tests/format-app/test_pilotes.py -q -k accueil`
Attendu : `assert [] == ['diagnostic.html', …]`.

- [ ] **Étape 3 : adapter la page**

Dans `index.html`, remplacer :

```html
<body>
```

par :

```html
<body class="page-accueil">
```

Remplacer :

```html
<section style="padding-top:0;padding-bottom:0">
```

par :

```html
<section class="acces-rapide" aria-labelledby="acces-titre">
  <div class="wrap">
    <h2 class="acces-titre" id="acces-titre">Accès rapide</h2>
    <ul class="acces-grille">
      <li><a class="acces svc svc-diagnostic" href="diagnostic.html"><span class="acces-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg></span>Diagnostic express</a></li>
      <li><a class="acces svc svc-outils" href="plan-tresorerie.html"><span class="acces-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3.5 19.5h17"/><path d="m5 15 4.5-4.5 3.5 3 6-6.5"/><path d="M15.5 7H19v3.5"/></svg></span>Plan de trésorerie</a></li>
      <li><a class="acces svc svc-peppol" href="facturation-electronique.html"><span class="acces-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M9.5 12h6M9.5 15.5h6M9.5 9h2.5"/></svg></span>Facture Peppol</a></li>
      <li><a class="acces svc svc-independant" href="independants.html"><span class="acces-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5.5 21V4M5.5 4h11.5l-2.5 4 2.5 4H5.5"/></svg></span>Devenir indépendant</a></li>
    </ul>
  </div>
</section>

<section style="padding-top:0;padding-bottom:0">
```

Remplacer :

```html
    <div class="grid avis">
```

par :

```html
    <div class="grid avis" role="region" aria-label="Avis clients" tabindex="0">
```

En mode app, les deux boutons du haut de page cèdent la place aux accès rapides (comme sur la maquette) : leurs actions restent dans « Diagnostic express » et dans le bouton central Rendez-vous. Sur ordinateur, rien ne change.

- [ ] **Étape 4 : ajouter les styles en fin de `style.css`**

Ajouter à la fin de `style.css` :

```css

/* Accueil en mode app : quatre accès rapides à la place des deux boutons du
   haut (leurs actions restent dans les accès et le bouton Rendez-vous), puis
   les piliers, les parcours et les avis en cartes à faire glisser. */
@media (max-width:1080px){
  .page-accueil .hero-accueil .btn-row{display:none}
  /* section.… : plus précis que « .hero + section ». */
  section.acces-rapide{display:block;padding:0 0 32px}
  .acces-titre{margin:0 0 12px;font-family:var(--font-body);font-size:20px;font-weight:700;letter-spacing:-.02em}
  .acces-grille{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .acces{display:flex;flex-direction:column;justify-content:space-between;gap:12px;height:100%;min-height:96px;padding:13px 12px 14px;background:var(--card);border-radius:16px;border-top:4px solid var(--svc-vif,var(--accent));color:var(--ink);text-decoration:none;font-family:var(--font-body);font-size:15px;font-weight:700;line-height:1.25}
  .acces-icone{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:var(--accent-soft);color:var(--accent)}
  .acces-icone svg{width:20px;height:20px}
}
@media (min-width:600px) and (max-width:1080px){.acces-grille{grid-template-columns:repeat(4,1fr)}}
@media (max-width:760px){
  .page-accueil .triangle-grid,.page-accueil .path-cards,.page-accueil .avis{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin-left:-24px;margin-right:-24px;padding:4px 24px 14px;scroll-padding:0 24px;scrollbar-width:none}
  .page-accueil .triangle-grid::-webkit-scrollbar,.page-accueil .path-cards::-webkit-scrollbar,.page-accueil .avis::-webkit-scrollbar{display:none}
  .page-accueil .triangle-grid > *,.page-accueil .triangle-base > *,.page-accueil .path-cards > *,.page-accueil .avis > *{flex:0 0 84%;scroll-snap-align:start}
  .page-accueil .avis:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
}
```

- [ ] **Étape 5 : lancer les tests**

Commande : `python3 -m pytest tests/format-app -q`
Attendu : tout passe.

- [ ] **Étape 6 : commit**

```bash
git add index.html style.css tests/format-app/test_pilotes.py
git commit -q -m "Format app : pilote accueil

Quatre accès rapides (diagnostic, plan de trésorerie, Peppol, devenir
indépendant), piliers, parcours et avis en cartes à faire glisser.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 16 : preuve que l'ordinateur ne bouge pas

**Fichiers :**
- Créer : `tests/format-app/test_ordinateur.py`

**Interfaces :**
- Consomme : `aide.servir`, `aide.REFERENCE`.

- [ ] **Étape 1 : écrire le test**

`tests/format-app/test_ordinateur.py` :

```python
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

CHANGEMENTS_PREVUS = {
    'facturation-electronique.html', 'conseils-facture-impayee.html',  # encadré « L'essentiel »
    'cookies.html', 'confidentialite.html',  # les trois clés du stockage local
    'services.html', 'mon-espace.html',  # pages nouvelles
}


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
```

- [ ] **Étape 2 : lancer**

Commande : `python3 -m pytest tests/format-app/test_ordinateur.py -q`
Attendu : tout passe (environ 1 min 30 : deux captures pleine page par page). Si une page diffère, le message donne la zone : comparer les deux captures (dossier `tmp_path` indiqué par pytest), retrouver la règle de la section « Format app » qui s'applique hors du mode app, la limiter à `@media (max-width:1080px)` et relancer.

- [ ] **Étape 3 : relire à l'œil les pages où un changement est prévu**

Ouvrir sur ordinateur `facturation-electronique.html` et `conseils-facture-impayee.html` (seul l'encadré « L'essentiel » est nouveau dans le haut de page), `cookies.html` et `confidentialite.html` (les trois lignes du tableau), `services.html` et `mon-espace.html` (en grille).

- [ ] **Étape 4 : commit**

```bash
git add tests/format-app/test_ordinateur.py
git commit -q -m "Format app : preuve que le rendu sur ordinateur ne change pas

Comparaison au pixel près avec le site de référence (révision 3433103),
servi depuis un arbre de travail git temporaire.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 17 : fiche de référence pour la future app et README

**Fichiers :**
- Créer : `brand/charte-app.md`
- Modifier : `README.md` (nouvelle section avant « Vocabulaire retenu »)

- [ ] **Étape 1 : écrire `brand/charte-app.md`**

`brand/charte-app.md` :

````markdown
# Charte de l'app Pilotia

Référence à reproduire à l'identique dans la future app (iOS, Android ou
web) pour que les clients retrouvent les mêmes repères que sur le site en
mode app. Conception complète : `format-app-CONCEPTION.md`. En cas d'écart,
le site fait foi et cette fiche se corrige.

## Onglets (ordre et libellés fixes)

| # | Libellé | Destination sur le site | Icône |
|---|---|---|---|
| 1 | Accueil | `index.html` | maison |
| 2 | Services | `services.html` | mallette |
| 3 | Rendez-vous | `contact.html` | calendrier avec un plus (bouton central) |
| 4 | Outils | `outils.html` (sous-onglets Outils, Conseils, Guides) | calculatrice |
| 5 | Mon espace | `mon-espace.html` | silhouette |

- Le libellé est toujours écrit sous l'icône ; jamais d'icône seule.
- Onglet actif : couleur d'accent `#0369A1` (sombre : `#4CA9E0`) et pastille
  `#E1EEF6` (sombre : `#16283D`) derrière l'icône. La barre garde ces
  couleurs de marque sur toutes les pages, y compris celles d'un service.
- Bouton central : rond de 60 px, fond d'accent, contour de 2 px et ombre
  décalée de 3 px en marine `#0F172A` (sombre : noir), surélevé de 24 px.
  Cerclé quand on est sur Rendez-vous.
- La barre se masque pendant la saisie au clavier.

## Correspondance des pages et des onglets

| Onglet | Page principale | Pages de détail (lien retour) |
|---|---|---|
| Accueil | `index.html` | aucune |
| Services | `services.html` | `entreprises`, `independants`, `facturation-electronique`, `affacturage`, `marketing-digital`, `offres`, les 5 pages `coaching-*` (« ‹ Services ») |
| Rendez-vous | `contact.html` | aucune |
| Outils | `outils.html`, `conseils.html`, `ressources.html` | `diagnostic`, `rapport-diagnostic`, les 6 `calculateur-*`, `plan-tresorerie`, `generateur-calendrier-contenu` (« ‹ Outils ») ; les 7 articles `conseils-*` (« ‹ Conseils ») |
| Mon espace | `mon-espace.html` | aucune |
| Aucun (menu « Plus ») | | `a-propos`, `methode`, `statistiques`, `parrainage`, `mentions-legales`, `confidentialite`, `cookies`, `cgv`, `accessibilite`, `404` |

## Icônes (grille de 24, trait de 2, extrémités arrondies)

```
Accueil      <path d="M3.5 10.5 12 3.5l8.5 7V20a1 1 0 0 1-1 1h-4.5v-6h-6v6H4.5a1 1 0 0 1-1-1z"/>
Services     <rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8.5 7V5.5a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2V7M3 12.5h18"/>
Rendez-vous  <rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17M12 12.5v5M9.5 15h5"/>
Outils       <rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7h7M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01M8.5 15h.01M12 15h.01M15.5 15h.01M8.5 18h.01M12 18h.01M15.5 18h.01"/>
Mon espace   <circle cx="12" cy="8.5" r="4"/><path d="M4.5 20.5c.8-3.6 3.9-6 7.5-6s6.7 2.4 7.5 6"/>
Retour       <path d="M15 5l-7 7 7 7"/>
```

## Couleurs et typographie

- Marque : marine `#0F172A`, accent `#0369A1`, fond `#F8FAFC`, cartes `#FFFFFF`.
  Mode sombre : fond `#0B1220`, cartes `#16223A`, accent `#4CA9E0`.
- Chaque service garde sa couleur (`style.css`, classes `.svc-*`) : Peppol
  `#1D4ED8`, mauvais payeurs `#C2410C`, affacturage `#157A3B`, diagnostic
  `#6D28D9`, présence digitale `#BE185D`, indépendants `#AD4F0A`, pilotage
  `#4338CA`, outils `#0F766E`.
- Police : Inter (titres en graisse 600 à 700, interlettrage resserré).
- Zones à toucher : 48 × 48 px au moins. Contraste du texte : 4,5:1 au moins.

## Comportements

- **Retour :** sur une page de détail, « ‹ Services », « ‹ Outils » ou
  « ‹ Conseils » ramène toujours à la page principale de l'onglet, jamais à
  l'historique.
- **Menu « Plus » (☰) :** panneau qui monte du bas ; Pilotia (À propos, Notre
  méthode, Statistiques, Parrainage, Instagram) et Informations (Mentions
  légales, Confidentialité, Cookies, Conditions générales, Accessibilité).
- **Pages longues :** encadré « L'essentiel » (trois points au plus, tirés de
  la page), puis sections repliables avec « Tout ouvrir ».
- **Calculateurs :** clavier en chiffres, résultat mis en valeur, l'écran
  descend jusqu'à lui.

## Mon espace, aujourd'hui et demain

- **Aujourd'hui :** les résultats enregistrés sur l'appareil (dernier
  diagnostic, point bas du plan de trésorerie), un « prochain pas » et un
  bouton d'effacement. Aucun compte.
- **Demain :** la connexion de l'espace client s'ajoute sur cet écran, au
  même endroit et sous le même onglet.
````

- [ ] **Étape 2 : ajouter une section au `README.md`**

Dans `README.md`, remplacer :

```markdown
## Vocabulaire retenu
```

par :

```markdown
## Format app (téléphone et tablette)

Sous 1 080 px de large, le site se comporte comme une app : barre d'onglets
(Accueil, Services, Rendez-vous, Outils, Mon espace), lien retour sur les
pages de détail, panneau « Plus », sections repliables sous 760 px. Sur
ordinateur, le rendu ne change pas. Conception : `brand/format-app-CONCEPTION.md` ;
fiche pour la future app : `brand/charte-app.md`.

- La navigation est écrite dans chaque page par `python3 scripts/navigation-app.py`
  (à relancer après toute création de page ; `--verifier` échoue si une page
  n'est pas à jour). Une nouvelle page se crée avec `scripts/nouvelle-page.py`.
- Comportements : `app.js` ; écran Mon espace : `mon-espace.js`.
- Tests : `pip install -q pytest`, puis `python3 -m pytest tests/format-app -q`
  (le dossier `tests` n'est pas publié, voir `.vercelignore`).

## Vocabulaire retenu
```

- [ ] **Étape 3 : vérifier l'absence de tiret long dans les ajouts**

```bash
grep -c "—" brand/charte-app.md || true
git diff README.md | grep "^+" | grep -c "—" || true
```

Attendu : `0` puis `0` (le README contient déjà des tirets longs dans ses parties anciennes ; la nouvelle section n'en ajoute aucun).

- [ ] **Étape 4 : commit**

```bash
git add brand/charte-app.md README.md
git commit -q -m "Format app : fiche de référence pour la future app et README

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyT2BSCm2kB3JFsPTGCWsC"
```

---

### Tâche 18 : vérification finale, version de test et captures

**Fichiers :**
- Aucun fichier du dépôt. La planche de captures va dans le dossier scratchpad de la session.

- [ ] **Étape 1 : tout relancer**

```bash
python3 scripts/navigation-app.py --verifier
python3 -m pytest tests/format-app -q
git status --short
```

Attendu : « Toutes les pages sont à jour. », puis `787 passed, 45 skipped` en 4 minutes environ (les 45 tests ignorés sont sans objet : pages sans encadré « L'essentiel » et pages nouvelles), et `git status` vide.

- [ ] **Étape 2 : pousser la branche**

```bash
git push -u origin format-app
```

Attendu : la branche `format-app` est à jour sur GitHub. En cas d'échec réseau, réessayer jusqu'à quatre fois en attendant 2, 4, 8 puis 16 secondes. Jamais de push sur `main`.

- [ ] **Étape 3 : vérifier la version de test Vercel**

Avec les outils Vercel :
1. `list_deployments` avec `projectId: "prj_XFj1ctOxjvJBd6JmvMjRiwAeXofI"`, `teamId: "team_AtT3RaUKe8QRHLhy3TBpwSFr"` : attendre que le déploiement de la branche `format-app` soit `READY` (relancer l'appel toutes les 30 secondes environ).
2. `web_fetch_vercel_url` sur `https://pilotia-git-format-app-nassaaxs-projects.vercel.app/services.html` : la page contient « Votre situation ».
3. Même appel sur `…/tests/format-app/essais/replis.html` : 404 (le dossier `tests` n'est pas publié).

- [ ] **Étape 4 : planche de captures pour la validation**

Écrire ce script hors du dépôt, dans le dossier scratchpad de la session : `/tmp/claude-0/-home-user-educateur-financier/621c7b44-369a-582f-ac89-46cf0640158e/scratchpad/planche_etape1.py`.

```python
# -*- coding: utf-8 -*-
"""Planche des écrans de l'étape 1, en 390 px (téléphone).

    python3 planche_etape1.py <racine du site> <sortie.png>"""
import sys

racine, sortie = sys.argv[1], sys.argv[2]
sys.path.insert(0, racine + '/tests/format-app')
from aide import CHROME, servir  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

DIAG = ('{"total":11,"pill":"Des failles ciblées","date":"2026-10-08T10:00:00.000Z","themes":'
        '{"Finances":3,"Personnel & organisation":3,"Présence digitale":3,"Trésorerie & résilience":2},"reponses":[]}')
RESUME = '{"montant":1250,"mois":"mars","annee":2027,"maj":"2026-10-10T09:00:00.000Z"}'
ECRANS = [('index.html', None, 'Accueil'), ('services.html', None, 'Services'),
          ('contact.html', None, 'Rendez-vous'), ('outils.html', 'liste', 'Outils'),
          ('mon-espace.html', 'donnees', "Mon espace (chiffres d'exemple)"),
          ('facturation-electronique.html', 'essentiel', 'Service : Peppol'),
          ('conseils-facture-impayee.html', 'replis', 'Article de conseil'),
          ('calculateur-marge.html', 'calcul', 'Calculateur de marge'),
          ('mentions-legales.html', None, 'Mentions légales'), ('index.html', 'plus', 'Menu « Plus »')]

serveur = servir(racine)
base = f'http://127.0.0.1:{serveur.server_address[1]}/'
images = []
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    for nom, mode, titre in ECRANS:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2,
                            is_mobile=True, has_touch=True, reduced_motion='reduce')
        p = ctx.new_page()
        p.goto(base + nom, wait_until='networkidle')
        if mode == 'donnees':
            p.evaluate(f"localStorage.setItem('pilotia-diagnostic', JSON.stringify({DIAG}));"
                       f"localStorage.setItem('pilotia-tresorerie-resume', JSON.stringify({RESUME}))")
            p.reload(wait_until='networkidle')
        elif mode == 'liste':
            p.evaluate("document.querySelector('.outil-vedette').scrollIntoView({block: 'start'})")
        elif mode == 'essentiel':
            p.evaluate("document.querySelector('.essentiel').scrollIntoView({block: 'start'})")
        elif mode == 'replis':
            p.evaluate("document.querySelector('.replis-outils').scrollIntoView({block: 'center'})")
        elif mode == 'calcul':
            p.fill('#prixVente', '20')
            p.fill('#coutRevient', '5')
            p.get_by_role('button', name='Calculer la marge →').click()
        elif mode == 'plus':
            p.locator('#navToggle').click()
        p.wait_for_timeout(700)
        images.append((p.screenshot(), titre))
        ctx.close()
    b.close()
serveur.shutdown()

import io  # noqa: E402
L, H, M, T = 390, 844, 36, 56
planche = Image.new('RGB', (5 * (L + M) + M, 2 * (H + T) + M), '#E9EDF3')
d = ImageDraw.Draw(planche)
police = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
for i, (png, titre) in enumerate(images):
    x, y = M + (i % 5) * (L + M), M + (i // 5) * (H + T)
    planche.paste(Image.open(io.BytesIO(png)).resize((L, H)), (x, y))
    d.text((x, y + H + 14), titre, fill='#0F172A', font=police)
planche.save(sortie)
print(sortie, planche.size)
```

```bash
python3 /tmp/claude-0/-home-user-educateur-financier/621c7b44-369a-582f-ac89-46cf0640158e/scratchpad/planche_etape1.py /home/user/pilotis /tmp/claude-0/-home-user-educateur-financier/621c7b44-369a-582f-ac89-46cf0640158e/scratchpad/app/etape1-captures.png
```

Attendu : une planche de dix écrans en 390 px (Accueil, Services, Rendez-vous, Outils, Mon espace avec des chiffres d'exemple, Peppol, article, calculateur, mentions légales, menu « Plus »). L'ouvrir et vérifier chaque écran.

- [ ] **Étape 5 : présenter l'étape 1 au fondateur**

Envoyer la planche (outil SendUserFile) avec l'adresse de test `https://pilotia-git-format-app-nassaaxs-projects.vercel.app/`, et préciser :
- ce qui est à essayer au pouce sur son téléphone : onglets, retour, ☰, Services, Mon espace après un diagnostic, replis, calculateur ;
- les choix faits en rédigeant le plan (section « Décisions prises en rédigeant ce plan ») ;
- que le site public n'a pas changé ;
- la question de la suite : valider, ou lister les retouches avant l'étape 2.
