# -*- coding: utf-8 -*-
"""Bande-son du film « Le mur » (film-services.html).

Entièrement synthétisée : aucun échantillon tiers, donc aucune licence à
déclarer ni revendication possible sur les réseaux.

La grille des bruitages n'est PAS retapée ici : elle est lue dans le film
(window.FILM.sons), exportée en JSON par le script de rendu. Image et son
viennent de la même source, ils ne peuvent pas diverger.

Usage : python3 score-services.py <grille.json> <sortie.wav>

Musique : 80 bpm, fa majeur, une mesure par carte (fa, ré mineur, si bémol,
do). Timbre pincé façon marimba, basse ronde, charleston léger. Un
demi-temps de silence musical juste avant la marque, puis l'accord final.

Le volume est de l'arithmétique : chaque élément est normalisé à une crête
connue AVANT le mélange ; le master est ensuite mesuré sur le fichier livré
(cible -14 LUFS, crête vraie <= -1 dBTP).
"""
import sys, json, wave
import numpy as np

SR = 48000
G = json.load(open(sys.argv[1], encoding='utf-8'))
SORTIE = sys.argv[2]

DUREE = G['duree']                  # même durée que l'image : le fondu final n'est pas coupé
N = int(SR * DUREE)
TEMPS = 60 / G['bpm']
MESURE = 4 * TEMPS
rng = np.random.default_rng(20260928)   # graine fixe : rendu reproductible
BRUIT = rng.standard_normal(N + SR)


def note(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def poser(piste, t0, son, gain=1.0):
    i = int(round(t0 * SR))
    if i >= N:
        return
    fin = min(N, i + len(son))
    piste[i:fin] += gain * son[:fin - i]


def normaliser(x, crete):
    m = np.max(np.abs(x))
    return x * (crete / m) if m > 0 else x


def pince(f, duree=0.5, decay=9.0):
    t = np.arange(int(SR * duree)) / SR
    env = np.exp(-decay * t) * np.minimum(1, t / 0.003)
    s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-14 * t) \
        + 0.18 * np.sin(2 * np.pi * 4.02 * f * t) * np.exp(-30 * t)
    return s * env


def basse(f, duree=0.9):
    t = np.arange(int(SR * duree)) / SR
    env = np.exp(-3.2 * t) * np.minimum(1, t / 0.008)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * env


def grosse_caisse():
    t = np.arange(int(SR * 0.28)) / SR
    f = 48 + 90 * np.exp(-28 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-11 * t)


def charley(i0=0):
    n = int(SR * 0.045)
    b = BRUIT[i0:i0 + n].copy()
    b = np.diff(b, prepend=0)                     # passe-haut grossier
    return b * np.exp(-np.arange(n) / SR * 90)


def claquement(i0=0):
    n = int(SR * 0.12)
    b = BRUIT[i0:i0 + n] * np.exp(-np.arange(n) / SR * 34)
    return np.diff(b, prepend=0)


def souffle(duree, i0=0, montee=0.7):
    """Bruit filtré dont l'enveloppe monte puis retombe : le passage d'une carte."""
    n = int(SR * duree)
    b = BRUIT[i0:i0 + n].copy()
    # filtre passe-bas à fréquence de coupure croissante (moyenne glissante variable)
    k = np.linspace(40, 6, n).astype(int)
    c = np.cumsum(np.concatenate([[0], b]))
    idx = np.arange(n)
    lo = np.maximum(0, idx - k)
    b = (c[idx + 1] - c[lo]) / np.maximum(1, idx + 1 - lo)
    t = np.linspace(0, 1, n)
    env = np.where(t < montee, t / montee, (1 - t) / (1 - montee)) ** 1.6
    return b * env


def pop(f0, f1, duree=0.09):
    t = np.arange(int(SR * duree)) / SR
    f = f1 + (f0 - f1) * np.exp(-40 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-38 * t)


# ── Musique ────────────────────────────────────────────────────────────────
ACCORDS = [(53, [65, 69, 72, 77]),          # fa
           (50, [62, 65, 69, 74]),          # ré mineur
           (46, [58, 62, 65, 70]),          # si bémol
           (48, [60, 64, 67, 72])]          # do
MOTIF = [0, 1, 2, 3, 2, 1, 2, 3, 0, 2, 1, 3, 2, 1, 3, 2]   # arpège en doubles croches

musique = np.zeros(N)
batterie = np.zeros(N)
silence_de, silence_a = G['slap'] - TEMPS * 0.75, G['slap']   # le souffle avant la marque

nb_mesures = int(np.ceil(G['slap'] / MESURE))
for m in range(nb_mesures):
    racine, notes = ACCORDS[m % 4]
    t0 = m * MESURE
    for i, n in enumerate(MOTIF):
        t = t0 + i * TEMPS / 4
        if t >= silence_de:
            break
        accent = 1.0 if i % 4 == 0 else 0.62
        poser(musique, t, pince(note(notes[n] + (12 if i >= 8 and m % 2 else 0))), 0.55 * accent)
    for b in (0, 2):
        t = t0 + b * TEMPS
        if t < silence_de:
            poser(musique, t, basse(note(racine - 12)), 1.0)
            poser(batterie, t, grosse_caisse(), 1.0)
    for b in (1, 3):
        t = t0 + b * TEMPS
        if t < silence_de and m > 0:
            poser(batterie, t, claquement(int(t * SR) % SR), 0.35)
    for c in range(8):
        t = t0 + c * TEMPS / 2
        if t < silence_de and m > 0:
            poser(batterie, t, charley(int(t * 997) % SR), 0.22 if c % 2 else 0.12)

# Accord final : fa majeur plein, sur la marque, avec une pluie de notes aiguës.
fin = G['slap']
for f in [41, 53, 60, 65, 69, 72, 77]:
    poser(musique, fin, pince(note(f), duree=3.6, decay=1.1), 0.5)
poser(musique, fin, basse(note(41), duree=3.0), 1.4)
poser(batterie, fin, grosse_caisse(), 1.6)
for i, f in enumerate([89, 84, 81, 77, 72]):
    poser(musique, fin + 0.09 * (i + 1), pince(note(f), duree=0.6, decay=7), 0.28)

# ── Bruitages ──────────────────────────────────────────────────────────────
sfx = np.zeros(N)
for k, t in enumerate(G['trajets']):
    poser(sfx, t, souffle(0.42, int(t * SR) % SR), 0.9)           # la caméra glisse
for t in G['poses']:
    poser(sfx, t - 0.16, souffle(0.2, int(t * 1301) % SR, montee=0.85), 0.8)
    poser(sfx, t, pop(820, 260, 0.11), 1.0)                        # la carte se pose
for t in G['etiquettes']:
    poser(sfx, t, pop(1500, 900, 0.07), 0.55)                      # l'étiquette se colle
for t in G['cartons']:
    poser(sfx, t, pop(700, 220, 0.12), 0.9)
poser(sfx, G['recul'], souffle(0.9, 777, montee=0.55), 1.0)       # recul sur le mur
poser(sfx, fin, pop(520, 120, 0.2), 1.3)                           # la marque se colle

# ── Mélange : chaque piste à une crête connue avant la somme ─────────────
musique = normaliser(musique, 0.55)
batterie = normaliser(batterie, 0.42)
sfx = normaliser(sfx, 0.5)
mix = musique + batterie + sfx

# Fondu de sortie sur la dernière demi-seconde, après la tenue de l'accord.
f = int(0.5 * SR)
mix[-f:] *= np.linspace(1, 0, f)
mix = normaliser(mix, 0.89)
# Saturation douce : les bruitages sont des pics très courts qui imposaient au
# limiteur de tout baisser (v1 : -14,7 LUFS et +0,1 dBFS de crête après AAC).
# On arrondit les pics AVANT le master, au lieu de les écraser après.
mix = normaliser(np.tanh(2.2 * mix), 0.89)

st = np.stack([mix, mix], axis=1)
with wave.open(SORTIE, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print(f'{SORTIE} : {DUREE:.2f} s, {len(G["poses"])} retournements, accord final à {fin:.2f} s')
