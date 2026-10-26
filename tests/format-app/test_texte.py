# -*- coding: utf-8 -*-
"""Le texte validé reste mot pour mot ; les ajouts n'inventent rien."""
import re

import pytest

from aide import REFERENCE, morceaux, pages_du_site, source

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
        'À COMPLÉTER : nom légal, siège, numéro BCE',
        'À COMPLÉTER : email de contact',
        'À VÉRIFIER : confirmer ce point dans le contrat Anthropic avant la mise en service payante',
    ],
    # Notes au fondateur retirées des pages (À COMPLÉTER, À VÉRIFIER, consignes de tarifs).
    'accessibilite.html': [
        'À COMPLÉTER : email de contact',
    ],
    'cgv.html': [
        'La structure juridique de Pilotia n’est pas encore immatriculée à la Banque-Carrefour des Entreprises. Les informations signalées par',
        'À COMPLÉTER',
        'doivent être renseignées dès l’immatriculation,',
        'toute prestation payante : l’article XII.6 du Code de droit économique impose que ces mentions soient accessibles de manière permanente et non équivoque.',
        'À COMPLÉTER : nom légal',
        ', dont le siège est situé',
        'À COMPLÉTER : adresse',
        ', inscrit à la Banque-Carrefour des Entreprises sous le numéro',
        'À COMPLÉTER : BE 0XXX.XXX.XXX',
        'À COMPLÉTER : email de contact',
    ],
    'mentions-legales.html': [
        'La structure juridique de Pilotia n’est pas encore immatriculée à la Banque-Carrefour des Entreprises. Les informations signalées par',
        'À COMPLÉTER',
        'doivent être renseignées dès l’immatriculation,',
        'toute prestation payante : l’article XII.6 du Code de droit économique impose que ces mentions soient accessibles de manière permanente et non équivoque.',
        'Dénomination :',
        'À COMPLÉTER : nom légal exact',
        'Forme juridique :',
        'À COMPLÉTER : personne physique (indépendant) ou société',
        'À COMPLÉTER : rue, numéro, code postal, commune',
        ', Belgique',
        'Numéro d’entreprise (BCE) :',
        'À COMPLÉTER : BE 0XXX.XXX.XXX',
        'À COMPLÉTER : email professionnel',
        'Téléphone :',
        'À COMPLÉTER : facultatif mais recommandé',
        'À COMPLÉTER : prénom et nom',
        ', en qualité de représentant légal de l’éditeur.',
    ],
    'offres.html': [
        'Appel de 15 minutes, sans engagement.',  # précisé : par téléphone ou en visio
        'Tarifs indicatifs à valider selon votre positionnement réel, vos coûts et la concurrence locale. Ils servent ici de point de départ crédible plutôt que de "sur devis" partout, qui freine souvent la prise de contact. Pensez à d\'éventuels forfaits par secteur (restauration / bâtiment / commerce) et à une politique de remise pour indépendants en lancement.',
    ],
    'statistiques.html': [
        'Chiffres collectés en septembre 2026 et sujets à mise à jour. À vérifier auprès des sources avant toute communication officielle ou commerciale.',
    ],
}


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
