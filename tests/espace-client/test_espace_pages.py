# -*- coding: utf-8 -*-
"""Les trois pages de l'espace client (conception, § 3.2, 3.4, 6 et 8.4)."""
import re
import subprocess

import pytest

from aide_espace import RACINE

PAGES = ['connexion.html', 'ma-fiche.html', 'conditions-espace.html']


def html(nom):
    return (RACINE / nom).read_text(encoding='utf-8')


@pytest.mark.parametrize('nom', PAGES)
def test_hors_des_moteurs_et_du_plan_du_site(nom):
    assert '<meta name="robots" content="noindex">' in html(nom)
    assert nom not in (RACINE / 'sitemap.xml').read_text(encoding='utf-8')
    assert nom not in (RACINE / 'llms.txt').read_text(encoding='utf-8')


@pytest.mark.parametrize('nom', PAGES)
def test_onglet_mon_espace_et_retour_vers_mon_espace(nom):
    t = html(nom)
    barre = re.search(r'<nav class="onglets".*?</nav>', t, re.S).group(0)
    assert '<a href="mon-espace.html" class="onglet" aria-current="true">' in barre
    assert '<a class="app-retour" href="mon-espace.html"' in t


def test_la_navigation_generee_est_a_jour():
    r = subprocess.run(['python3', 'scripts/navigation-app.py', '--verifier'], cwd=RACINE,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


@pytest.mark.parametrize('nom', ['connexion.html', 'ma-fiche.html'])
def test_sans_javascript_un_message_clair(nom):
    assert ('<noscript><p class="lead">Activez JavaScript pour utiliser votre espace client. '
            'Les outils gratuits fonctionnent sans.</p></noscript>') in html(nom)


def test_connexion_les_trois_etapes_sont_en_place():
    t = html('connexion.html')
    for i in ('connexion-ferme', 'etape-email', 'connexion-email', 'etape-code', 'connexion-code',
              'code-renvoyer', 'etape-bienvenue', 'bienvenue-prenom', 'bienvenue-import',
              'bienvenue-conditions'):
        assert f'id="{i}"' in t, i
    assert 'autocomplete="one-time-code"' in t and 'inputmode="numeric"' in t
    assert 'class="hp-field" aria-hidden="true"' in t  # champ leurre, comme le formulaire de contact
    assert '<a href="conditions-espace.html">conditions d\'utilisation</a>' in t


def test_fiche_les_champs_et_les_valeurs_de_la_conception():
    t = html('ma-fiche.html')
    for nom in ('prenom', 'entreprise', 'secteur', 'statut', 'tva', 'chiffreAffaires', 'fraisFixes', 'salaries'):
        assert f'name="{nom}"' in t, nom
    for valeur in ('restaurant', 'boulangerie', 'coiffure', 'esthetique', 'immobilier', 'batiment',
                   'commerce', 'services', 'autre', 'principal', 'complementaire', 'societe', 'projet',
                   'assujetti', 'franchise', 'inconnu'):
        assert f'value="{valeur}"' in t, valeur
    for aide in ('Pré-remplit le calculateur de cotisations.',
                 'Pré-remplit la vérification de la franchise TVA.',
                 'Pré-remplit le calculateur de marge, et le taux horaire (× 12).'):
        assert aide in t


def test_les_conditions_reprennent_le_texte_valide():
    t = html('conditions-espace.html')
    for titre in ('1. Objet', '2. Accès', '3. Connexion', '4. Vos données', '5. Nature des outils',
                  '6. Disponibilité', '7. Durée et suppression', '8. Responsabilité',
                  '9. Modification des conditions', '10. Droit applicable et litiges'):
        assert f'>{titre}</h2>' in t, titre
    assert 'À COMPLÉTER' in t and 'mediationconsommateur.be' in t
    assert 'ne remplacent pas l&rsquo;avis d&rsquo;un' in t


@pytest.mark.parametrize('nom', PAGES)
def test_aucun_tiret_long(nom):
    principal = re.search(r'<main.*?</main>', html(nom), re.S).group(0)
    assert '—' not in principal
