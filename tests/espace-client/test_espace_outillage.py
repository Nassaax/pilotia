# -*- coding: utf-8 -*-
"""L'outillage de test et la publication du dossier brand/ (conception, § 9)."""
import fnmatch

from aide_espace import RACINE


def test_le_serveur_sert_le_site_avec_les_en_tetes_de_vercel(client):
    r = client.get('/index.html')
    assert r.statut == 200 and '<title>' in r.texte
    assert r.entete('Content-Security-Policy') and "connect-src 'self'" in r.entete('Content-Security-Policy')[0]
    assert client.get('/page-qui-n-existe-pas.html').statut == 404


def test_les_emails_sont_interceptes_et_la_base_repond(serveur):
    assert serveur.courriels() == []
    assert serveur.sql('select 40 + 2 as n') == [{'n': 42}]


def test_une_fonction_inconnue_repond_404(client):
    assert client.get('/api/fonction-inconnue').statut == 404


def _publie(chemin):
    """Vrai si .vercelignore laisse publier ce chemin (règles simples du fichier)."""
    regles = [l.strip() for l in (RACINE / '.vercelignore').read_text(encoding='utf-8').splitlines()
              if l.strip() and not l.startswith('#')]
    for r in regles:
        if fnmatch.fnmatch(chemin, r) or chemin == r or chemin.startswith(r.rstrip('/') + '/'):
            return False
    return True


def test_les_documents_de_travail_de_brand_ne_sont_pas_publies():
    assert not _publie('brand/espace-client-CONCEPTION.md')
    assert not _publie('brand/format-app-PLAN-etape1.md')
    assert not _publie('brand/espace-client/maquette-e1-connexion.jpg')
    assert not _publie('brand/format-app/maquette-1-navigation.jpg')
    assert not _publie('tests/espace-client/serveur.js')


def test_l_avatar_de_la_page_a_propos_reste_publie():
    assert 'brand/avatar-pilotia.svg' in (RACINE / 'a-propos.html').read_text(encoding='utf-8')
    assert _publie('brand/avatar-pilotia.svg')
