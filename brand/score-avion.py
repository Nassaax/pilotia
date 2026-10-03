# -*- coding: utf-8 -*-
"""Bande-son du film « Prenez de la hauteur » (film-avion.html).

Entièrement synthétisée (aucun échantillon, aucune licence), sauf la voix off,
générée par synthèse vocale (voir film-avion-DIRECTION.md).
La grille des événements est lue dans le film (window.FILM.sons) : chaque
bruitage tombe sur l'image qui le produit.

Usage : python3 score-avion.py <grille.json> <voix.wav> <sortie.wav> [ffmpeg]

Acte I (nuit) : piano feutré en ré mineur, pendule, chambre silencieuse ;
chaque feuille, chaque tampon a son bruit. Acte II : un pli par croche à
111 bpm, une note qui monte à chaque pli. Acte III (aube) : groove ample en
fa majeur. Acte IV : la ligne du logo chante en montant, accord final sur
« Pilotia ». La musique se creuse sous la voix (−9 dB) : la voix gagne toujours.
"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
G = json.load(open(sys.argv[1], encoding='utf-8'))
VOIX, SORTIE = sys.argv[2], sys.argv[3]
FFMPEG = sys.argv[4] if len(sys.argv) > 4 else 'ffmpeg'
DUREE = G['duree']; N = int(SR * DUREE)
rng = np.random.default_rng(20261003)
BRUIT = rng.standard_normal(N + SR * 2)
CRO = 60 / G['tempo'] / 2                      # une croche = un pli (0,27 s)


def note(m): return 440.0 * 2 ** ((m - 69) / 12)
def piste(): return np.zeros((2, N))
def tt(d): return np.arange(int(SR * d)) / SR


def poser(bus, t0, son, gain=1.0, pan=0.0):
    i = int(round(t0 * SR))
    if son.ndim == 1:
        a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
        son = np.stack([son * np.cos(a), son * np.sin(a)]) * np.sqrt(2)
    if i < 0: son = son[:, -i:]; i = 0
    if i >= N: return
    fin = min(N, i + son.shape[1]); bus[:, i:fin] += gain * son[:, :fin - i]


def normaliser(x, c):
    m = np.max(np.abs(x)); return x * (c / m) if m > 0 else x


def filtre(x, masque):
    f = np.fft.rfftfreq(x.shape[-1], 1 / SR); return np.fft.irfft(np.fft.rfft(x) * masque(f), x.shape[-1])


def bande(fc, l): return lambda f: np.exp(-0.5 * (np.log2(np.maximum(f, 1) / fc) / l) ** 2)
def passe_bas(fc): return lambda f: 1 / np.sqrt(1 + (f / fc) ** 4)
def passe_haut(fc): return lambda f: 1 / np.sqrt(1 + (fc / np.maximum(f, 1)) ** 4)


def env(n, a, c):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / c)


def glissade(i0, duree, f0, f1, bloc=2048, l=0.9):
    """Bruit dont la bande glisse de f0 à f1 (souffles, passages)."""
    n = int(SR * duree); x = np.concatenate([BRUIT[i0:i0 + n], np.zeros(bloc)])
    out = np.zeros(n + bloc); fen = np.hanning(bloc); f = np.fft.rfftfreq(bloc, 1 / SR)
    for i in range(0, n, bloc // 2):
        u = min(1, (i + bloc / 2) / n)
        out[i:i + bloc] += np.fft.irfft(np.fft.rfft(x[i:i + bloc] * fen) * bande(f0 * (f1 / f0) ** u, l)(f), bloc)
    return out[:n]


def reverb(x, rt=2.2, seed=7, ton=5000):
    """Réverbération par convolution avec une réponse synthétique (bruit à décroissance exponentielle, stéréo décorrélée)."""
    n = int(SR * rt * 1.2); t = np.arange(n) / SR; r = np.random.default_rng(seed)
    ir = np.stack([filtre(r.standard_normal(n), passe_bas(ton)) * np.exp(-6.9 * t / rt) for _ in range(2)])
    ir[:, :int(.012 * SR)] = 0; ir /= np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))
    L = x.shape[1] + n; F = 1 << (L - 1).bit_length()
    y = np.stack([np.fft.irfft(np.fft.rfft(x[c], F) * np.fft.rfft(ir[c], F), F)[:x.shape[1]] for c in range(2)])
    return y


# ── Instruments ───────────────────────────────────────────────────────────
def piano(m, duree=3.0, dur=1.0):
    """Piano feutré : partiels légèrement inharmoniques, marteau doux, aigus amortis."""
    f = note(m); t = tt(duree); s = np.zeros_like(t)
    for k in range(1, 9):
        fk = k * f * np.sqrt(1 + .0004 * k * k)
        if fk > 9000: break
        s += np.sin(2 * np.pi * fk * t) * k ** -1.6 * np.exp(-t * (.9 + .55 * k) / dur)
    s *= np.minimum(1, t / .006)
    s += filtre(BRUIT[int(f * 7) % SR:int(f * 7) % SR + len(t)], passe_bas(1800)) * np.exp(-t * 60) * .05
    return s


def nappe(ms, duree, clarte=.4, att=.8):
    t = tt(duree); s = np.zeros_like(t)
    for j, m in enumerate(ms):
        for d in (-.07, .07):
            f = note(m) * 2 ** (d / 12)
            for k in range(1, 7): s += np.sin(2 * np.pi * k * f * t + j + k) * (clarte ** (k - 1)) / k
    return s * np.minimum(1, np.minimum(t / att, (duree - t) / .9).clip(0)) / max(1, len(ms))


def cloche(m, duree=2.2):
    t = tt(duree); f = note(m)
    return sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in ((1, 1, 2.2), (2.76, .45, 4.5), (5.4, .25, 8), (8.93, .1, 12))) * np.minimum(1, t / .002)


def pince(m, duree=.5):
    t = tt(duree); f = note(m)
    return (np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 18)) * env(len(t), .002, .12)


def grosse():
    t = tt(.45); return np.sin(2 * np.pi * np.cumsum(48 + 90 * np.exp(-t * 32)) / SR) * np.exp(-t * 7) + BRUIT[:len(t)] * np.exp(-t * 400) * .2


def claque(i0):
    t = tt(.25); return filtre(BRUIT[i0:i0 + len(t)], bande(1800, 1.1)) * np.exp(-t * 26)


def charley(i0):
    t = tt(.05); return filtre(BRUIT[i0:i0 + len(t)], passe_haut(7500)) * np.exp(-t * 110)


def papier(i0, d=.09, fc=2600):
    """Claque de feuille : bruit large, attaque sèche, petit corps grave."""
    t = tt(d + .12); x = filtre(BRUIT[i0:i0 + len(t)], bande(fc, 1.3)) * np.exp(-t / (d / 3))
    return x + .35 * np.sin(2 * np.pi * 110 * t) * np.exp(-t * 40)


def froisse(i0, d=.16):
    """Pli de papier : craquements épars filtrés + claquement final."""
    t = tt(d); g = np.random.default_rng(i0)
    imp = np.zeros(len(t)); idx = g.integers(0, len(t), 420); imp[idx] = g.standard_normal(420) * (1 - .6 * idx / len(t))
    x = filtre(np.convolve(imp, np.exp(-np.arange(80) / 12), 'same'), bande(3200, 1.4))
    x = x / (np.max(np.abs(x)) + 1e-9)
    corps = filtre(BRUIT[i0 % SR:i0 % SR + len(t)], bande(1800, 1.0)); corps /= np.max(np.abs(corps)) + 1e-9   # le souffle du papier qui bascule
    return (np.tanh(2.2 * x) * .8 + corps * .45 * np.sin(np.pi * t / d)) * np.minimum(1, t / .01)


def S(*xs):
    """Somme de sons de longueurs différentes (complétés par du silence)."""
    n = max(len(x) for x in xs); return sum(np.pad(x, (0, n - len(x))) for x in xs)


def coup(f0=55, d=1.2):
    t = tt(d); return np.sin(2 * np.pi * np.cumsum(f0 + 70 * np.exp(-t * 22)) / SR) * np.exp(-t * 3.2)


# ── Acte I : la nuit ──────────────────────────────────────────────────────
mus, sfx, amb = piste(), piste(), piste()
NUIT = [(50, [62, 65, 69]), (46, [62, 65, 70]), (53, [60, 65, 69]), (48, [60, 64, 67])]    # rém, sib, fa, do
FIN_NUIT = G['lev']
t, k = 0.9, 0
while t < FIN_NUIT - .5:
    b, acc = NUIT[k % 4]
    poser(mus, t, piano(b - 12, 4, 1.4), .55, -.2)
    for j, m in enumerate(acc):                                 # accord égrené, comme on joue tard le soir
        poser(mus, t + .32 * j + .05, piano(m, 3.2, 1.1), .32, -.3 + .3 * j)
    if k % 2 == 1: poser(mus, t + 1.45, piano(acc[-1] + 12, 2.6, .8), .2, .35)
    t += 2.6; k += 1
poser(mus, 0.9, nappe([38, 50], FIN_NUIT + .6, .25, 2.5), .32)
# chambre silencieuse, pendule qui s'arrête quand tout bascule
poser(amb, 0, filtre(BRUIT[:int(SR * FIN_NUIT)], passe_bas(500)) * .05)
t = 0.62
while t < G['balayage']:
    tt_ = tt(.03); poser(amb, t, filtre(BRUIT[int(t * 911) % SR:int(t * 911) % SR + len(tt_)], bande(4200, .5)) * np.exp(-tt_ * 160), .22 if int(t) % 2 else .16, .55)
    t += 1.0
# lampe : clic d'interrupteur
tc = tt(.12); poser(sfx, G['lampe'], filtre(BRUIT[100:100 + len(tc)], bande(3500, 1.2)) * np.exp(-tc * 90) + .5 * np.sin(2 * np.pi * 140 * tc) * np.exp(-tc * 50), .9, -.3)
for j, tp in enumerate(G['pile']): poser(sfx, tp, papier(2000 + j * 777, .08), .8 - .1 * j, -.4 + .1 * j)
poser(sfx, G['pile'][0] - .45, glissade(3333, .5, 900, 2600) * np.hanning(int(SR * .5)), .35, -.6)
# tampon « EN RETARD » : le coup sourd de l'encreur sur le bois
poser(sfx, G['tampon'], S(coup(70, .5) * 1.1, papier(5555, .05, 1500)), 1.0)
poser(sfx, G['glissePep'], glissade(4444, .62, 2600, 1100) * np.hanning(int(SR * .62)), .55, .6)
poser(sfx, G['glissePep'] + .55, papier(4747, .06), .45, .3)
poser(sfx, G['tamponPep'], S(coup(85, .4) * .7, papier(5656, .04, 1800) * .7), .8, .15)
poser(sfx, G['postit'], papier(6161, .05, 3400) * .7, .55, -.25)
# « vous ne la voyez plus » : la pièce s'étouffe
poser(sfx, G['flou'], np.sin(2 * np.pi * np.cumsum(220 * np.exp(-tt(1.4) * 1.6) + 40) / SR) * env(int(SR * 1.4), .05, .6), .45)
for a, b in G['vacille']:
    d = b - a + .02; ti = tt(d)
    poser(sfx, a, (np.sin(2 * np.pi * 100 * ti) + .5 * np.sin(2 * np.pi * 200 * ti) + .3 * np.sign(np.sin(2 * np.pi * 50 * ti))) * np.minimum(1, ti / .004) * np.minimum(1, (d - ti) / .004), .12, -.3)
    poser(sfx, a, papier(int(a * 1000) % SR, .02, 5000) * .3, .25, -.3)
# départ des autres feuilles
for j in range(3): poser(sfx, G['depart'] + j * .08, glissade(7000 + j * 333, .55, 1800, 700) * np.hanning(int(SR * .55)), .42, -.7 + .5 * j)
# balayage turquoise : un frisson de verre qui monte
d = 1.2; ti = tt(d); vb = sum(np.sin(2 * np.pi * np.cumsum(note(m) * (1 + .5 * ti / d)) / SR) for m in (86, 90, 93, 97)) / 4
poser(sfx, G['balayage'], vb * np.sin(np.pi * ti / d) ** 2 * .6 + glissade(8888, d, 3000, 9000) * np.sin(np.pi * ti / d) * .5, .35)
# lévitation : un bourdon qui monte, puis la montée vers « Pilotia »
d = G['pilotia'] - G['lev']; ti = tt(d)
poser(mus, G['lev'], np.sin(2 * np.pi * np.cumsum(55 * 2 ** (ti / d)) / SR) * (ti / d) ** 1.5 * .8, .6)
poser(sfx, G['pilotia'] - 1.3, glissade(9191, 1.3, 400, 7000) * tt(1.3) ** 2.4 / 1.3 ** 2.4, .4)

# ── Acte II : le pliage ───────────────────────────────────────────────────
tp = G['pilotia']
poser(sfx, tp, coup(50, 1.0) * .9, 1.0)
for m in (74, 81, 86): poser(mus, tp, cloche(m, 3.0), .22, (m - 80) / 10)
ECHELLE = [74, 77, 81, 84, 86, 89]
plis = piste()                                   # les plis ont leur propre piste (niveau réglé à part)
for j, tpl in enumerate(G['plis']):
    poser(plis, tpl - .1, froisse(12000 + j * 997, .16), 1.0, (-.4, .4)[j % 2])
    poser(plis, tpl, papier(13000 + j * 501, .03, 4000), .75, (-.3, .3)[j % 2])
    poser(mus, tpl, pince(ECHELLE[j], .6), .5, (-.25, .25)[j % 2])
poser(mus, G['ouvre'], nappe([62, 69, 74, 77], 1.4, .45, .3), .45)
poser(sfx, G['ouvre'], glissade(14000, .6, 600, 2400) * np.hanning(int(SR * .6)), .3)
# décollage : un souffle qui s'emballe et frôle l'objectif (gauche → droite)
d = G['coupe1'] - G['decol'] + .35; ti = tt(d); w = glissade(15000, d, 300, 5500, l=1.1) * (ti / d) ** 2.2 * np.minimum(1, (d - ti) / .3)
pan = np.clip((ti - (d - .45)) / .3, -1, 1)
poser(sfx, G['decol'], np.stack([w * np.cos((pan + 1) * np.pi / 4), w * np.sin((pan + 1) * np.pi / 4)]) * np.sqrt(2), 2.4)

# ── Acte III : l'aube ─────────────────────────────────────────────────────
AUBE = [(41, [65, 69, 72, 76]), (48, [64, 67, 72, 74]), (50, [62, 65, 69, 72]), (46, [62, 65, 70, 74])]   # fa, do, rém, sib (couleur add9/7)
T3 = G['pilotia'] + 12 * CRO                          # premier temps du groove, sur la grille des plis
FIN3 = G['coupe2']
bat, basse = piste(), piste()
GK = grosse()
t, n = T3, 0
while t < FIN3 - .05:
    mes, pos = n // 8, n % 8; b, acc = AUBE[mes % 4]
    if pos in (0, 4): poser(bat, t, GK, 1.0)
    if pos in (2, 6) and mes > 0: poser(bat, t, claque(int(t * 977) % SR), .45, .1)
    poser(bat, t, charley(int(t * 1301) % SR), .22 if pos % 2 else .12, .3)
    if pos % 2 == 0: poser(basse, t, np.sin(2 * np.pi * note(b - 12) * tt(.5)) * env(int(SR * .5), .005, .25) + .3 * np.sin(4 * np.pi * note(b - 12) * tt(.5)) * env(int(SR * .5), .005, .12), 1.0)
    arp = [acc[0], acc[2], acc[1], acc[3], acc[2], acc[0] + 12, acc[3], acc[1]]
    poser(mus, t, pince(arp[pos] + 12, .45), .28, (-.45, .45)[pos % 2])
    if pos == 0: poser(mus, t, nappe(acc, 8 * CRO + .3, .55, .25), .5)
    t += CRO; n += 1
poser(amb, G['aube'], filtre(BRUIT[SR:SR + int(SR * (FIN3 - G['aube']))], bande(700, 1.6)) * np.minimum(1, tt(FIN3 - G['aube']) / .5) * .5, .55)
poser(sfx, G['aube'], glissade(16000, 1.0, 4000, 600) * np.exp(-tt(1.0) * 5.5), .4)       # le souffle de la coupe s'ouvre en vent
for j, tf in enumerate(G['faisceaux']):
    poser(mus, tf, cloche((81, 84, 88, 89, 93)[j], 2.4), .6, (-.5, .1, .5, -.2, .6)[j])
    poser(sfx, tf, coup(45, .8) * .5, .65)
poser(sfx, G['cap'] - .25, glissade(17000, .7, 500, 3000) * np.hanning(int(SR * .7)), .45, -.2)
poser(sfx, G['cap'], coup(41, 1.6), .6)
for j, tm in enumerate(G['mois']): poser(mus, tm + .2, cloche((77, 79, 81)[j], 1.6), .12, -.3 + .3 * j)   # entre les mots, jamais dessus
for j, tk in enumerate(G['cartes']):
    poser(sfx, tk - .05, papier(18000 + j * 444, .07, 2200), .55, (-.5, .3, -.6, .1)[j])
    poser(sfx, tk - .25, glissade(19000 + j * 555, .35, 900, 3600) * np.hanning(int(SR * .35)), .3, (-.5, .3, -.6, .1)[j])
d = .45; poser(sfx, G['seul'] - d, glissade(20000, d, 600, 6000) * tt(d) ** 2 / d ** 2, .9)       # les cartes s'engouffrent
poser(sfx, G['seul'], S(coup(60, .9) * .9, cloche(93, 1.2) * .45), 1.1)
d = .4; poser(sfx, G['coupe2'] - d, glissade(21000, d + .15, 800, 7000) * np.sin(np.pi * np.minimum(1, tt(d + .15) / (d + .15))) ** 1.5, .7, .2)

# ── Acte IV : le logo ─────────────────────────────────────────────────────
t4 = G['point']
poser(mus, G['coupe2'], nappe([53, 60, 65, 69], DUREE - G['coupe2'], .35, 1.2), .42)
tq = tt(.12); poser(sfx, t4, np.sin(2 * np.pi * np.cumsum(500 + 900 * (1 - np.exp(-tq * 40))) / SR) * env(len(tq), .002, .04), .5)
poser(mus, t4, cloche(84, 2.0), .3, -.3)
d = G['traceFin'] - t4; ti = tt(d + .3)
chant = np.sin(2 * np.pi * np.cumsum(note(69) * 2 ** (np.minimum(1, ti / d) ** 1.2)) / SR) * np.minimum(1, ti / .15) * np.minimum(1, np.maximum(0, (d + .3 - ti) / .3))
poser(mus, t4, chant * .5 + glissade(22000, d + .3, 2000, 8000) * .05, .35, .1)
poser(sfx, G['cta'], S(papier(23000, .03, 3500) * .6, pince(93, .3) * .4), .45, .2)
poser(sfx, G['fleche'], S(papier(24000, .04, 4200), coup(55, 1.0) * .6), .75)
poser(mus, G['fleche'], cloche(93, 2.4), .3, .3)
tm = G['marque']; FINAL = [41, 53, 60, 65, 69, 72, 76]
for j, m in enumerate(FINAL): poser(mus, tm + .015 * j, piano(m, DUREE - tm + .2, 2.6), .42 if m > 50 else .6, -.4 + .13 * j)
poser(mus, tm, nappe([65, 69, 72, 76], DUREE - tm, .5, .6), .5)
poser(sfx, tm, coup(41, 2.5) * .8, .7)

# ── Voix : lecture, mise en forme, creusement de la musique ──────────────
brut = subprocess.run([FFMPEG, '-v', 'error', '-i', VOIX, '-ac', '1', '-ar', str(SR), '-f', 'f64le', '-'], capture_output=True, check=True).stdout
v = np.frombuffer(brut, np.float64)[:N]; v = np.pad(v, (0, N - len(v)))
v = filtre(v, lambda f: passe_haut(85)(f) * (1 + .33 * np.exp(-.5 * (np.log2(np.maximum(f, 1) / 3500) / .7) ** 2)))   # présence +2,5 dB
e = np.sqrt(np.convolve(v ** 2, np.ones(int(.01 * SR)) / int(.01 * SR), 'same'))
seuil = .5 * np.percentile(e[e > 1e-4], 90); gr = np.minimum(1, (np.maximum(e, seuil) / seuil) ** (-(1 - 1 / 2.5)))   # compression douce 2,5:1
v *= np.convolve(gr, np.ones(int(.02 * SR)) / int(.02 * SR), 'same')
voix = np.stack([v, v]); voix = voix + .07 * reverb(voix, 1.1, 3, 4000)
# enveloppe de la voix (attaque 20 ms, relâche 300 ms) -> creusement
ev = np.abs(v); lis = np.zeros_like(ev); a_, r_ = np.exp(-1 / (.02 * SR)), np.exp(-1 / (.3 * SR)); acc_ = 0.0
blk = 64
for i in range(0, N, blk):
    x = ev[i:i + blk].max(); acc_ = (a_ ** blk) * acc_ + (1 - a_ ** blk) * x if x > acc_ else (r_ ** blk) * acc_ + (1 - r_ ** blk) * x; lis[i:i + blk] = acc_
lis /= np.percentile(lis[lis > 1e-4], 95)
creux = 1 - .65 * np.clip(lis, 0, 1)            # jusqu'à −9 dB sous la voix

# la pièce s'étouffe pendant le flou (mélange vers une version passe-bas)
w = np.zeros(N); a, b = int(G['flou'] * SR), int(G['flouFin'] * SR); w[a:b] = np.sin(np.pi * np.linspace(0, 1, b - a)) ** .6
mus = mus * (1 - w) + filtre(mus, passe_bas(500)) * w
mus = mus + .28 * reverb(mus, 2.6, 5, 5000); sfx = sfx + .15 * reverb(sfx, 1.6, 9, 6000)
bat = bat + .1 * reverb(bat, 1.2, 11, 6000)
# fondu final
fade = np.ones(N); i0 = int((DUREE - 1.2) * SR); fade[i0:] = np.linspace(1, 0, N - i0) ** 1.6
mix = (normaliser(mus, .5) * creux + normaliser(bat, .42) * (.45 + .55 * creux) + normaliser(basse, .36) * creux
       + normaliser(amb, .16) + normaliser(sfx, .62) * (.7 + .3 * creux) + normaliser(plis, .85) + normaliser(voix, .95)) * fade
mix = normaliser(np.tanh(1.3 * normaliser(mix, .9)), .89)
with wave.open(SORTIE, 'wb') as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix.T * 32767).astype('<i2').tobytes())
print(f'{SORTIE} : {DUREE:.2f} s')
