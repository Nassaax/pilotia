# -*- coding: utf-8 -*-
"""Voix off du film n° 6 « Prenez de la hauteur » (film-avion.html).

Synthèse : Kokoro v1.0 (ONNX, licence Apache 2.0), voix française « ff_siwis ».
Modèles (non versionnés, à télécharger) : kokoro-v1.0.onnx et voices-v1.0.bin
(github.com/thewh1teagle/kokoro-onnx, release model-files-v1.0), placés dans V.
kokoro-durees.onnx = le même modèle, avec la sortie interne « /encoder/Round »
exposée : la durée de chaque phonème (600 échantillons par unité, à 24 kHz).
C'est ce qui donne l'instant EXACT de chaque mot, écrit dans film-avion-voix.json.

Usage : python3 film-avion-voix.py   (écrit voix.wav et voix.json)
"""
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
import onnxruntime as ort
DUR = ort.InferenceSession('../voix/kokoro-durees.onnx')

def dire(texte, vit):
    """Synthèse + instant exact de début de chaque mot (durées lues dans le modèle :
    600 échantillons par unité de durée, mesuré)."""
    # « p:… » = phonèmes imposés (prononciations corrigées après test de compréhension)
    ph = texte[2:] if texte.startswith('p:') else k.tokenizer.phonemize(texte, 'fr-fr'); tok = k.tokenizer.tokenize(ph)
    assert len(tok) == len(ph), (texte, ph)        # un jeton par caractère phonétique
    st = k.get_voice_style('ff_siwis')[len(tok)]
    a, d = DUR.run(None, {'tokens': np.array([[0, *tok, 0]], np.int64), 'style': st.reshape(1, 256).astype(np.float32),
                          'speed': np.array([vit], np.float32)})
    d = np.asarray(d).ravel(); assert len(d) == len(tok) + 2 and abs(d.sum() * 600 - len(a)) < 2
    debut = np.concatenate([[0], np.cumsum(d)])[:-1] * 600 / SR      # début de chaque jeton (s)
    mots, i = [], 0
    for m in ph.split(' '):
        if m.strip(' .,?!:;'): mots.append([m, float(debut[1 + i])])
        i += len(m) + 1
    return np.asarray(a, np.float32), mots
V = '../voix/'
k = Kokoro(V + "kokoro-v1.0.onnx", V + "voices-v1.0.bin")
SR = 24000
# (identifiant, texte prononcé, texte affiché, silence AVANT la phrase en s, vitesse)
SCRIPT = [
  ('tard',     "Il est tard.",                                         "Il est tard.",                                   0.9, 0.92),
  ('boutique', "La boutique est fermée, et vous êtes encore sur vos factures.", "La boutique est fermée, et vous êtes encore sur vos factures.", 0.35, 0.95),
  ('impaye',   "Celle-ci attend toujours d'être payée.",               "Celle-ci attend toujours d'être payée.",         0.55, 0.95),
  ('peppol',   "Et celle-là doit partir par Pèppol.",                  "Et celle-là doit partir par Peppol.",            0.45, 0.95),
  ('marge',    "Et votre marge, vous ne la voyez plus.",               "Et votre marge, vous ne la voyez plus.",         0.5, 0.9),
  ('commandes',"Et si on reprenait les commandes, ensemble ?",         "Et si on reprenait les commandes, ensemble ?",   0.9, 0.92),
  ('pilotia',  "p:avɛk pilotiˈa.",                                     "Avec Pilotia.",                                  1.0, 0.88),
  ('chiffres', "On part de vos chiffres réels.",                       "On part de vos chiffres réels.",                 2.6, 0.97),
  ('priorites',"On fixe trois à cinq priorités.",                      "On fixe 3 à 5 priorités.",                       0.3, 0.97),
  ('cap',      "Et on garde le cap, mois après mois.",                 "Et on garde le cap, mois après mois.",           0.3, 0.95),
  ('services', "p:faktˈyʁ, tʁezoʁʁˈi, pɛpˈɔl, vizibilitˈe : ɛ̃ sˈœl ɛ̃tɛʁlokytˈœʁ.", "Factures, trésorerie, Peppol, visibilité : un seul interlocuteur.", 0.6, 0.97),
  ('appel',    "Votre premier appel est gratuit.",                     "Votre premier appel est gratuit.",               0.7, 0.95),
  ('hauteur',  "p:pʁənˈe də la otˈœʁ, avɛk pilotiˈa.",                "Prenez de la hauteur, avec Pilotia.",            0.45, 0.88),
]
FIN = 2.4   # queue après le dernier mot (logo, accord final)
morceaux, meta, t = [], [], 0.0
for cle, dit, affiche, avant, vit in SCRIPT:
    x, mots = dire(dit, vit)
    # rogner le silence du moteur en début et fin (seuil −45 dBFS), garder 20 ms
    e = np.abs(x) > 10 ** (-45 / 20); i0, i1 = np.argmax(e), len(x) - np.argmax(e[::-1])
    c0 = max(0, i0 - int(.02 * SR)); x = x[c0: min(len(x), i1 + int(.06 * SR))]
    sf.write(f'seg-{cle}.wav', x, SR)
    t += avant
    morceaux.append((t, x))
    meta.append({'id': cle, 'texte': affiche, 'debut': round(t, 3), 'fin': round(t + len(x) / SR, 3),
                 'mots': [[w, round(t + ts - c0 / SR, 3)] for w, ts in mots]})
    t += len(x) / SR
DUREE = t + FIN
y = np.zeros(int(DUREE * SR) + 1, np.float32)
for t0, x in morceaux: i = int(round(t0 * SR)); y[i:i + len(x)] += x
sf.write('voix.wav', y, SR)
json.dump({'duree': round(DUREE, 3), 'phrases': meta}, open('voix.json', 'w'), ensure_ascii=False, indent=1)
for m in meta: print(f"{m['debut']:6.2f}-{m['fin']:6.2f} {m['id']:10s} " + ' '.join(f"{w}@{ts:.2f}" for w, ts in m['mots']))
print('durée', round(DUREE, 2))
