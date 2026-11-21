# -*- coding: utf-8 -*-
"""Bande-son des Reels terrain Pilotia.

Entierement synthetisee (aucun echantillon tiers) : aucune licence a declarer,
aucun risque de revendication sur les reseaux. Un groove pop leger a 112 bpm
(grosse caisse, caisse claire, charleston, basse, accords en contretemps), une
claque d'autocollant a chaque carte qui arrive, puis un carillon sur la carte
de fin, ou la batterie s'arrete.

Usage :
    python3 score-terrain.py <sortie.wav> <duree> <impacts> <fin>
    python3 score-terrain.py reel.wav 15 0.15,0.55,3.6,6.2,8.4 11.6

Le master (-14 LUFS, crete vraie <= -1 dBTP) se fait ensuite avec ffmpeg
loudnorm en deux passes, et se mesure sur le fichier livre.
"""
import sys, wave
import numpy as np

SR = 48000
BPM = 112


def construire(duree, impacts, fin):
    n = int(SR * duree)
    t = np.arange(n) / SR
    rng = np.random.default_rng(20261116)      # graine fixe : reproductible
    temps = 60.0 / BPM
    sortie = np.zeros(n)

    def coller(signal, t0, gain):
        i = int(t0 * SR)
        if i >= n: return
        m = min(len(signal), n - i)
        sortie[i:i + m] += gain * signal[:m]

    def son(longueur):
        return np.arange(int(longueur * SR)) / SR

    # Batterie, jusqu'a la fin (une mesure de 4 temps)
    x = son(0.4)
    grosse = np.sin(2 * np.pi * (48 + 70 * np.exp(-x * 28)) * x) * np.exp(-x * 9)
    x2 = son(0.25)
    claire = (0.6 * rng.standard_normal(len(x2)) + 0.5 * np.sin(2 * np.pi * 190 * x2)) * np.exp(-x2 * 22)
    x3 = son(0.06)
    bruit = rng.standard_normal(len(x3))
    charleston = (bruit - np.convolve(bruit, np.ones(6) / 6, 'same')) * np.exp(-x3 * 70)
    k = 0
    while k * temps < fin - 0.3:
        t0 = k * temps
        if k % 4 in (0, 2): coller(grosse, t0, 0.95)
        if k % 4 in (1, 3): coller(claire, t0, 0.42)
        coller(charleston, t0 + temps / 2, 0.28)
        coller(charleston, t0, 0.16)
        k += 1

    # Basse et accords : do, sol, la mineur, fa, une mesure chacun
    grille = [(65.41, (261.63, 329.63, 392.00)), (98.00, (246.94, 293.66, 392.00)),
              (110.0, (261.63, 329.63, 440.00)), (87.31, (261.63, 349.23, 440.00))]
    mesure = 4 * temps
    m = 0
    while m * mesure < fin:
        racine, accord = grille[m % 4]
        for b in range(4):
            t0 = m * mesure + b * temps
            if t0 >= fin - 0.1: break
            xb = son(temps * 0.9)
            basse = (np.sin(2 * np.pi * racine * xb) + 0.3 * np.sin(2 * np.pi * 2 * racine * xb)) * np.exp(-xb * 3.2)
            coller(basse, t0, 0.55)
            xs = son(0.18)
            stab = sum(np.sin(2 * np.pi * f * xs) + 0.25 * np.sin(2 * np.pi * 2 * f * xs) for f in accord)
            coller(stab * np.exp(-xs * 16), t0 + temps / 2, 0.16)
        m += 1

    # Claque d'autocollant a chaque carte : souffle aigu + petit « pop » qui monte
    xc = son(0.16)
    souffle = rng.standard_normal(len(xc))
    souffle = souffle - np.convolve(souffle, np.ones(4) / 4, 'same')
    pop = np.sin(2 * np.pi * (520 + 900 * xc) * xc)
    claque = (0.7 * souffle * np.exp(-xc * 60) + 0.6 * pop * np.exp(-xc * 26))
    for t0 in impacts:
        coller(claque, t0, 0.55)

    # Carillon de fin : do, mi, sol, do
    for j, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
        xf = son(2.2)
        cloche = (np.sin(2 * np.pi * f * xf) + 0.35 * np.sin(2 * np.pi * 2.76 * f * xf)) * np.exp(-xf * 2.4)
        coller(cloche, fin + 0.08 * j, 0.32)
    xa = son(max(duree - fin, 0.5))
    nappe = sum(np.sin(2 * np.pi * f * xa) for f in (130.81, 196.0, 261.63, 329.63))
    coller(nappe * np.minimum(xa / 0.3, 1) * np.exp(-xa * 0.6), fin, 0.12)

    # Fondu d'entree et de sortie
    enveloppe = np.minimum(1, t / 0.05) * np.minimum(1, np.maximum(duree - t, 0) / 0.6)
    sortie *= enveloppe
    st = np.stack([sortie, np.roll(sortie, 96)], axis=1)
    crete = float(np.max(np.abs(st)))
    return st / crete * 0.8, crete


def main():
    sortie = sys.argv[1]
    duree = float(sys.argv[2])
    impacts = [float(x) for x in sys.argv[3].split(',')] if sys.argv[3] else []
    fin = float(sys.argv[4])
    st, crete = construire(duree, impacts, fin)
    with wave.open(sortie, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype('<i2').tobytes())
    print(f'{sortie} : {duree:.2f} s, {len(impacts)} claque(s), fin a {fin:.2f} s')


if __name__ == '__main__':
    main()
