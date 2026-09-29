# Film n° 3 : « Le cap »

Film Instagram (9:16, 31 s) en motion design, registre « publicité tech haut
de gamme ». Il ne reparle pas des huit services (« Le mur ») : il présente
**la façon de travailler** de Pilotia, sa méthode en 4 étapes, ses engagements
et le sens de son nom.

## Brief

- **Public :** dirigeants de petites entreprises et futurs indépendants, sur
  Instagram, en lecture automatique **son coupé** : le texte porte tout.
- **La seule affirmation :** avec Pilotia, vous gardez le cap, et c'est vous
  qui restez aux commandes.
- **Angle :** la phrase du site, « Piloter, c'est garder le cap même quand la
  route se complique ». Elle est la dernière chose qu'on lit, au-dessus du logo
  dont on vient de découvrir le creux.
- **Contrainte :** pas de voix (aucune synthèse vocale disponible) ; musique et
  bruitages synthétisés, donc aucune licence.

## Chiffres autorisés à l'écran

`4` (étapes de la méthode), `15 minutes` (premier appel), `3 à 5` (priorités
chiffrées), et les numéros de chapitre `01` à `04`. Aucun autre nombre, aucun
montant, aucun nom de client ni de partenaire. Tous les textes viennent de
`methode.html`, `a-propos.html` et `contact.html`.

## Trois pistes, deux tuées

### A. « Le cadran » : TUÉE
Un instrument de précision (cadran, lunette crantée) filmé en macro, chaque
cran de la lunette étant une étape de la méthode.
**Pourquoi tuée :** c'est la direction « instrument de précision » du guide,
reprise telle quelle ; le métal en CSS risque de faire gadget, et la métaphore
laisse croire qu'on vend un objet.

### B. « Verre liquide » : TUÉE
L'icône Pilotia en verre translucide, des panneaux de verre flottant en
profondeur, un balayage de lumière sur chacun.
**Pourquoi tuée :** c'est le kit « pub Apple » appliqué en bloc (verre, dégradé,
reflets) ; un concurrent pourrait le reprendre sans rien changer, et des
panneaux qui défilent refont les cartes du « Mur ».

### C. « Le cap » : RETENUE
Un seul plan-séquence en **vue pilote** : caméra basse derrière une ligne
lumineuse qui file sur un sol sombre ponctué de points. Le texte vit dans le
ciel, les graphismes au sol. Quatre stations (Écouter, Diagnostiquer, Décider,
Piloter), puis la caméra s'élève et révèle que la route parcourue **était la
ligne du logo**, et que le sol survolé **était la tuile de l'icône**.

## Le geste signature

**Le cap ne bouge jamais à l'écran : quand la route tourne, c'est le monde
qui tourne autour de la ligne.** Deux virages pendant le vol (le sommet puis le
creux du logo), vécus comme une rotation du sol ; à la fin, la vue d'en haut
montre le vrai tracé, creux compris, au moment où le texte dit « même quand la
route se complique ».

## Cadrans, comparés aux deux films précédents

| Cadran | Film n° 1 | Film n° 2 « Le mur » | Film n° 3 « Le cap » |
|---|---|---|---|
| Énergie | contemplative | vive | vive, puis un arrêt net |
| Fond | vide bleu-nuit, grain | papier crème | sol marine et champ de points, ciel noir |
| Profondeur | 2D | cartes retournées | vraie perspective 3D, caméra basse |
| Caméra | fixe | tournée de carte en carte | un seul plan-séquence, puis grue jusqu'à la vue d'en haut |
| Texture | grain, vignette | net, contours épais | net, lumière (halo sur la ligne) |
| Couleur | monochrome + cyan | huit aplats | noir et blanc ; le spectre de la marque en lumière seulement |
| Typo | Calistoga + Inter léger | Inter 900 façon autocollant | Inter variable : chaque titre passe du fin au gras en arrivant |
| Son | nappe grave, silences | marimba 80 bpm | électro 120 bpm pompée, puis coupure sèche |
| Structure | on ouvre sur la réponse | beaucoup de problèmes, un par un | une démonstration continue, et la révélation que le trajet était le logo |
| Fin | la marque se pose, calme | accord plein | la musique s'arrête net sur la pointe de la flèche ; logo dans le silence |

## Budget de l'accent (le spectre)

Le spectre de la marque (turquoise du logo, bleu, indigo, violet, rose, corail,
ambre) n'apparaît que : sur la ligne et son halo, sur **un** mot par titre, et
sur le liseré lumineux autour de l'icône finale. Tout le reste est blanc, gris
ou marine.

## Grille (120 bpm, un temps = 0,5 s, une mesure = 2 s)

| Temps | Contenu |
|---|---|
| 0 à 2 | « Qui pilote votre entreprise ? », la ligne est déjà en route |
| 2 à 4 | « Vous. » (la musique démarre), « Avec une méthode en 4 étapes. » |
| 4 à 8 | 01 Écouter : ondes au sol ; appel de 15 minutes, gratuit, sans engagement |
| 7,5 | virage 1 : le sol tourne, le cap reste |
| 8 à 12 | 02 Diagnostiquer : balayage radar ; marges, organisation, visibilité |
| 11,5 | virage 2 |
| 12 à 16 | 03 Décider : un éventail de routes se referme sur une seule ; 3 à 5 priorités chiffrées |
| 16 à 20 | 04 Piloter : portes franchies sur le temps ; suivi mensuel, si vous le voulez |
| 20 à 24 | Quatre engagements, un par seconde |
| 24 à 26,5 | La grue : la caméra s'élève, le sol devient la tuile de l'icône, la route devient la ligne du logo |
| 26,5 à 28 | « Garder le cap, même quand la route se complique. » au-dessus du logo immobile, creux compris ; le spectre se vide, la ligne devient blanche |
| 28 | La flèche se pose, la musique s'arrête net |
| 28 à 31 | L'icône exacte se pose, un reflet, PILOTIA, « Premier appel gratuit · lien en bio » ; le titre reste en haut |

Chaque bruitage est calculé depuis la grille exportée par le film
(`window.FILM.sons`) : image et son ne peuvent pas diverger.

## Journal des versions (mesuré sur les fichiers livrés)

- **v1 :** −13,9 LUFS, crête vraie −2,5 dB ; départ de la musique +10 dB sur
  « Vous. », impact du chapitre 1 +4 dB, silence final à −74 dB. Défauts
  vus sur les images extraites : portes qui montaient dans le ciel et barraient
  « Chiffré, pas vague. », marche sombre sous l'horizon, points qui
  stroboscopaient dans les virages, coup final pas plus fort que la musique.
- **v2 :** interrompue (la source avait déjà évolué).
- **v3 :** portes sous la hauteur de caméra et effacées après passage ; sol
  infini en vue pilote qui s'efface pendant la grue ; flou de bougé réel
  (12 instants dans les virages, 4 au sprint et à la grue) ; inclinaison dans
  les virages ; ouverture à la verticale du point turquoise ; coup final
  +3,9 dB au-dessus de la montée. Déterminisme vérifié : même image à l'octet
  près quel que soit l'ordre des positions demandées.
- **v4 :** « Vous. » arrive épais et claque sur le départ ; la flèche paraît
  une image plus tôt, sur le coup ; repères du radar agrandis.
- **v5 :** vérification image par image (par numéro d'image, pas par temps) :
  l'image 61 montrait « Vous. » par-dessus le fantôme de la question. La
  question finit maintenant de sortir à 1,94 s et « Vous. » est déjà là sur
  l'image 60, celle du départ de la musique ; la flèche est présente sur
  l'image 840, celle du coup final.
