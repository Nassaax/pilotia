# -*- coding: utf-8 -*-
"""Bande-son du Reel « Bienvenue chez Pilotia » (brand/reel-lancement.html).

Entierement synthetisee (aucun echantillon tiers) : aucune licence a declarer.
Tempo 120 bpm (un temps = 0,5 s), calque sur les coupes du montage :
  0-4 s    accroche : batterie legere et accords, sans basse
  4-8 s    avalanche : basse, charleston en doubles croches, montee de bruit,
           silence d'un demi-temps juste avant la coupe
  8 s      impact grave (« Respirez »), 8-12 s : demi-tempo, nappe, roulement final
  12-25,5  groove complet (savoir-faire, publics), souffle a chaque transition
  25,5 s   carillon de fin, la batterie s'arrete
Une claque d'autocollant a chaque carte qui arrive (liste fournie par le calque).

Usage :
    python3 score-lancement.py <sortie.wav> <duree> <impacts> <fin> <souffles>
Le master (-14 LUFS) se fait ensuite avec ffmpeg loudnorm en deux passes.
"""
import sys, wave
import numpy as np

SR = 48000
BPM = 120
TEMPS = 60.0 / BPM


def construire(duree, impacts, fin, souffles):
    n = int(SR * duree)
    t = np.arange(n) / SR
    rng = np.random.default_rng(20261123)      # graine fixe : reproductible
    sortie = np.zeros(n)

    def coller(signal, t0, gain):
        i = int(round(t0 * SR))
        if i >= n or i + len(signal) <= 0: return
        a = max(0, -i); i = max(i, 0)
        m = min(len(signal) - a, n - i)
        sortie[i:i + m] += gain * signal[a:a + m]

    def son(longueur):
        return np.arange(int(longueur * SR)) / SR

    def aigu(x):          # bruit sans ses graves (soustraction d'une moyenne glissante)
        return x - np.convolve(x, np.ones(8) / 8, 'same')

    x = son(0.45)
    grosse = np.sin(2 * np.pi * (50 + 90 * np.exp(-x * 30)) * x) * np.exp(-x * 8)
    xc = son(0.22)
    clap = sum(np.roll(aigu(rng.standard_normal(len(xc))) * np.exp(-xc * 30), int(SR * d)) for d in (0, .008, .017))
    xh = son(0.05)
    charleston = aigu(rng.standard_normal(len(xh))) * np.exp(-xh * 80)
    xo = son(0.18)
    ouvert = aigu(rng.standard_normal(len(xo))) * np.exp(-xo * 18)

    # Grille d'accords, une mesure (2 s) chacun : do, sol, la mineur, fa
    grille = [(65.41, (261.63, 329.63, 392.00)), (98.00, (246.94, 293.66, 392.00)),
              (110.0, (261.63, 329.63, 440.00)), (87.31, (261.63, 349.23, 440.00))]

    def section(k):
        tb = k * TEMPS
        if tb < 4: return 'accroche'
        if tb < 7.75: return 'avalanche'
        if tb < 8: return 'silence'
        if tb < 12: return 'respire'
        if tb < fin - .05: return 'groove'
        return 'fin'

    k = 0
    while k * TEMPS < duree:
        t0, s, temps_mesure = k * TEMPS, section(k), k % 4
        racine, accord = grille[(k // 4) % 4]
        if s in ('accroche', 'avalanche', 'groove'):
            coller(grosse, t0, 0.9 if s != 'accroche' else 0.7)
            if temps_mesure in (1, 3): coller(clap, t0, 0.38)
            coller(ouvert, t0 + TEMPS / 2, 0.16)
            if s != 'accroche':
                for d in (0.25, 0.75): coller(charleston, t0 + d * TEMPS, 0.14 if s == 'groove' else 0.2)
                xb = son(TEMPS * 0.45)
                basse = (np.sin(2 * np.pi * racine * xb) + 0.35 * np.sin(2 * np.pi * 2 * racine * xb)) * np.exp(-xb * 5)
                coller(basse, t0, 0.6)
                coller(basse * 0.8, t0 + TEMPS / 2, 0.45)   # rebond a l'octave en croches
            xs = son(0.16)
            stab = sum(np.sin(2 * np.pi * f * xs) + 0.3 * np.sin(2 * np.pi * 2 * f * xs) for f in accord)
            coller(stab * np.exp(-xs * 18), t0 + TEMPS * 0.5, 0.15)
        elif s == 'respire':
            if temps_mesure == 0: coller(grosse, t0, 0.75)
            if temps_mesure == 2: coller(clap, t0, 0.22)
            if temps_mesure == 0:
                xa = son(2 * TEMPS * 4 * 0.98)
                nappe = sum(np.sin(2 * np.pi * f * xa) for f in accord)
                coller(nappe * np.minimum(xa / .3, 1) * np.exp(-xa * .5), t0, 0.07)
                coller(np.sin(2 * np.pi * racine * son(1.6)) * np.exp(-son(1.6) * 1.5), t0, 0.4)
        k += 1

    # Montee de bruit avant la coupure de 8 s, et roulement de caisse avant 12 s
    debut, longueur = 5.5, 2.25
    xr = son(longueur)
    montee = aigu(rng.standard_normal(len(xr))) * (xr / longueur) ** 2
    montee += 0.25 * np.sin(2 * np.pi * (200 + 900 * (xr / longueur) ** 2) * xr) * (xr / longueur) ** 2
    coller(montee, debut, 0.35)
    for j in range(16):
        coller(clap, 11.0 + j * TEMPS / 8, 0.06 + 0.012 * j)   # triples croches, crescendo

    # Impact grave a 8 s
    xi = son(1.4)
    boum = np.sin(2 * np.pi * (36 + 60 * np.exp(-xi * 6)) * xi) * np.exp(-xi * 2.6)
    coller(boum, 8.0, 1.1)
    coller(aigu(rng.standard_normal(len(son(.5)))) * np.exp(-son(.5) * 9), 8.0, 0.3)

    # Souffle a chaque transition (barres, bandeaux)
    xw = son(0.6)
    souffle = aigu(rng.standard_normal(len(xw))) * np.sin(np.pi * xw / 0.6) ** 2
    for c in souffles:
        coller(souffle, c - 0.3, 0.3)

    # Claque d'autocollant a chaque carte
    xk = son(0.16)
    pop = np.sin(2 * np.pi * (520 + 900 * xk) * xk)
    claque = 0.7 * aigu(rng.standard_normal(len(xk))) * np.exp(-xk * 60) + 0.6 * pop * np.exp(-xk * 26)
    for c in impacts:
        coller(claque, c, 0.42)

    # Fin : carillon do, mi, sol, do et nappe
    for j, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
        xf = son(2.4)
        cloche = (np.sin(2 * np.pi * f * xf) + 0.35 * np.sin(2 * np.pi * 2.76 * f * xf)) * np.exp(-xf * 2.2)
        coller(cloche, fin + 0.08 * j, 0.3)
    xa = son(max(duree - fin, 0.5))
    nappe = sum(np.sin(2 * np.pi * f * xa) for f in (130.81, 196.0, 261.63, 329.63))
    coller(nappe * np.minimum(xa / 0.3, 1) * np.exp(-xa * 0.45), fin, 0.12)

    enveloppe = np.minimum(1, t / 0.03) * np.minimum(1, np.maximum(duree - t, 0) / 0.8)
    sortie *= enveloppe
    st = np.stack([sortie, np.roll(sortie, 96)], axis=1)
    return st / float(np.max(np.abs(st))) * 0.8


def main():
    sortie, duree = sys.argv[1], float(sys.argv[2])
    impacts = [float(x) for x in sys.argv[3].split(',') if x]
    fin = float(sys.argv[4])
    souffles = [float(x) for x in sys.argv[5].split(',') if x]
    st = construire(duree, impacts, fin, souffles)
    with wave.open(sortie, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype('<i2').tobytes())
    print(f'{sortie} : {duree:.2f} s, {len(impacts)} claque(s), {len(souffles)} souffle(s), fin a {fin:.2f} s')


if __name__ == '__main__':
    main()
