# -*- coding: utf-8 -*-
"""Bande-son du film « Votre métier » (film-metiers.html).

Entièrement synthétisée : aucun échantillon tiers, donc aucune licence à
déclarer ni revendication possible sur les réseaux.

La grille des événements est lue dans le film (window.FILM.sons), exportée
en JSON par le script de rendu : image et son ne peuvent pas diverger.

Usage : python3 score-metiers.py <grille.json> <sortie.wav>

Musique : pop-funk à 128 bpm, do majeur. L'accroche n'a que des claquements
de doigts et un piano électrique ; le groove (grosse caisse, basse slappée)
démarre sur le premier métier. Le film est mené par les bruitages : un
rebond à chaque transformation, une claque à chaque autocollant, une note
par mot. Il finit sur un accord suspendu (sol sus4) : la question reste ouverte.

Le volume est de l'arithmétique : chaque bus est normalisé à une crête connue
AVANT le mélange ; le master est mesuré sur le fichier livré (cible -14 LUFS,
crête vraie <= -1 dBTP).
"""
import sys, json, wave
import numpy as np

SR = 48000
G = json.load(open(sys.argv[1], encoding='utf-8'))
SORTIE = sys.argv[2]
DUREE = G['duree']
N = int(SR * DUREE)
TEMPS = G['temps']
MESURE = 4 * TEMPS
rng = np.random.default_rng(20260930)      # graine fixe : rendu reproductible
BRUIT = rng.standard_normal(N + SR)


def note(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def piste():
    return np.zeros((2, N))


def poser(bus, t0, son, gain=1.0, pan=0.0):
    i = int(round(t0 * SR))
    if i >= N or i < 0:
        return
    if son.ndim == 1:
        a = (pan + 1) * np.pi / 4
        son = np.stack([son * np.cos(a), son * np.sin(a)]) * np.sqrt(2)
    fin = min(N, i + son.shape[1])
    bus[:, i:fin] += gain * son[:, :fin - i]


def normaliser(x, crete):
    m = np.max(np.abs(x))
    return x * (crete / m) if m > 0 else x


def filtre_fft(x, masque):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * masque(f), len(x))


def passe_bande(fc, largeur):
    return lambda f: np.exp(-0.5 * (np.log2(np.maximum(f, 1) / fc) / largeur) ** 2)


def env(n, attaque, chute):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attaque, 1e-4)) * np.exp(-t / chute)


# ── Harmonie : sol pendant l'accroche, puis do, la m, fa, sol en boucle ──
ACCORDS = {
    'C': (48, [60, 64, 67, 72]), 'Am': (45, [60, 64, 69, 72]),
    'F': (41, [60, 65, 69, 72]), 'G': (43, [59, 62, 67, 71]),
}
DEPART = G['groove']
def accord(t):
    n = int(np.floor((t - DEPART) / MESURE + 1e-6))
    return ACCORDS[['C', 'Am', 'F', 'G'][n % 4]]


# ── Timbres ────────────────────────────────────────────────────────────────
def piano(f, duree=0.9, force=1.0):
    """Piano électrique (modulation de fréquence) : attaque de marteau, tenue ronde."""
    n = int(SR * duree); t = np.arange(n) / SR
    indice = 2.4 * np.exp(-t * 7) + 0.25
    s = np.sin(2 * np.pi * f * t + indice * np.sin(2 * np.pi * f * t))
    s += 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)          # le « tine »
    return s * env(n, 0.003, 0.55) * force


def basse_slap(f, duree=0.28, pop=False):
    n = int(SR * duree); t = np.arange(n) / SR
    eclat = np.exp(-t * 16)
    s = np.zeros(n)
    for k in range(1, 12):
        s += np.sin(2 * np.pi * f * k * t) / k * np.exp(-(k - 1) * (1.2 - eclat))
    if pop:
        s += 0.6 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 40)
    return s * env(n, 0.002, 0.16)


def grosse_caisse():
    n = int(SR * 0.35); t = np.arange(n) / SR
    fr = 50 + 110 * np.exp(-t * 35)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9) + BRUIT[:n] * np.exp(-t * 400) * 0.3


def claque_mains(i0):
    n = int(SR * 0.2); t = np.arange(n) / SR
    b = filtre_fft(BRUIT[i0:i0 + n], passe_bande(1500, 1.0))
    e = np.zeros(n)
    for d in (0, 0.009, 0.019):
        k = int(d * SR); e[k:] += np.exp(-t[:n - k] * (70 if d < 0.019 else 20))
    return b * e


def doigts(i0):
    n = int(SR * 0.08); t = np.arange(n) / SR
    return filtre_fft(BRUIT[i0:i0 + n], passe_bande(2600, 0.6)) * np.exp(-t * 70) + 0.3 * np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90)


def charleston(i0):
    n = int(SR * 0.04); t = np.arange(n) / SR
    return filtre_fft(BRUIT[i0:i0 + n], lambda f: np.clip((f - 7000) / 3000, 0, 1)) * np.exp(-t * 120)


def cuivres(notes, duree=0.42):
    """Coup de cuivres synthétiques sur chaque transformation."""
    n = int(SR * duree); t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for d in (-0.006, 0.006):
            f = note(m) * (1 + d)
            for k in range(1, 9):
                s += np.sin(2 * np.pi * f * k * t) / k * np.exp(-(k - 1) * 0.35)
    return s * env(n, 0.012, 0.16)


def rebond(f0=190):
    """Le « boing » du ressort : la hauteur saute puis retombe en vibrant."""
    n = int(SR * 0.5); t = np.arange(n) / SR
    f = f0 * (1 + 0.9 * np.exp(-t * 9)) * (1 + 0.06 * np.sin(2 * np.pi * 17 * t) * np.exp(-t * 4))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.004, 0.16)


def vague(i0, duree=0.42):
    """Le souffle de l'inondation de couleur."""
    n = int(SR * duree); u = np.linspace(0, 1, n)
    b = filtre_fft(BRUIT[i0:i0 + n], passe_bande(1800, 1.3))
    return b * np.sin(np.pi * u) ** 1.5


def claque(i0):
    """Un autocollant qui claque : papier + petit choc sourd."""
    n = int(SR * 0.12); t = np.arange(n) / SR
    papier = filtre_fft(BRUIT[i0:i0 + n], passe_bande(2200, 0.9)) * np.exp(-t * 55)
    choc = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 35)
    return papier + 0.7 * choc


def pop(f0=320, f1=1100):
    n = int(SR * 0.09); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.035)


def marimba(f):
    n = int(SR * 0.35); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 3.99 * f * t) * np.exp(-t * 30)) * env(n, 0.002, 0.08)


# ── Batterie ──────────────────────────────────────────────────────────────
bat = piste()
GC = grosse_caisse()
fin_groove = G['final'] - TEMPS           # tout s'arrête un temps avant l'accord final : il tombe dans le vide
# Accroche : claquements de doigts sur les temps 2 et 4.
k = 1
while k * TEMPS < DEPART - 0.01:
    if k % 2 == 1:
        poser(bat, k * TEMPS, doigts(int(k * 997) % SR), 0.55, 0.3 if k % 4 == 1 else -0.3)
    k += 1
# Groove : grosse caisse sur 1, 2-et, 3 ; mains sur 2 et 4 ; charleston en croches.
t = DEPART
while t < fin_groove - 0.01:
    pos = round((t - DEPART) / (TEMPS / 2)) % 8                     # position en croches dans la mesure
    pause = G['bulle'] <= t < G['bulle'] + MESURE                    # un souffle quand la bulle apparaît
    if not pause:
        if pos in (0, 3, 4):
            poser(bat, t, GC, 1.0)
        if pos in (2, 6):
            poser(bat, t, claque_mains(int(t * 577) % SR), 0.55)
        poser(bat, t, charleston(int(t * 1301) % SR), 0.28 if pos % 2 else 0.18, 0.2)
        if G['emballement'] <= t < G['bulle']:                     # l'emballement : doubles croches
            poser(bat, t + TEMPS / 4, charleston(int(t * 733) % SR), 0.22, -0.2)
    t += TEMPS / 2
# Roulement de mains qui accélère vers la bulle.
t = G['bulle'] - MESURE
while t < G['bulle'] - 0.01:
    u = (t - (G['bulle'] - MESURE)) / MESURE
    poser(bat, t, claque_mains(int(t * 331) % SR), 0.15 + 0.35 * u)
    t += TEMPS / 2 if u < 0.5 else TEMPS / 4

# ── Musique ───────────────────────────────────────────────────────────────
mus = piste()
# Piano électrique : accords en contretemps pendant le groove, tenus pendant l'accroche.
t = 0.0
while t < fin_groove - 0.01:
    if t < DEPART:
        racine, notes = (ACCORDS['G'] if t >= DEPART - MESURE else ACCORDS['Am'] if t < MESURE else ACCORDS['F'])
        if abs((t / MESURE) - round(t / MESURE)) < 1e-6:
            for j, m in enumerate(notes):
                poser(mus, t + j * 0.012, piano(note(m), 1.8, 0.7), 0.5, -0.25 + j * 0.17)
        t += TEMPS
        continue
    racine, notes = accord(t)
    pos = round((t - DEPART) / (TEMPS / 2)) % 8
    if pos in (1, 3, 5, 6) and not (G['bulle'] <= t < G['bulle'] + MESURE / 2):
        for j, m in enumerate(notes[:3]):
            poser(mus, t, piano(note(m), 0.35, 0.8), 0.32, -0.3 + j * 0.3)
    t += TEMPS / 2
# Basse slappée : motif funk d'une mesure en croches (racine, octave, quinte).
MOTIF = [(0, 0, False), None, (12, 0, True), (0, 0, False), (0, 0, False), (7, 0, False), (12, 0, True), (10, 0, False)]
t = DEPART
while t < fin_groove - 0.01:
    pos = round((t - DEPART) / (TEMPS / 2)) % 8
    m = MOTIF[pos]
    if m and not (G['bulle'] <= t < G['bulle'] + MESURE / 2):
        racine = accord(t)[0]
        poser(mus, t, basse_slap(note(racine + m[0]), pop=m[2]), 0.9)
    t += TEMPS / 2
mus = normaliser(mus, 0.6)

# ── Bruitages ─────────────────────────────────────────────────────────────
sfx = piste()
poser(sfx, G['apparition'], pop(250, 800), 0.6)
PENTA = [72, 74, 76, 79, 81, 84, 86, 88]                             # do majeur pentatonique
for j, t in enumerate(G['mots']):
    poser(sfx, t, marimba(note(PENTA[j % len(PENTA)])), 0.22, -0.3 + (j % 5) * 0.15)
# Le tampon « non » : choc sourd et petit buzzer de jeu télévisé.
n = int(SR * 0.3); tt = np.arange(n) / SR
buzz = np.sign(np.sin(2 * np.pi * 110 * tt)) * env(n, 0.003, 0.12)
poser(sfx, G['tampon'], np.sin(2 * np.pi * (60 + 50 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) + 0.25 * filtre_fft(buzz, lambda f: np.exp(-f / 2500)), 0.9)
for t in G['autocollants']:
    poser(sfx, t, claque(int(t * 811) % SR), 0.6)
for j, t in enumerate(G['morphs']):
    rapide = G['emballement'] <= t < G['bulle']
    poser(sfx, t, rebond(170 + 22 * (j % 6)), 0.55 if rapide else 0.7)
    poser(sfx, t, vague(int(t * 919) % SR), 0.4)
    if not rapide and t < G['bulle']:
        poser(sfx, t, cuivres([m + 12 for m in accord(t)[1][:3]]), 0.35)
poser(sfx, G['bulle'], pop(300, 1400), 0.8)
for j, t in enumerate(G['minis']):
    poser(sfx, t, pop(400 + 120 * j, 1300 + 200 * j), 0.45, -0.5 + j * 0.25)
# Montée vers la bulle.
n = int(SR * (G['bulle'] - G['emballement'])); u = np.linspace(0, 1, n)
montee = filtre_fft(BRUIT[:n], lambda f: np.exp(-0.5 * (np.log2(np.maximum(f, 1) / 2500) / 1.4) ** 2)) * u ** 2
poser(sfx, G['emballement'], montee, 0.25)

# ── La fin : un accord suspendu, qui résonne ──────────────────────────────
coup = piste()
poser(coup, G['final'], GC, 1.0)
poser(coup, G['final'], claque_mains(4242), 0.6)
for j, m in enumerate([55, 60, 62, 67, 72, 74]):                    # sol sus4 : sol, do, ré
    poser(coup, G['final'] + j * 0.01, piano(note(m), 2.6, 1.0), 0.4, -0.4 + j * 0.16)
poser(coup, G['final'], cuivres([67, 72, 74], 0.6), 0.4)
poser(coup, G['final'], basse_slap(note(43), 0.9), 0.9)
poser(coup, G['final'] + 0.05, rebond(210), 0.5)
n = int(SR * TEMPS); u = np.linspace(0, 1, n)                        # le temps de silence : une aspiration qui monte
aspiration = filtre_fft(BRUIT[:n], lambda f: np.exp(-0.5 * (np.log2(np.maximum(f, 1) / 3000) / 1.2) ** 2)) * u ** 2.5
poser(coup, G['final'] - TEMPS, aspiration, 0.35)

# ── Mélange ───────────────────────────────────────────────────────────────
mix = normaliser(mus, 0.5) + normaliser(bat, 0.5) + normaliser(sfx, 0.46) + normaliser(coup, 0.86)
f = int(0.35 * SR)
mix[:, -f:] *= np.linspace(1, 0, f)
mix = normaliser(np.tanh(1.7 * normaliser(mix, 0.89)), 0.89)
with wave.open(SORTIE, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
print(f'{SORTIE} : {DUREE:.2f} s, {len(G["morphs"])} transformations, accord final à {G["final"]:.2f} s')
