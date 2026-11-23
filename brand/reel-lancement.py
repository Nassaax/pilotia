# -*- coding: utf-8 -*-
"""Assemble le Reel « Bienvenue chez Pilotia » : plans filmés + calque motion design + bande-son.

    python3 brand/reel-lancement.py <dossier des rushs> <dossier de sortie>

Le site doit être servi en local sur http://127.0.0.1:8765 (python3 -m http.server
8765 à la racine du dépôt). Les rushs sont des vidéos libres de droits, sans son,
fournies par le fondateur ; ils ne sont pas versionnés. On les reconnaît au numéro
de la banque d'images contenu dans leur nom de fichier.

30 s à 120 bpm : chaque coupe tombe sur un temps (0,5 s). Chaque plan est recadré
en 9:16 avec un lent panoramique ; les plans rapides entrent avec un léger « coup de
zoom », les plans calmes avancent doucement, le plan de l'avalanche tremble.
Livrables : pilotia-reel-lancement.mp4 (avec la bande-son de brand/score-lancement.py,
-14 LUFS), pilotia-reel-lancement-sans-musique.mp4 (pour poser une musique Instagram),
et pilotia-reel-lancement-couverture.jpg.
"""
import json
import pathlib
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
IPS = 30

# Rushs, par numéro de la banque d'images :
RUSHS = {
    'equipe': '273921',         # open space, quatre personnes
    'telephone': '202987',      # mains sur un téléphone, dans le noir
    'classeur': '11862',        # une femme trie des classeurs
    'bureau': '293084',         # vue de dessus : café, calculatrice, graphiques
    'clavier': '6878288',       # mains sur un clavier, appareil photo à côté
    'camera': '6878291',        # même bureau, autre angle (720p)
    'tournage': '9032607',      # une femme filmée par un appareil sur trépied
    'equipe-femmes': '7490508', # vertical : une équipe sourit autour de documents
    'code': '15406860',         # écran de code, mains sur le clavier
    'site-code': '8523655',     # portable : une page web, puis du code
    'design': '7610994',        # vertical : création graphique sur portable
    'maison': '5585983',        # vertical : une femme travaille au calme, chez elle
}

# Plans : (rush, début dans le rush, durée, cadre au début et à la fin de 0 à 1, mouvement)
PLANS = [
    ('equipe', 1.0, 1.0, .15, .35, 'coup'),        # 0-4 s : accroche, une coupe par seconde
    ('telephone', 2.0, 1.0, .45, .55, 'coup'),
    ('classeur', 3.0, 1.0, .30, .42, 'coup'),
    ('bureau', 1.0, 1.0, .50, .62, 'coup'),
    ('clavier', 3.0, 2.0, .58, .45, 'coup'),       # 4-8 s : avalanche de tâches
    ('camera', 2.0, 2.0, .50, .38, 'tremble'),
    ('maison', 0.0, 4.0, .50, .50, 'lent'),        # 8-12 s : « Respirez »
    ('bureau', 8.0, 2.0, .30, .48, 'coup'),        # 12-22 s : cinq savoir-faire
    ('site-code', 0.5, 2.0, .45, .60, 'coup'),
    ('telephone', 8.0, 2.0, .40, .52, 'coup'),
    ('tournage', 1.0, 2.0, .30, .48, 'coup'),
    ('design', 3.0, 1.0, .50, .50, 'coup'),
    ('code', 3.0, 1.0, .40, .55, 'coup'),
    ('equipe-femmes', 2.0, 8.0, .50, .50, 'lent'), # 22-30 s : publics, puis abonnement
]


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True)


def plan(rushs, rush, debut, duree, p0, p1, mouvement, sortie):
    source = next(rushs.glob(f'*{RUSHS[rush]}*.mp4'))
    images = round(duree * IPS)
    zoom = {'coup': '1+0.09*max(0,1-on/9)',
            'lent': f'1+0.07*on/{images}',
            'tremble': '1.05'}[mouvement]
    # Le tremblement monte dans la dernière seconde du plan, sous les tâches qui secouent.
    secousse = f'+28*sin(on*2.1)*max(0,(on-{images - 33})/33)' if mouvement == 'tremble' else ''
    filtre = (f"fps={IPS},scale=-2:1920:flags=lanczos,"
              f"crop=1080:1920:x='(iw-1080)*({p0}+({p1}-{p0})*t/{duree})':y=0,"
              f"scale=2160:3840:flags=lanczos,"
              f"zoompan=z='{zoom}':x='iw/2-iw/zoom/2{secousse}':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps={IPS},"
              f"tpad=stop_mode=clone:stop_duration=1,"
              f"eq=contrast=1.08:saturation=1.1,vignette=PI/6,setsar=1,format=yuv420p")
    ffmpeg('-ss', str(debut), '-t', str(duree + 0.5), '-i', str(source), '-an', '-vf', filtre,
           '-frames:v', str(images), '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', str(sortie))


def main():
    rushs, sortie = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    travail = sortie / '_lancement'
    travail.mkdir(parents=True, exist_ok=True)

    calque = travail / 'calque'
    subprocess.run(['node', str(ICI / 'reels-terrain-calque.js'), 'http://127.0.0.1:8765', 'lancement',
                    str(calque), str(IPS), 'reel-lancement.html'], check=True)
    infos = json.loads((calque / 'infos.json').read_text())

    morceaux = []
    for i, p in enumerate(PLANS):
        f = travail / f'plan{i:02d}.mp4'
        plan(rushs, *p, f)
        morceaux.append(f)
    liste = travail / 'plans.txt'
    liste.write_text(''.join(f"file '{f}'\n" for f in morceaux))
    video = travail / 'video.mp4'
    ffmpeg('-f', 'concat', '-safe', '0', '-i', str(liste), '-t', str(infos['duree']),
           '-c:v', 'libx264', '-crf', '16', str(video))

    son = travail / 'son.wav'
    subprocess.run([sys.executable, str(ICI / 'score-lancement.py'), str(son), str(infos['duree']),
                    ','.join(str(x) for x in infos['impacts']), str(infos['fin']),
                    ','.join(str(x) for x in infos['souffles'])], check=True)
    mesure = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(son), '-af',
                             'loudnorm=I=-14:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'],
                            capture_output=True, text=True).stderr
    m = json.loads(mesure[mesure.rindex('{'):mesure.rindex('}') + 1])
    master = travail / 'master.wav'
    ffmpeg('-i', str(son), '-af',
           f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
           f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
           "aresample=48000", str(master))

    image = travail / 'image.mp4'
    ffmpeg('-i', str(video), '-framerate', str(IPS), '-i', str(calque / '%05d.png'),
           '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]', '-map', '[v]',
           '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-profile:v', 'high',
           '-t', str(infos['duree']), str(image))
    final = sortie / 'pilotia-reel-lancement.mp4'
    # -0,6 dB : l'encodage AAC fait remonter la crête ; on la garde sous -1 dBFS.
    ffmpeg('-i', str(image), '-i', str(master), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
           '-af', 'volume=-0.6dB', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(infos['duree']), str(final))
    ffmpeg('-i', str(image), '-c:v', 'copy', '-an', '-movflags', '+faststart',
           str(sortie / 'pilotia-reel-lancement-sans-musique.mp4'))
    # Couverture : l'accroche entière à l'écran.
    ffmpeg('-ss', '3.2', '-i', str(final), '-frames:v', '1', '-q:v', '2',
           str(sortie / 'pilotia-reel-lancement-couverture.jpg'))
    print(final)


if __name__ == '__main__':
    main()
