# -*- coding: utf-8 -*-
"""Chaque formulaire du site prévient le fondateur par email (Brevo) :
contact, inscription à un guide et rapport diagnostic. L'alerte part vers
CONTACT_RECIPIENT ; une alerte perdue ne fait jamais échouer la demande."""
import json
import subprocess

import pytest

from aide import RACINE

# Appelle une fonction de api/ avec une fausse requête ; fetch est remplacé
# pour enregistrer les appels à Brevo (et répondre pour Claude) sans réseau.
HARNAIS = r"""
const [fichier, corps, echecAlerte] = process.argv.slice(1);
const appels = [];
global.fetch = async (url, init) => {
  const envoi = JSON.parse(init.body);
  appels.push({ url, envoi });
  if (url.includes('anthropic')) {
    const texte = '## Votre situation\nUn paragraphe.\n## Vos priorités\nUn autre.';
    return { ok: true, status: 200, json: async () => ({ content: [{ type: 'text', text: texte }] }), text: async () => '' };
  }
  const versAlerte = url.endsWith('/smtp/email') && envoi.to[0].email === 'fondateur@exemple.be';
  if (echecAlerte === '1' && versAlerte) return { ok: false, status: 500, text: async () => 'panne' };
  return { ok: true, status: url.endsWith('/contacts') ? 201 : 200, text: async () => '' };
};
const res = { statut: 0, setHeader() {}, status(s) { this.statut = s; return this; },
              json() { return this; }, send() { return this; } };
require(fichier)({ method: 'POST', body: JSON.parse(corps), headers: {} }, res).then(() => {
  console.log(JSON.stringify({ statut: res.statut, appels }));
});
"""

ENV = {'BREVO_API_KEY': 'cle-de-test', 'BREVO_SENDER_EMAIL': 'contact@exemple.be',
       'CONTACT_RECIPIENT': 'fondateur@exemple.be', 'ANTHROPIC_API_KEY': 'cle-de-test', 'PATH': '/usr/bin:/bin'}
DIAG = {'total': 11, 'reponses': [{'q': 'Trésorerie', 'r': 2}], 'themes': {'Finances': 3}}


def appeler(fonction, corps, echec_alerte=False):
    import os
    env = dict(ENV, PATH=os.environ['PATH'])
    r = subprocess.run(['node', '-e', HARNAIS, str(RACINE / 'api' / fonction), json.dumps(corps),
                        '1' if echec_alerte else '0'], capture_output=True, text=True, env=env, cwd=RACINE)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout.strip().splitlines()[-1])


def alertes(resultat):
    return [a['envoi'] for a in resultat['appels']
            if a['url'].endswith('/smtp/email') and a['envoi']['to'][0]['email'] == 'fondateur@exemple.be']


def test_contact_previent_le_fondateur():
    r = appeler('contact.js', {'nom': 'Marie', 'email': 'marie@exemple.be', 'message': 'Bonjour',
                               'consent': True, 'website': ''})
    assert r['statut'] == 200
    (alerte,) = alertes(r)
    assert alerte['subject'] == 'Contact site : Marie'
    assert alerte['replyTo']['email'] == 'marie@exemple.be'


def test_inscription_a_un_guide_previent_le_fondateur():
    r = appeler('subscribe.js', {'email': 'paul@exemple.be', 'resource': 'guide-independant-pdf'})
    assert r['statut'] == 200
    (alerte,) = alertes(r)
    assert alerte['subject'] == 'Nouvelle inscription : guide-independant-pdf'
    assert 'paul@exemple.be' in alerte['htmlContent']
    assert alerte['replyTo']['email'] == 'paul@exemple.be'


def test_rapport_diagnostic_previent_le_fondateur():
    r = appeler('generate-report.js', {'diagnostic': DIAG, 'secteur': 'Restaurant', 'taille': '1 à 5',
                                       'difficulte': 'Trésorerie', 'prenom': 'Léa', 'email': 'lea@exemple.be'})
    assert r['statut'] == 200
    (alerte,) = alertes(r)
    assert alerte['subject'] == 'Nouveau rapport diagnostic : Léa'
    for texte in ('lea@exemple.be', 'Restaurant', 'Trésorerie', '11 / 16'):
        assert texte in alerte['htmlContent'], texte


def test_un_texte_piege_n_est_pas_interprete_dans_l_alerte():
    r = appeler('subscribe.js', {'email': 'x@exemple.be', 'resource': '<img src=x onerror=alert(1)>'})
    assert '<img' not in alertes(r)[0]['htmlContent']


@pytest.mark.parametrize('fonction,corps', [
    ('subscribe.js', {'email': 'paul@exemple.be', 'resource': 'guide'}),
    ('generate-report.js', {'diagnostic': DIAG, 'secteur': 'Restaurant', 'taille': '1 à 5',
                            'difficulte': 'Trésorerie', 'prenom': 'Léa', 'email': 'lea@exemple.be'}),
])
def test_une_alerte_perdue_ne_fait_pas_echouer_la_demande(fonction, corps):
    assert appeler(fonction, corps, echec_alerte=True)['statut'] == 200
