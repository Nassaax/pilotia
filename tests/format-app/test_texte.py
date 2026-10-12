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
