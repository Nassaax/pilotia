# -*- coding: utf-8 -*-
"""Assemble les Reels terrain : plans filmés + calque de texte + bande-son.

    python3 brand/reels-terrain.py <dossier des rushs> <dossier de sortie> [reel …]

Chaque Reel dure 30 s : deux chutes humoristiques, la réponse de Pilotia,
puis une carte de fin d'environ 5 s.

Le site doit être servi en local sur http://127.0.0.1:8765 (python3 -m
http.server 8765 à la racine du dépôt). Les rushs sont des vidéos libres de
droits, sans son, fournies par le fondateur ; ils ne sont pas versionnés.

Pour chaque Reel : chaque plan est recadré en 9:16 avec un lent panoramique,
légèrement étalonné, puis le calque (brand/reels-terrain.html) est posé dessus
et la bande-son (brand/score-terrain.py) masterisée à -14 LUFS, crête vraie
-1 dBTP. Livrables : <reel>.mp4 et <reel>-couverture.jpg.
"""
import json
import pathlib
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
IPS = 30

# Rushs (préfixe du nom de fichier) :
#   bureau   vue de dessus, café, calculatrice, graphiques, ordinateur
#   classeur une femme trie des classeurs
#   equipe   un open space, quatre personnes au travail
#   soir     un homme en cravate devant son ordinateur, bureau sombre
#   telephone des mains sur un téléphone, dans le noir
#   clavier  des mains sur un clavier d'ordinateur portable
RUSHS = {'bureau': '2d048d1e', 'classeur': '36705734', 'equipe': '7c0a60c5',
         'soir': '95546009', 'telephone': '9c34d59b', 'clavier': 'a0fdf15d'}

# Plans : (rush, début dans le rush, durée, position du cadre au début et à la fin,
# de 0 = bord gauche à 1 = bord droit de l'image recadrée).
MONTAGES = {
    'administratif': [('soir', 0.5, 9.0, 0.18, 0.32), ('bureau', 2.0, 9.0, 0.40, 0.62),
                      ('clavier', 4.0, 12.0, 0.58, 0.42)],
    'papiers': [('classeur', 1.0, 14.0, 0.25, 0.45), ('bureau', 4.0, 16.0, 0.62, 0.40)],
    'budget': [('telephone', 0.0, 15.0, 0.40, 0.58), ('bureau', 4.0, 15.0, 0.30, 0.55)],
    'renfort': [('equipe', 0.0, 8.0, 0.10, 0.90), ('soir', 8.0, 7.0, 0.25, 0.35),
                ('clavier', 7.0, 15.0, 0.50, 0.35)],
    'projet': [('clavier', 0.0, 8.0, 0.40, 0.60), ('telephone', 6.0, 6.0, 0.50, 0.40),
               ('bureau', 3.0, 16.0, 0.60, 0.35)],
}


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True)


def plan(rushs, rush, debut, duree, p0, p1, sortie):
    source = next(rushs.glob(RUSHS[rush] + '*.mp4'))
    filtre = (f"scale=-2:1920,crop=1080:1920:x='(iw-1080)*({p0}+({p1}-{p0})*t/{duree})':y=0,"
              f"fps={IPS},eq=contrast=1.06:saturation=0.92:brightness=-0.02,"
              f"vignette=PI/5,setsar=1,format=yuv420p")
    ffmpeg('-ss', str(debut), '-t', str(duree), '-i', str(source), '-an', '-vf', filtre,
           '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', str(sortie))


def assembler(rushs, sortie, reel):
    travail = sortie / f'_{reel}'
    travail.mkdir(parents=True, exist_ok=True)
    calque = travail / 'calque'
    subprocess.run(['node', str(ICI / 'reels-terrain-calque.js'), 'http://127.0.0.1:8765', reel,
                    str(calque), str(IPS)], check=True)
    infos = json.loads((calque / 'infos.json').read_text())

    morceaux = []
    for i, m in enumerate(MONTAGES[reel]):
        f = travail / f'plan{i}.mp4'
        plan(rushs, *m, f)
        morceaux.append(f)
    liste = travail / 'plans.txt'
    liste.write_text(''.join(f"file '{f}'\n" for f in morceaux))
    video = travail / 'video.mp4'
    ffmpeg('-f', 'concat', '-safe', '0', '-i', str(liste), '-t', str(infos['duree']),
           '-c:v', 'libx264', '-crf', '16', str(video))

    son = travail / 'son.wav'
    subprocess.run([sys.executable, str(ICI / 'score-terrain.py'), str(son), str(infos['duree']),
                    ','.join(str(x) for x in infos['impacts']), str(infos['fin'])], check=True)
    # Master en deux passes : loudnorm mesure, puis corrige vers -14 LUFS / -1 dBTP.
    mesure = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(son), '-af',
                             'loudnorm=I=-14:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'],
                            capture_output=True, text=True).stderr
    m = json.loads(mesure[mesure.rindex('{'):mesure.rindex('}') + 1])
    master = travail / 'master.wav'
    ffmpeg('-i', str(son), '-af',
           f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
           f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
           "aresample=48000", str(master))

    final = sortie / f'pilotia-reel-{reel}.mp4'
    ffmpeg('-i', str(video), '-framerate', str(IPS), '-i', str(calque / '%05d.png'), '-i', str(master),
           '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]',
           '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
           '-profile:v', 'high', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
           '-t', str(infos['duree']), str(final))
    # Couverture : l'image où l'accroche est posée et lisible.
    ffmpeg('-ss', '2.2', '-i', str(final), '-frames:v', '1', '-q:v', '2',
           str(sortie / f'pilotia-reel-{reel}-couverture.jpg'))
    return final


def main():
    rushs, sortie = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    sortie.mkdir(parents=True, exist_ok=True)
    for reel in (sys.argv[3:] or list(MONTAGES)):
        print(assembler(rushs, sortie, reel))


if __name__ == '__main__':
    main()
