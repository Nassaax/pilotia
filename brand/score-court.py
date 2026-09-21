# -*- coding: utf-8 -*-
"""Bande-son d'un film court Pilotia.

Entierement synthetisee : aucun echantillon tiers, donc aucune licence a
declarer et aucun risque de revendication sur les reseaux.

Usage :
    python3 score-court.py <sortie.wav> <duree> <impacts> <resolution>
    python3 score-court.py court.wav 15.4 5.15,5.75,6.85 14.05

Le volume est de l'arithmetique, pas du gout : chaque element est normalise
a une crete connue AVANT le melange, et le master est mesure apres coup
(cible -14 LUFS, crete vraie <= -1 dBTP, la norme de diffusion d'Instagram).
"""
import sys, wave
import numpy as np

SR = 48000


def construire(duree, impacts, resolution):
    n = int(SR * duree)
    t = np.arange(n) / SR
    rng = np.random.default_rng(20260921)      # graine fixe : reproductible

    def sine(f):
        return np.sin(2 * np.pi * f * t)

    def env(t0, attaque, maintien, chute):
        e = np.zeros(n)
        i = [min(max(int(x * SR), 0), n) for x in
             (t0, t0 + attaque, t0 + attaque + maintien,
              t0 + attaque + maintien + chute)]
        if i[1] > i[0]: e[i[0]:i[1]] = np.linspace(0, 1, i[1] - i[0])
        if i[2] > i[1]: e[i[1]:i[2]] = 1.0
        if i[3] > i[2]: e[i[2]:i[3]] = np.linspace(1, 0, i[3] - i[2])
        return e

    # nappe grave, presente tout du long
    pad = 0.55 * sine(55.0) + 0.42 * sine(82.41) + 0.30 * sine(110.0) + 0.10 * sine(110.6)
    pad *= 0.78 + 0.22 * np.sin(2 * np.pi * 0.075 * t)
    pad *= env(0.0, 1.6, max(duree - 3.4, 0.1), 1.8)

    # frappes : un corps grave qui decroit, plus un transitoire de souffle
    coups = np.zeros(n)
    for k, t0 in enumerate(impacts):
        d = np.maximum(t - t0, 0)
        actif = (t >= t0)
        corps = np.sin(2 * np.pi * (74.0 - 4.0 * k) * d) * np.exp(-d * 7.5) * actif
        souffle = rng.standard_normal(n) * np.exp(-d * 52) * actif
        coups += (0.74 + 0.07 * k) * (0.85 * corps + 0.13 * souffle)

    # resolution : un accord qui s'ouvre sur le logotype
    accord = (0.42 * sine(110.0) + 0.34 * sine(164.81) + 0.26 * sine(220.0)
              + 0.16 * sine(277.18) + 0.10 * sine(329.63))
    accord *= env(resolution, 1.1, 0.5, max(duree - resolution - 1.6, 0.4))

    def cale(x, cible):
        c = float(np.max(np.abs(x)))
        return x * (cible / c) if c > 1e-9 else x

    mix = cale(pad, 0.52) + cale(coups, 0.62) + cale(accord, 0.48)
    mix *= env(0.0, 0.5, max(duree - 1.2, 0.1), 0.7)

    large = cale(pad, 0.52)
    st = np.stack([mix + 0.045 * np.roll(large, 240),
                   mix - 0.045 * np.roll(large, 240)], axis=1)
    crete = float(np.max(np.abs(st)))
    return st / crete * 0.82, crete


def main():
    sortie = sys.argv[1]
    duree = float(sys.argv[2])
    impacts = [float(x) for x in sys.argv[3].split(',')] if sys.argv[3] else []
    resolution = float(sys.argv[4])

    st, crete = construire(duree, impacts, resolution)
    with wave.open(sortie, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype('<i2').tobytes())
    print(f'{sortie} : {duree:.2f} s, {len(impacts)} frappe(s), '
          f'crete avant normalisation {crete:.3f}')


if __name__ == '__main__':
    main()
