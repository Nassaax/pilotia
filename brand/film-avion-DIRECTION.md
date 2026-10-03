# Film n° 6 : « Prenez de la hauteur »

Premier film Pilotia **avec une voix off française**. Format 9:16 pour
Instagram et le site, environ 45 secondes, sous-titres intégrés à l'image
(le son est coupé par défaut sur Instagram : le film doit se comprendre muet).

## Brief

- **Public :** gérants de petites entreprises et de commerces, le soir, sur
  leur téléphone.
- **La seule affirmation :** Pilotia vous sort de la paperasse et vous aide à
  piloter, à partir de vos vrais chiffres.
- **L'angle :** le moment que tout gérant connaît, tard le soir, seul avec ses
  factures. Puis la même facture devient ce qui vous fait décoller.
- **Chiffres autorisés à l'écran ou dans la voix (tous repris du site) :**
  « 3 à 5 priorités » (méthode), « premier appel gratuit ». Aucun montant :
  les sommes de la facture sont des barres grises, comme dans les
  illustrations du site.

## Trois pistes, deux tuées

### A. « Le tableau des départs » : TUÉE
Un tableau d'aéroport à palettes qui affiche, au fil de la voix, « Facture
Peppol : à l'heure », « Trésorerie : retardée »…
**Pourquoi tuée :** le tableau d'aéroport est un poncif publicitaire, et des
palettes qui se retournent une à une, c'est le mécanisme du « Mur ».

### B. « Le bruit devient signal » : TUÉE
Des milliers de caractères (TVA, marge, facture…) tourbillonnent puis
s'alignent en une seule ligne nette.
**Pourquoi tuée :** des particules qui forment une figure, c'est la signature
de « 9 questions ». Ce serait le même film avec un autre mot.

### C. « La facture qui s'envole » : RETENUE
Un seul objet réel, filmé en vraie 3D (lumière physique, ombres portées,
profondeur de champ) : une facture sous une lampe de bureau, la nuit. La voix
nomme ce qui pèse : l'impayé, Peppol, la marge qu'on ne voit plus. Sur le mot
« Pilotia », la facture **se plie elle-même en avion de papier**, décolle,
sort de la nuit vers l'aube, et sa traînée **dessine la ligne du logo** :
le point turquoise au départ, l'avion devient la flèche.

## Le geste signature

**La facture devient l'avion, l'avion devient la flèche du logo.** Le nom
« Pilotia » contient « pilote » : le pliage tombe exactement sur ce mot.

## Ce qui le distingue des cinq films précédents

| | Films précédents | « Prenez de la hauteur » |
|---|---|---|
| Voix | aucune | voix off française, chaque animation calée sur le mot prononcé |
| Matière | aplats, lumière abstraite, cartes | papier réel en 3D, lampe, ombres, profondeur de champ |
| Couleur | marine/spectre, crème/couleurs franches, nuit/couleurs vives | nuit chaude (lampe ambre) qui devient aube (bleu pâle, rose) |
| Structure | démonstration ou inventaire | récit : une soirée, un basculement, un envol |
| Son | musique seule | voix, piano nocturne, froissements de papier calés sur chaque pli, souffle du décollage |

## Méthode (exigences appliquées)

1. La voix est générée **avant** l'image ; la durée de chaque plan vient de
   la longueur réelle de la voix.
2. Chaque mot est daté par un modèle de reconnaissance vocale française ;
   chaque apparition est calée sur le début du mot qu'elle illustre.
3. Rendu déterministe : chaque image est une fonction pure du temps.
4. Vérification sur le fichier livré : images par numéro, niveau de chaque
   bruitage mesuré, intelligibilité de la voix mesurée par transcription
   automatique du master, −14 LUFS, crête vraie ≤ −1 dBTP.
5. Versions numérotées, jamais écrasées ; journal ci-dessous.

## Journal des versions (mesuré sur les fichiers livrés)

- **v1 :** rendu complet (1 200 images, 2 065 rendus 3D avec sous-images de
  flou de bougé). −13,8 LUFS, crête −2,5 dB ; voix comprise à 94 % dans le
  mix (transcription automatique). Défauts relevés sur le fichier livré :
  pliage sombre, petit et en bas du cadre ; image noire juste avant la coupe
  vers l'aube ; soleil et faisceaux qui brûlent « cap » ; plis de papier
  inaudibles sous le coup de « Pilotia » ; souffle du décollage trop faible.
- **v2 :** caméra haute pendant le pliage et lumière d'appoint par-dessus ;
  l'avion frôle l'objectif exactement à l'image de la coupe ; faisceaux
  éteints avant « cap », soleil adouci. Recalcul des seules images de 15,4 à
  32 s (le reste repris du brut v1, à l'image près). Décollage +7,6 dB,
  « seul » +2,3 dB.
- **v3 (livrée) :** son seul. Les plis ont leur propre piste et un vrai corps
  de papier : +6,7 à +15 dB au-dessus du silence qui les précède (les deux
  premiers restent volontairement sous la voix). Cloches de « mois après
  mois » déplacées entre les mots (elles masquaient « mois »). −13,8 LUFS,
  crête −2,1 dB, voix comprise à 94 % (erreurs restantes : orthographe de
  « Peppol » et « Pilotia », « On » entendu « En »).
  Déterminisme vérifié : mêmes images au pixel près quel que soit l'ordre.

**À faire ensuite si on y revient :** une version 16:9 pour le site et
YouTube (la scène 3D se recadre, il suffit de nouvelles caméras), et une
voix masculine en alternative.
