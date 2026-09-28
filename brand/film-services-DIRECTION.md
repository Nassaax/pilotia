# Film de lancement n° 2 : « Le mur »

Film de présentation des services, dans la direction colorée de la série
Services (`services.css`). Il ne remplace pas la grammaire du premier film
(`film-lancement.mp4`, « Ce qui est déjà engagé ») : il doit s'en distinguer sur
le fond, pas seulement sur la palette.

## Brief

- **Produit :** Pilotia, accompagnement de gestion pour PME et indépendants belges.
- **Public :** dirigeants de petites structures, sur Instagram (9:16, son coupé par
  défaut) et sur la page d'accueil du site (16:9).
- **La seule affirmation :** les casse-têtes du quotidien d'un entrepreneur ont
  chacun une réponse, et un seul interlocuteur les porte toutes.
- **Contrainte :** muet côté voix (aucune synthèse vocale disponible), donc mené
  par les cartons et la musique. Le texte doit se lire son coupé.

## Chiffres autorisés à l'écran

`8` (le nombre de services présentés), `3 minutes` (diagnostic express),
`60 jours` (plafond légal du délai de paiement entre entreprises). Aucun autre
nombre. Aucun montant, aucun taux, aucun nom de partenaire.

## Trois pistes, deux tuées

### A. « Une journée, huit coups de main » : TUÉE
Journée chronologique, une horloge-autocollant dans un coin, un volet circulaire
coloré à chaque heure.
**Pourquoi tuée :** l'horloge est le cliché de la catégorie, déjà écarté pour le
premier film. Et une journée où tout arrive à heure fixe ment sur la réalité
d'un indépendant.

### B. « Le mur » : RETENUE
Le film **s'ouvre plein** : un mur de huit cartes grises, huit casse-têtes. La
caméra fait la tournée du mur, carte par carte, et **chaque carte se retourne sur
le temps fort de la mesure** pour montrer sa réponse, dans la couleur de son
service. Le mur passe du gris à l'arc-en-ciel. À la fin, la caméra recule sur le
mur entièrement coloré, et la marque s'y colle.

### C. « Le paquet de cartes » : TUÉE
Huit cartes distribuées puis regroupées en une seule.
**Pourquoi tuée :** « plusieurs deviennent un » est le dispositif par défaut, et
le regroupement final est le climax que tout le monde fait.

## Cadrans (B), comparés au premier film

| Cadran | Film n° 1 | Film n° 2 |
|---|---|---|
| Énergie | contemplative, deux silences | vive, une mesure par carte |
| Fond | vide bleu-nuit | papier crème |
| Profondeur | 2D stricte | retournements 3D des cartes |
| Caméra | fixe, un seul recul | tournée continue d'une carte à l'autre |
| Texture | grain et vignette | net, sans grain |
| Couleur | monochrome + cyan | une couleur par service, huit en tout |
| Son | nappe grave, silences | musique pincée à 80 bpm, bruitages sur chaque retournement |
| Structure | on ouvre sur une réponse et on la démonte | on ouvre plein de problèmes et on les retourne un à un |
| Fin | le plan reste, la marque se pose | fin forte : accord plein sur le mur coloré |

## Le geste signature

**La caméra arrive sur une carte grise, et la carte se retourne exactement sur le
deuxième temps de la mesure, comme si la musique la retournait.** Le mur, lui,
change de couleur une carte à la fois : c'est le seul indicateur de progression
du film.

## Grille de temps (80 bpm, une mesure = 3 s)

| Mesure | Temps | Contenu |
|---|---|---|
| 0 | 0,0 à 3,0 | Mur gris en plan large. Carton « 8 casse-têtes d'entrepreneur. » puis « Pilotia les retourne. » |
| 1 à 8 | 3,0 à 27,0 | Une carte par mesure : trajet 0,45 s, retournement posé au 2e temps, étiquette au 3e temps |
| 9 | 27,0 à 28,5 | Recul sur le mur coloré, puis un demi-temps de silence musical |
| 9-10 | 28,5 à 31,5 | La marque se colle au 3e temps : accord final, tenue immobile |

Chaque bruitage est calculé depuis cette même grille (voir `score-services.py`) :
la synchronisation est garantie par construction, pas mesurée après coup.
