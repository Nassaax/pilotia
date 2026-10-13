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
# Pages de l'espace client (brand/espace-client-CONCEPTION.md, § 6).
ESPACE = ('connexion.html', 'ma-fiche.html', 'conditions-espace.html')
RETOURS = {'services': ('services.html', 'Services'),
           'outils': ('outils.html', 'Outils'),
           'conseils': ('conseils.html', 'Conseils'),
           'espace': ('mon-espace.html', 'Mon espace')}
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
    if nom in ESPACE:
        return 'espace', 'espace'
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
