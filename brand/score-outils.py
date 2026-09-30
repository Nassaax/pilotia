# -*- coding: utf-8 -*-
"""Bande-son du film « 9 questions » (film-outils.html).

Entièrement synthétisée : aucun échantillon tiers, aucune licence.
La grille des événements est lue dans le film (window.FILM.sons).

Usage : python3 score-outils.py <grille.json> <sortie.wav>

Hip-hop mi-tempo à 96 bpm, la mineur. La caisse claire tombe sur le temps 3,
exactement quand chaque carte claque. Les coups de fouet ont leur souffle.
La fin monte vers le premier temps : la vidéo boucle, le son aussi.
"""
import sys, json, wave
import numpy as np

SR = 48000
G = json.load(open(sys.argv[1], encoding='utf-8'))
SORTIE = sys.argv[2]
DUREE, TEMPS, MES = G['duree'], G['temps'], G['mesure']
N = int(SR * DUREE)
rng = np.random.default_rng(20261001)
BRUIT = rng.standard_normal(N + SR)
EXPLO = G['explosion']


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


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


def normaliser(x, c):
    m = np.max(np.abs(x))
    return x * (c / m) if m > 0 else x


def filtre(x, masque):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(np.fft.rfft(x) * masque(f), len(x))


def bande(fc, l):
    return lambda f: np.exp(-0.5 * (np.log2(np.maximum(f, 1) / fc) / l) ** 2)


def env(n, a, c):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / c)


def glissade(i0, duree, f0, f1, bloc=2048):
    """Bruit dont la bande glisse de f0 à f1 (souffle de coup de fouet)."""
    n = int(SR * duree); x = np.concatenate([BRUIT[i0:i0 + n], np.zeros(bloc)])
    out = np.zeros(n + bloc); fen = np.hanning(bloc); f = np.fft.rfftfreq(bloc, 1 / SR)
    for i in range(0, n, bloc // 2):
        u = min(1, (i + bloc / 2) / n)
        out[i:i + bloc] += np.fft.irfft(np.fft.rfft(x[i:i + bloc] * fen) * bande(f0 * (f1 / f0) ** u, 1.0)(f), bloc)
    return out[:n] * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.2


ACC = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]   # la m, fa, do, sol
def accord(t):
    return ACC[int(t // MES) % 4]


# ── Batterie ──────────────────────────────────────────────────────────────
def gc():
    n = int(SR * 0.3); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(50 + 120 * np.exp(-t * 40)) / SR) * np.exp(-t * 12) + BRUIT[:n] * np.exp(-t * 500) * 0.3


def caisse(i0):
    n = int(SR * 0.3); t = np.arange(n) / SR
    corps = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25)
    grain = filtre(BRUIT[i0:i0 + n], bande(3000, 1.4)) * np.exp(-t * 14)
    return 0.6 * corps + grain


def charley(i0):
    n = int(SR * 0.04); t = np.arange(n) / SR
    return filtre(BRUIT[i0:i0 + n], lambda f: np.clip((f - 7000) / 3000, 0, 1)) * np.exp(-t * 130)


def b808(f, duree):
    n = int(SR * duree); t = np.arange(n) / SR
    fr = f * (1 + 0.9 * np.exp(-t * 30))
    s = np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(fr) / SR))
    return s * env(n, 0.003, duree * 0.45)


bat, basse = piste(), piste()
GC = gc()
t = 0.0
while t < EXPLO - 1e-6:
    p = round((t % MES) / (TEMPS / 2))                      # position en croches (0 à 7)
    if p in (0, 3):
        poser(bat, t, GC, 1.0)
        if p == 0:                                         # la 808 seulement sur le 1 : le 3 appartient à l'impact
            poser(basse, t, b808(note(accord(t)[0] - 12), 1.0), 1.0)
    poser(bat, t, charley(int(t * 1301) % SR), 0.35 if p % 2 else 0.22, 0.25)
    if p == 7:                                             # roulement de charleston avant chaque fouet
        for k in range(1, 4):
            poser(bat, t + k * TEMPS / 6, charley(int(t * 733 + k) % SR), 0.2 + 0.08 * k, -0.25)
    t += TEMPS / 2
choc = piste()                                              # les impacts ont leur propre piste
for tc in G['coups']:                                       # la caisse claire = la carte qui claque
    if tc < EXPLO:
        poser(choc, tc, caisse(int(tc * 577) % SR), 0.9)

# ── Mélodie : cloches en arpège, doucement ────────────────────────────────
mus = piste()
t, k = 0.0, 0
while t < EXPLO - 1e-6:
    notes = accord(t)[1]
    m = notes[[0, 2, 1, 2, 0, 2, 1, 2][k % 8]] + 12 + (12 if k % 8 == 5 else 0)
    n = int(SR * 0.5); tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * note(m) * tt) + 0.3 * np.sin(2 * np.pi * 2.76 * note(m) * tt) * np.exp(-tt * 12)) * env(n, 0.002, 0.18)
    poser(mus, t, s, 0.5, -0.35 if k % 2 else 0.35)
    t += TEMPS / 2; k += 1
# nappe basse, pour lier
t = 0.0
while t < EXPLO - 1e-6:
    n = int(SR * MES); tt = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * note(m) * tt) + 0.2 * np.sin(4 * np.pi * note(m) * tt) for m in accord(t)[1])
    s *= np.minimum(1, np.minimum(tt / 0.2, (MES - tt) / 0.2))
    poser(mus, t, s, 0.12)
    t += MES

# ── Bruitages ─────────────────────────────────────────────────────────────
sfx = piste()
for j, tw in enumerate(G['fouets']):
    s = glissade(int(tw * 911) % SR, 0.42, 5000, 400)
    u = np.linspace(0.8, -0.8, len(s))                      # de droite à gauche, comme l'image
    poser(sfx, tw - 0.2, np.stack([s * np.cos((u + 1) * np.pi / 4), s * np.sin((u + 1) * np.pi / 4)]) * np.sqrt(2), 0.9)
for tc in G['coups']:
    n = int(SR * 0.9); tt = np.arange(n) / SR
    boum = np.sin(2 * np.pi * (45 + 40 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 3)
    metal = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) for f, d in ((1870, 6), (2630, 8), (3950, 11))) / 3
    poser(choc, tc, boum + 0.35 * metal, 1.3 if tc == G['neuf'] else 0.8)   # le 9 frappe plus fort
    if tc != G['neuf']:                                     # la carte arrive du fond (le 9, lui, naît des particules)
        poser(sfx, tc - 0.4, glissade(int(tc * 313) % SR, 0.4, 300, 3500) * np.linspace(0, 1, int(SR * 0.4)), 0.3)
for j, t in enumerate(G['mots']):
    n = int(SR * 0.05); tt = np.arange(n) / SR
    poser(sfx, t, np.sin(2 * np.pi * (2200 + 180 * (j % 5)) * tt) * np.exp(-tt * 90), 0.12, -0.4 + (j % 5) * 0.2)
for t in G['gratuits'] + [G['lien']]:
    n = int(SR * 0.1); tt = np.arange(n) / SR
    poser(sfx, t, np.sin(2 * np.pi * np.cumsum(1400 - 1000 * np.exp(-tt * 50)) / SR) * env(n, 0.001, 0.04), 0.45)
# les particules se rassemblent : un scintillement qui monte jusqu'au 9
for k in range(40):
    t = 0.1 + (G['neuf'] - 0.1) * (k / 40) ** 0.8
    n = int(SR * 0.25); tt = np.arange(n) / SR
    poser(sfx, t, np.sin(2 * np.pi * note(81 + [0, 3, 5, 7, 10, 12, 15][k % 7]) * tt) * env(n, 0.002, 0.06), 0.06 + 0.06 * k / 40, np.sin(k * 1.7) * 0.7)
poser(sfx, G['anneau'], glissade(4444, 0.8, 400, 6000), 0.6)
# l'explosion, puis la montée qui ramène au début
n = int(SR * 1.4); tt = np.arange(n) / SR
poser(choc, EXPLO, filtre(BRUIT[:n], lambda f: np.exp(-f / 5000)) * np.exp(-tt * 3.5) + 1.2 * np.sin(2 * np.pi * (40 + 60 * np.exp(-tt * 10)) * tt) * np.exp(-tt * 3), 1.0)
reste = DUREE - EXPLO - 0.35
n = int(SR * reste); u = np.linspace(0, 1, n)
montee = glissade(9999, reste, 300, 7000) / (np.sin(np.pi * np.linspace(0, 1, n)) ** 1.2 + 1e-3) * u ** 2.2
poser(sfx, EXPLO + 0.35, np.clip(montee, -6, 6), 0.3)

# Chaque impact creuse la basse et la mélodie (−9 dB, retour en 0,35 s) : il
# domine ce qui l'entoure au lieu de s'y noyer.
creux = np.ones(N)
for tc in list(G['coups']) + [EXPLO]:
    i = int(tc * SR); n = int(0.6 * SR); tt = np.arange(min(n, N - i)) / SR
    creux[i:i + len(tt)] = np.minimum(creux[i:i + len(tt)], 1 - 0.65 * np.exp(-tt / 0.18))
basse *= creux; mus *= creux; bat *= 0.4 + 0.6 * creux
mix = normaliser(bat, 0.45) + normaliser(basse, 0.42) + normaliser(mus, 0.3) + normaliser(sfx, 0.42) + normaliser(choc, 0.86)
mix = normaliser(np.tanh(1.7 * normaliser(mix, 0.89)), 0.89)
with wave.open(SORTIE, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
print(f'{SORTIE} : {DUREE:.2f} s, {len(G["coups"])} coups, explosion à {EXPLO:.2f} s')
