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
SITE = 'https://www.pilotia.be/'


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
