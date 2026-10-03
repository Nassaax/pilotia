# Norme vidéo Pilotia

Demande explicite du fondateur (octobre 2026) : **chaque nouvelle vidéo doit
atteindre au minimum le niveau du film n° 6 « Prenez de la hauteur »**
(voix off française, vraie 3D, effets travaillés). Ce document est la
référence à relire **avant** de commencer toute vidéo, et à appliquer en
entier. Une vidéo qui ne coche pas tout n'est pas livrée comme finie : on
dit ce qui manque.

## 1. Direction (avant toute image)

- [ ] Un brief : public, **une seule** affirmation, sujet jamais traité par
      les films précédents (voir le journal des films dans `charte-social.md`).
- [ ] Trois pistes visuelles réellement différentes, deux tuées par écrit
      (`film-*-DIRECTION.md`), avec la raison de chaque mise à mort.
- [ ] Un geste signature qu'on peut nommer en une phrase, et qui n'existe
      dans aucun film précédent.
- [ ] Liste des chiffres autorisés, tous repris du site. Aucun chiffre
      inventé, aucun faux avis, aucun nom de partenaire d'affacturage,
      aucun conseil fiscal. Pas de tiret long dans les textes à l'écran.

## 2. Voix off française (par défaut, sauf film volontairement muet)

- [ ] Script écrit pour l'oreille : une idée par phrase, l'affirmation dans
      les 10 premières secondes, un appel à l'action à la fin.
- [ ] Voix synthétisée **avant** l'image ; la durée des plans vient de la
      voix réelle. Moteur actuel : Kokoro (voix française `ff_siwis`),
      phrase par phrase, silences choisis à la main (`film-avion-voix.py`).
- [ ] Prononciation vérifiée par transcription automatique (Whisper) ;
      corriger par phonèmes imposés les mots mal compris (ex. « Pilotia »
      dit `pilotiˈa`, toujours précédé d'un mot : « avec Pilotia »).
- [ ] Instant de chaque mot lu dans le modèle de voix (durées de phonèmes),
      jamais estimé. Chaque apparition à l'écran part du mot qu'elle
      illustre.
- [ ] Sous-titres mot à mot intégrés à l'image (le son est coupé par défaut
      sur Instagram), dans la zone sûre (y 300 à 1450 en 9:16).

## 3. Image

- [ ] Vraie profondeur : 3D (three.js, `vendor/three`) ou 2,5D construite,
      lumière qui raconte quelque chose (lampe, aube, contre-jour).
- [ ] Mouvements de caméra motivés, chaque plan se pose avant de couper.
- [ ] Effets au service du sens : profondeur de champ et mise au point,
      flou de bougé réel (moyenne de sous-images sur ce qui va vite), halo
      lumineux, grain, vignette, transitions cachées dans un mouvement.
- [ ] Couleurs de la marque exactes à la fin (logo, turquoise `#22D3C3`,
      marine), sans dérive due au rendu.
- [ ] Rendu déterministe : chaque image est une fonction pure du temps.
      Test obligatoire : mêmes images au pixel près quel que soit l'ordre.

## 4. Son

- [ ] Bande-son synthétisée (aucune licence) : musique + un bruitage pour
      chaque événement visible, calé sur la grille exportée par le film.
- [ ] La musique se creuse sous la voix (environ −9 dB) ; la voix gagne
      toujours. Intelligibilité mesurée **dans le mix** : taux d'erreur de
      transcription au plus égal à celui de la voix seule (hors noms propres).
- [ ] Master à −14 LUFS (±0,5), crête vraie ≤ −1 dBTP, mesurés sur le
      fichier livré.

## 5. Vérification sur le fichier livré

- [ ] Images extraites par numéro aux instants clés et regardées ; défauts
      écrits avant que quelqu'un d'autre les voie, corrigés en v2, v3…
- [ ] Versions numérotées, jamais écrasées ; journal des versions avec
      les mesures dans le document de direction.
- [ ] Livrables : master 9:16, couverture, version web légère avec affiche
      pour le site, résumé texte pour les lecteurs d'écran.
