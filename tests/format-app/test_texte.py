# -*- coding: utf-8 -*-
"""Le texte validé reste mot pour mot ; les ajouts n'inventent rien."""
import html
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
        'Dernière mise à jour : 12 octobre 2026. Voir aussi la',
    ],
    'confidentialite.html': [
        'Le site n’utilise aucun cookie. Il enregistre en revanche un élément dans le stockage'
        ' local (',
        ') de votre navigateur :',
        'Vos réponses au diagnostic express et votre score',
        'Dernière mise à jour : 20 septembre 2026.',
        'Dernière mise à jour : 16 novembre 2026.',
        'À COMPLÉTER : nom légal, siège, numéro BCE',
        'À COMPLÉTER : email de contact',
        'À VÉRIFIER : confirmer ce point dans le contrat Anthropic avant la mise en service payante',
        # Prestataires ajoutés (Cal.com, OVHcloud, Google) et rapport IA envoyé sans relecture.
        'Vercel et Anthropic sont établis aux États-Unis. Les données qui leur sont transmises le sont sur la base des garanties appropriées prévues au chapitre V du RGPD (clauses contractuelles types de la Commission européenne et/ou certification au',
        'à votre égard au sens de l’article 22 RGPD. Le contenu généré reste une analyse indicative, relue et assumée par l’éditeur, et ne remplace pas un avis professionnel.',
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
    # Accueil épuré : les deux films partent (« Prenez de la hauteur » passe
    # sur la page À propos) et seuls trois avis restent ; les deux autres
    # figurent sur leurs pages métier.
    'index.html': [
        # Ouverture aux particuliers et troisième parcours.
        'Pilotia accompagne les petites entreprises et les futurs indépendants à trouver leurs points faibles, structurer leur gestion et développer leur visibilité, avec un regard extérieur clair, chiffré et sans jargon.',
        'Deux parcours, une même exigence',
        'En 30 secondes',
        'Huit casse-têtes, un seul interlocuteur',
        "Facture Peppol, client qui paie en retard, trésorerie qui se tend, visibilité en ligne : chaque casse-tête d'entrepreneur a sa réponse. Pilotia les porte toutes.",
        'Votre navigateur ne peut pas lire cette vidéo.',
        'Télécharger le film (MP4)',
        'Le film, en texte.',
        "Un mur de huit cartes grises, chacune portant un casse-tête d'entrepreneur. Un carton annonce : « 8 casse-têtes d'entrepreneur. Pilotia les retourne. » La caméra passe ensuite de carte en carte, et chacune se retourne pour montrer sa réponse, dans une couleur différente. « Je me lance. Par où commencer ? » devient « Un cadre clair pour démarrer » (devenir indépendant). « Mes factures PDF ne comptent plus ? » devient « Mis en règle avec Peppol » (facture Peppol). « Ce client paie toujours en retard » devient « Des relances planifiées, sans gêne » (mauvais payeurs). « Payé dans 60 jours, les salaires c'est demain » devient « Payé sans attendre l'échéance » (affacturage). « Où part mon argent ? » devient « Le diagnostic, en 3 minutes » (diagnostic express). « Personne ne me trouve sur Google » devient « Une fiche Google à jour » (présence digitale). « Ma banque ne montre que le passé » devient « Mon point bas, repéré d'avance » (outils gratuits). « Seul face à mes chiffres » devient « Un point chaque mois, ensemble » (accompagnement). La caméra recule sur le mur entièrement coloré, et un dernier carton se colle : « Huit casse-têtes. Un seul interlocuteur. Premier appel gratuit. » La musique, entièrement synthétisée, ne porte aucune information.",
        'Voir les offres',
        'En 40 secondes, avec le son',
        'Prenez de la hauteur',
        'Une facture, tard le soir. Au mot « Pilotia », elle se plie en avion de papier et prend son envol. Notre façon de travailler, racontée en un film.',
        "Une voix de femme raconte, sur des images en trois dimensions. « Il est tard. La boutique est fermée, et vous êtes encore sur vos factures. » Une facture sous une lampe de bureau. « Celle-ci attend toujours d'être payée. » Un tampon rouge « En retard ». « Et celle-là doit partir par Peppol. » Un tampon bleu « Via Peppol ». « Et votre marge, vous ne la voyez plus. » Un post-it « Marge ? », puis l'image devient floue. « Et si on reprenait les commandes, ensemble ? Avec Pilotia. » La facture se soulève et se plie en avion de papier, qui décolle. « On part de vos chiffres réels. On fixe 3 à 5 priorités. Et on garde le cap, mois après mois. » L'avion survole à l'aube un paysage de documents ; des faisceaux turquoise s'allument, un trait se dessine vers l'horizon. « Factures, trésorerie, Peppol, visibilité : un seul interlocuteur. » Quatre cartes portant ces mots rejoignent l'avion. « Votre premier appel est gratuit. Prenez de la hauteur, avec Pilotia. » La traînée de l'avion dessine le logo Pilotia et l'avion devient sa flèche. La voix est synthétisée ; la musique, entièrement synthétisée, ne porte aucune information.",
        "Aide précieuse pour le démarrage de mon entreprise. On a cadré l'offre, le positionnement, la cible et le modèle de revenus. J'ai évité beaucoup d'erreurs et j'ai gagné un temps énorme. Je recommande à toute personne qui lance son activité et veut partir sur des bases solides.",
        'Farah, agent immobilier',
        "Accompagnement complet et très rassurant : diagnostic de départ, plan de lancement, puis suivi des chiffres et ajustements. J'ai apprécié la méthode, la disponibilité et la capacité à transformer des idées en actions. J'ai démarré plus vite, avec une communication plus claire et une gestion mieux structurée.",
        'Lucas, restaurateur',
    ],
    # Prise de contact par WhatsApp au lieu de l'agenda Cal.com.
    'contact.html': [
        'Parlons de votre entreprise.',
        'Réserver un créneau',
        "Choisissez directement un créneau de 15 minutes dans l'agenda, avec confirmation immédiate par email.",
        'Voir les créneaux disponibles →',
        'Ou laissez-nous un message',
    ],
    # Expérience immobilière mise en avant pour l'aide aux particuliers.
    'a-propos.html': [
        "Bachelier en comptabilité de formation, j'ai travaillé plusieurs années en fiduciaire, puis comme gestionnaire de salaires, avant une courte expérience comme agent immobilier. Ce parcours m'a mis au contact quotidien des chiffres, des obligations administratives et du fonctionnement réel des petites entreprises belges. Je connais les rouages du système entrepreneurial belge de l'intérieur.",
    ],
}

# Contact par WhatsApp activé, Peppol retiré des titres de carte, Cal.com en pause.
for _nom, _passages in {
    'contact.html': ['Laissez-nous un message',
                     'Décrivez votre situation en quelques mots : je vous réponds personnellement,'
                     ' et on fixe ensemble un appel de 15 minutes, gratuit.'],
    'index.html': ['Gestion administrative & Peppol →'],
    'entreprises.html': ['2. Gestion administrative & Peppol →'],
    'cookies.html': ['Certains liens mènent vers des sites externes : l’outil de réservation Cal.com,'
                     ' le SPF Économie, l’INASTI. Une fois sur ces sites, leurs propres politiques'
                     ' de cookies s’appliquent, sur lesquelles nous n’avons aucune maîtrise.'],
    'mentions-legales.html': ['Ce site renvoie vers des ressources tierces (SPF Économie, INASTI, guichets'
                              ' d’entreprises, outil de réservation Cal.com). Ces sites disposent de leurs'
                              ' propres politiques et l’éditeur n’exerce aucun contrôle sur leur contenu ni'
                              ' sur les données qu’ils collectent.'],
}.items():
    REECRITS.setdefault(_nom, []).extend(_passages)


# Avis clients retirés (novembre 2026) : Pilotia ouvre en janvier 2027 et aucun
# client réel ne les a donnés. Ils restent dans l'historique Git ; seuls les avis
# réels, publiés avec l'accord écrit du client, reviendront.
for _nom in ('index.html', 'coaching-agent-immobilier.html', 'coaching-boulangerie.html',
             'coaching-coiffeur.html', 'coaching-esthetique.html', 'coaching-restaurant.html'):
    _ancien = source(_nom, REFERENCE) or ''
    _avis = re.findall(r'<blockquote>(.*?)</blockquote>|<figcaption>(.*?)</figcaption>', _ancien, re.S)
    REECRITS.setdefault(_nom, []).extend(
        [html.unescape(b or f).strip() for b, f in _avis]
        + ['Ce que nos clients en pensent', 'Témoignage'])


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
                   'acces-rapide', 'duree', 'prelancement', 'prelancement-note', 'credit-site'):
        ajouts += morceaux(html, zone='body', exclure=(), seulement=classe)
    if nom in ('services.html', 'mon-espace.html'):
        ajouts += morceaux(html, exclure=())
    assert '\u2014' not in ' '.join(ajouts)  # tiret long
