# -*- coding: utf-8 -*-
"""Bande-son du film « Le cap » (film-cap.html).

Entièrement synthétisée : aucun échantillon tiers, donc aucune licence à
déclarer ni revendication possible sur les réseaux.

La grille des événements n'est PAS retapée ici : elle est lue dans le film
(window.FILM.sons), exportée en JSON par le script de rendu. Image et son
viennent de la même source, ils ne peuvent pas diverger.

Usage : python3 score-cap.py <grille.json> <sortie.wav>

Musique : 120 bpm, la mineur (sol, la m, fa, do, sol...), une grosse caisse
par temps qui fait « pomper » la nappe et la basse (compression latérale).
La musique démarre sur « Vous. », monte pendant la grue, puis s'arrête net
sur la flèche : le logo arrive dans le silence, avec un seul son de verre.

Le volume est de l'arithmétique : chaque bus est normalisé à une crête
connue AVANT le mélange ; le master est ensuite mesuré sur le fichier livré
(cible -14 LUFS, crête vraie <= -1 dBTP).
"""
import sys, json, wave
import numpy as np

SR = 48000
G = json.load(open(sys.argv[1], encoding='utf-8'))
SORTIE = sys.argv[2]
DUREE = G['duree']
N = int(SR * DUREE)
TEMPS = 60 / G['bpm']
MESURE = 4 * TEMPS
FIN_MUSIQUE = G['fleche']                 # la musique s'arrête net sur la flèche
rng = np.random.default_rng(20260929)     # graine fixe : rendu reproductible
BRUIT = rng.standard_normal(N + SR)


def note(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def piste():
    return np.zeros((2, N))


def poser(bus, t0, son, gain=1.0, pan=0.0):
    """Pose un son (mono ou stéréo) à t0, panoramique à puissance constante."""
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


def env_ad(n, attaque, chute):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attaque, 1e-4)) * np.exp(-t / chute)


def filtre_fft(x, masque):
    """Filtre statique dans le domaine fréquentiel. masque(f) -> gain."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * masque(f), len(x))


def filtre_glissant(x, masque_t, bloc=2048):
    """Filtre qui varie dans le temps : fenêtres de Hann à 50 %, un masque
    par fenêtre (masque_t(t_centre, f) -> gain), puis recouvrement-addition."""
    n = len(x)
    out = np.zeros(n + bloc)
    fen = np.hanning(bloc)
    f = np.fft.rfftfreq(bloc, 1 / SR)
    xs = np.concatenate([x, np.zeros(bloc)])
    for i in range(0, n, bloc // 2):
        seg = xs[i:i + bloc] * fen
        out[i:i + bloc] += np.fft.irfft(np.fft.rfft(seg) * masque_t((i + bloc / 2) / SR, f), bloc)
    return out[:n]


def passe_bande(fc, largeur):
    return lambda f: np.exp(-0.5 * (np.log2(np.maximum(f, 1) / fc) / largeur) ** 2)


def dent_de_scie(f, t, harmoniques=14, eclat=6.0):
    """Dent de scie additive, sans repliement, harmoniques adoucies."""
    s = np.zeros_like(t)
    for k in range(1, harmoniques + 1):
        if f * k > SR / 2 - 1000:
            break
        s += np.sin(2 * np.pi * f * k * t) / k * np.exp(-(k - 1) / eclat)
    return s


ACCORDS = {                                # racine (basse), notes de la nappe
    'Am': (45, [57, 60, 64, 69]),
    'F': (41, [57, 60, 65, 69]),
    'C': (48, [55, 60, 64, 67]),
    'G': (43, [55, 59, 62, 67]),
}
SUITE = ['G', 'Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F']


def accord(t):
    return ACCORDS[SUITE[min(len(SUITE) - 1, int(t // MESURE))]]


# ── Batterie ───────────────────────────────────────────────────────────────
bat = piste()
depart = G['depart']
kicks = [depart + i * TEMPS for i in range(int(round((G['revelation'][0] - depart) / TEMPS)))]


def grosse_caisse():
    n = int(SR * 0.42); t = np.arange(n) / SR
    f = 44 + 120 * np.exp(-t * 32)
    corps = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    clic = BRUIT[:n] * np.exp(-t * 380) * 0.35
    return corps + clic


def claquement(i0):
    n = int(SR * 0.22); t = np.arange(n) / SR
    b = filtre_fft(BRUIT[i0:i0 + n], passe_bande(1400, 1.0))
    e = np.zeros(n)
    for d in (0, 0.011, 0.022):                         # trois mains, un claquement
        k = int(d * SR); e[k:] += np.exp(-(t[:n - k]) * (60 if d < 0.02 else 18))
    return b * e


def charleston(i0, ouvert=False):
    n = int(SR * (0.16 if ouvert else 0.035)); t = np.arange(n) / SR
    b = filtre_fft(BRUIT[i0:i0 + n], lambda f: np.clip((f - 6500) / 3000, 0, 1))
    return b * np.exp(-t * (22 if ouvert else 110))


GC = grosse_caisse()
for k in kicks:
    poser(bat, k, GC, 1.0)
t = depart + 2 * TEMPS
while t < G['revelation'][0] - 0.01:
    if int(round((t - depart) / TEMPS)) % 2 == 1 and t >= G['chapitres'][0]:
        poser(bat, t, claquement(int(t * 997) % SR), 0.5)
    t += TEMPS
for i in range(int((G['revelation'][0] - G['chapitres'][0]) / (TEMPS / 4))):
    t = G['chapitres'][0] + i * TEMPS / 4
    accent = [0.35, 0.18, 0.6, 0.2][i % 4]
    poser(bat, t, charleston(int(t * 1301) % SR), accent, 0.25 if i % 2 else -0.25)
    sprint = G['engagements'][0] <= t < G['grue'] and i % 4 == 2
    if sprint:
        poser(bat, t, charleston(int(t * 733) % SR, ouvert=True), 0.4, 0.3)
# Roulement de caisse claire qui accélère pendant la révélation
t, pas = G['revelation'][0], TEMPS / 2
while t < FIN_MUSIQUE - 0.01:
    prog = (t - G['revelation'][0]) / (FIN_MUSIQUE - G['revelation'][0])
    poser(bat, t, claquement(int(t * 577) % SR), 0.18 + 0.4 * prog)
    pas = TEMPS / 2 if prog < 0.33 else (TEMPS / 4 if prog < 0.66 else TEMPS / 8)
    t += pas

# ── Musique ────────────────────────────────────────────────────────────────
mus = piste()
tt = np.arange(N) / SR
# Nappe : dent de scie adoucie, deux voix désaccordées (gauche/droite),
# plus claire après le départ, qui s'ouvre pendant la grue.
nappe = np.zeros((2, N))
for m in range(int(np.ceil(FIN_MUSIQUE / MESURE))):
    t0, t1 = m * MESURE, min(FIN_MUSIQUE, (m + 1) * MESURE)
    i0, i1 = int(t0 * SR), int(t1 * SR)
    t = np.arange(i1 - i0) / SR
    racine, notes = ACCORDS[SUITE[m]]
    eclat = 2.5 if t0 < depart else (5.0 if t0 < G['grue'] else 8.0)
    for c, detune in ((0, -0.004), (1, 0.004)):
        s = sum(dent_de_scie(note(n) * (1 + detune), t + t0, 10, eclat) for n in notes)
        fondu = np.minimum(1, np.minimum(t / 0.03, (t1 - t0 - t) / 0.03))
        nappe[c, i0:i1] += s * fondu
nappe *= np.where(tt < depart, 0.35 + 0.65 * (tt / depart) ** 2, 1.0)
# Basse : croches, racine puis octave, en pincé.
basse = np.zeros(N)
t = depart
while t < G['revelation'][0] - 0.01:
    racine = accord(t)[0]
    k = int(round((t - depart) / (TEMPS / 2)))
    f = note(racine + (12 if k % 2 else 0))
    n = int(SR * 0.24); tb = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * tb) + 0.35 * np.sin(4 * np.pi * f * tb) + 0.12 * np.sin(6 * np.pi * f * tb)) * env_ad(n, 0.004, 0.11)
    i = int(t * SR); basse[i:i + n] += s[:max(0, min(n, N - i))]
    t += TEMPS / 2
# Compression latérale : chaque grosse caisse creuse la nappe et la basse.
pompe = np.ones(N)
for k in kicks:
    i = int(k * SR); n = int(SR * TEMPS)
    pompe[i:i + n] *= 1 - 0.72 * np.exp(-np.arange(min(n, N - i)) / SR / 0.11)
nappe *= pompe; basse *= pompe
mus += normaliser(nappe, 0.5) + normaliser(basse, 0.8)
# Arpège en doubles croches, en ping-pong, de « Diagnostiquer » à la grue.
arp = piste()
i = 0
t = G['chapitres'][1]
while t < G['revelation'][0] - 0.01:
    notes = accord(t)[1]
    nn = notes[[0, 1, 2, 3, 2, 1, 3, 2][i % 8]] + 12
    n = int(SR * 0.2); ta = np.arange(n) / SR
    s = (np.sin(2 * np.pi * note(nn) * ta) + 0.3 * np.sin(4 * np.pi * note(nn) * ta)) * env_ad(n, 0.002, 0.07)
    poser(arp, t, s, 0.9 if i % 4 == 0 else 0.6, 0.45 if i % 2 else -0.45)
    t += TEMPS / 4; i += 1
mus += normaliser(arp, 0.28) * pompe

# ── Bruitages ──────────────────────────────────────────────────────────────
sfx = piste()


def tic(f=3200, duree=0.03):
    n = int(SR * duree); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 180)


def souffle(duree, i0, f0, f1, montee=0.6):
    """Bruit filtré dont la bande glisse de f0 à f1 : un passage d'air."""
    n = int(SR * duree)
    b = BRUIT[i0:i0 + n]
    b = filtre_glissant(b, lambda tc, f: passe_bande(f0 * (f1 / f0) ** min(1, tc / duree), 0.9)(f))
    u = np.linspace(0, 1, n)
    return b * (np.where(u < montee, u / montee, (1 - u) / (1 - montee)) ** 1.5)


def impact():
    n = int(SR * 1.2); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * (48 + 30 * np.exp(-t * 20)) * t) * np.exp(-t * 3.2)
    b = filtre_fft(BRUIT[:n], lambda f: np.exp(-f / 900)) * np.exp(-t * 18)
    return sub + 0.5 * b


def cloche(f, duree=1.4):
    n = int(SR * duree); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d)
            for a, r, d in ((1, 1, 3.2), (0.45, 2.76, 5.5), (0.25, 5.4, 9), (0.12, 8.9, 14)))
    return s * np.minimum(1, t / 0.002)


def ping(f):
    n = int(SR * 0.9); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * (1 - 0.03 * t) * t) * np.exp(-t * 5) * np.minimum(1, t / 0.003)


for i, t in enumerate(G['mots']):                        # accroche : un tic par mot
    poser(sfx, t, tic(2600 + 300 * i), 0.35)
for t in G['chapitres']:                                   # chaque chapitre tombe sur un impact
    poser(sfx, t, impact(), 0.9)
    poser(sfx, t, cloche(note(accord(t)[1][-1] + 12)), 0.22)
for t in G['sousTitres']:
    poser(sfx, t, tic(4200, 0.02), 0.12)
for k, (t, d) in enumerate(G['virages']):                  # virages : souffle panoramique
    s = souffle(d, int(t * 911) % SR, 300, 3800)
    u = np.linspace(-0.8, 0.8, len(s)) * (1 if k == 0 else -1)
    poser(sfx, t, np.stack([s * np.cos((u + 1) * np.pi / 4), s * np.sin((u + 1) * np.pi / 4)]) * np.sqrt(2), 0.9)
for t in G['ondes']:                                       # ondes au sol : sonar
    poser(sfx, t, ping(1318.5), 0.3)
    poser(sfx, t + 0.18, ping(1318.5), 0.1, 0.5)
r = G['radar']
poser(sfx, r['debut'], souffle(r['duree'], 4321, 900, 2400, montee=0.3), 0.35)
for k, t in enumerate(r['points']):
    poser(sfx, t, ping(1760 * 2 ** (k * 4 / 12)) * np.exp(-np.arange(int(SR * 0.9)) / SR * 6), 0.3, [-0.5, 0.1, 0.5][k])
for k in range(9):                                         # l'éventail s'ouvre : un scintillement
    poser(sfx, G['eventail'] + k * 0.035, ping(note(81 + [0, 3, 7, 10, 12, 15, 19, 22, 24][k])) * 0.5, 0.18, -0.6 + k * 0.15)
n = int(SR * 0.28); tz = np.arange(n) / SR                  # il se referme : une glissade descendante
poser(sfx, G['fermeture'], np.sin(2 * np.pi * np.cumsum(2200 * np.exp(-tz * 9) + 250) / SR) * np.exp(-tz * 7), 0.3)
for k, t in enumerate(G['portes']):                        # chaque porte franchie
    poser(sfx, t - 0.12, souffle(0.3, int(t * 523) % SR, 1200, 5200, montee=0.7), 0.4)
    poser(sfx, t, cloche(note(76 + [0, 2, 4, 7][k]), 0.6), 0.2)
for t in G['engagements']:                                 # un accent d'accord par engagement
    notes = accord(t)[1]
    n = int(SR * 0.35); ts = np.arange(n) / SR
    s = sum(dent_de_scie(note(x + 12), ts, 8, 5) for x in notes) * env_ad(n, 0.003, 0.09)
    poser(sfx, t, s, 0.22)
# La grue : longue montée (bruit et sirène) jusqu'à la flèche.
d = FIN_MUSIQUE - G['grue']
n = int(SR * d); tg = np.arange(n) / SR
montee = souffle(d, 777, 250, 7000, montee=0.999)
f = 110 * (1 + 5 * (tg / d) ** 2)
sirene = np.sin(2 * np.pi * np.cumsum(f) / SR) * (tg / d) ** 2
poser(sfx, G['grue'], montee * 1.0 + 0.25 * sirene, 0.5)
for t in G['revelation']:
    poser(sfx, t, tic(3000, 0.025), 0.2)
n = int(SR * 0.8); tb = np.arange(n) / SR                   # le spectre se vide : un reflet qui monte
poser(sfx, G['blanc'], sum(np.sin(2 * np.pi * note(84 + k) * (1 + 0.5 * tb) * tb) for k in (0, 7, 12)) * np.sin(np.pi * tb / 0.8) * 0.3, 0.25)

# ── La fin : un coup, puis le silence ─────────────────────────────────────
coup = piste()
poser(coup, FIN_MUSIQUE, GC, 1.2)
poser(coup, FIN_MUSIQUE, impact(), 1.0)
n = int(SR * 0.6); ts = np.arange(n) / SR
notes = ACCORDS['C'][1]
stab = sum(dent_de_scie(note(x), ts, 12, 7) + dent_de_scie(note(x + 12), ts, 8, 5) for x in notes) * env_ad(n, 0.002, 0.16)
poser(coup, FIN_MUSIQUE, stab, 0.45)
poser(coup, FIN_MUSIQUE, filtre_fft(BRUIT[:int(SR * 0.7)], lambda f: np.clip(f / 4000, 0, 1)) * np.exp(-np.arange(int(SR * 0.7)) / SR * 7), 0.25)
poser(coup, G['reflet'], cloche(note(96), 2.2), 0.16)             # le reflet sur l'icône, seul dans le silence

# Tout ce qui joue s'arrête net sur la flèche (fondu de 8 ms contre le clic).
i = int(FIN_MUSIQUE * SR); f = int(0.008 * SR)
for bus in (bat, mus, sfx):
    bus[:, i:i + f] *= np.linspace(1, 0, f)
    bus[:, i + f:] = 0

# ── Mélange : chaque bus à une crête connue avant la somme ───────────────
mix = normaliser(mus, 0.5) + normaliser(bat, 0.52) + normaliser(sfx, 0.4) + normaliser(coup, 0.85)
f = int(0.4 * SR)
mix[:, -f:] *= np.linspace(1, 0, f)
mix = normaliser(mix, 0.89)
# Saturation douce : arrondit les crêtes courtes avant le master plutôt que
# de laisser le limiteur tout baisser.
mix = normaliser(np.tanh(1.8 * mix), 0.89)

with wave.open(SORTIE, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
print(f'{SORTIE} : {DUREE:.2f} s, {len(kicks)} grosses caisses, arrêt net à {FIN_MUSIQUE:.2f} s')
