# Film n° 4 : « Votre métier »

Film Instagram (9:16, 31 s) en motion design, dans la charte colorée de la
série Services (`services.css`) : crème, couleurs franches, contours marine
épais, ombres portées nettes, pastilles inclinées, autocollants.

## Brief

- **Sujet (nouveau) :** les cinq métiers qui ont leur page d'accompagnement
  sur le site : coiffure, boulangerie, restauration, esthétique, immobilier.
  Aucun film ne les a encore traités (« Le mur » : les services ; « Le cap » :
  la méthode ; Reels : un service chacun).
- **Public :** gérants de ces commerces, sur Instagram, son coupé par défaut.
- **La seule affirmation :** Pilotia parle votre métier, pas un conseil
  générique de commerce.
- **Textes :** les accroches et les défis sont repris mot pour mot des pages
  `coaching-*.html`. Aucun chiffre à l'écran.

## Trois pistes, deux tuées

### A. « La rue des vitrines » : TUÉE
Un travelling le long d'une rue de cinq boutiques qui s'allument une à une.
**Pourquoi tuée :** c'est la tournée de caméra du « Mur » (beaucoup
d'éléments, un par un), avec des vitrines à la place des cartes.

### B. « L'écran partagé » : TUÉE
Cinq bandes verticales, une par métier, qui jouent en même temps puis se
réorganisent.
**Pourquoi tuée :** trop dense pour un téléphone : cinq animations côte à
côte donnent des éléments de 200 px de large, illisibles.

### C. « L'objet qui change de métier » : RETENUE
Caméra fixe. Un seul autocollant au centre, contour marine et ombre portée,
**se transforme d'un métier à l'autre** sur le premier temps de la mesure :
cercle gris « générique », sèche-cheveux, croissant, cloche de restaurant,
flacon de vernis, maison, puis bulle de dialogue. À chaque transformation, la
couleur du métier inonde l'écran depuis l'intérieur de l'objet.

## Le geste signature

**Une forme qui change de métier.** Le contour de l'objet se déforme d'un
emblème à l'autre (le même tracé, jamais un fondu), avec écrasement et rebond,
et le monde prend la couleur du métier. Il apparaît au début (le cercle
générique barré d'un « non merci »), se répète pour chaque métier, puis
s'emballe (un métier par temps) avant de devenir la bulle « Et votre métier ? ».

## Ce qui le distingue des films précédents

| | « Le mur » | « Le cap » | « Votre métier » |
|---|---|---|---|
| Caméra | tournée de carte en carte | plan-séquence en vol | fixe, rien ne bouge que l'objet |
| Procédé | beaucoup de cartes, retournées une à une | une démonstration continue | un seul objet qui se transforme |
| Couleur | huit aplats sur crème | noir, spectre en lumière | le fond entier change de couleur à chaque métier |
| Son | marimba 80 bpm | électro 120 bpm, coupure sèche | pop-funk 128 bpm menée par les bruitages (rebonds, claques d'autocollants) |
| Fin | accord plein sur le mur | logo dans le silence | une question ouverte : « Et votre métier ? », sur un accord suspendu |

## Couleurs (reprises de la série Services, variante « plein » pour le texte blanc)

| Métier | Fond | Emblème |
|---|---|---|
| Coiffure | rose `#BE185D` | sèche-cheveux |
| Boulangerie | ambre `#B45309` | croissant |
| Restauration | corail `#C2410C` | cloche de service |
| Esthétique | violet `#6D28D9` | flacon de vernis |
| Immobilier | bleu `#1D4ED8` | maison |

Accroche et fin sur le crème. Le jaune `#FACC15` reste la couleur des
pastilles et du mot en exergue.

## Grille (128 bpm : un temps = 0,469 s, une mesure = 1,875 s)

| Temps | Contenu |
|---|---|
| 0 à 5,6 | Cercle gris : « Des conseils génériques ? », tampon « non merci », puis « Pilotia parle votre métier. » |
| 5,6 à 24,4 | Cinq métiers, deux mesures chacun : transformation et inondation sur le premier temps, pastille du métier, accroche du site en trois lignes, autocollant du défi |
| 24,4 à 27,2 | Emballement : un métier par temps, puis la bulle |
| 27,2 à 31 | « Et votre métier ? », premier appel gratuit, lien en bio ; accord suspendu |

## Journal des versions (mesuré sur les fichiers livrés)

- **v1 :** −14,0 LUFS, crête vraie −1,9 dB. Tampon « non » +23 dB au-dessus de
  ce qui précède, départ du groove +19 dB, rebond de transformation +3 dB,
  creux de la pause bulle à −27 dB. Défaut : l'accord final n'était que 0,3 dB
  au-dessus du groove.
- **v2 :** tout s'arrête un temps avant l'accord final, une aspiration remplit
  ce temps ; l'accord tombe 9,7 dB au-dessus. Synchro vérifiée par numéro
  d'image : le tampon claque sur l'image 57 (1,90 s), la première
  transformation démarre sur l'image 169.
- **v3 :** rebond final visible (la bulle s'étire, les cinq mini-emblèmes
  sautent sur l'accord). Déterminisme vérifié : même image à l'octet près quel
  que soit l'ordre des positions demandées.
