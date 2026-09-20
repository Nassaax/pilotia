# Kit avatar Pilotia

Avatar dessiné en vectoriel, aux couleurs exactes du site. Aucune licence à
respecter, aucune attribution : c'est un fichier fait sur mesure pour Pilotia.

## Les fichiers

| Fichier | À quoi il sert |
|---|---|
| `avatar-pilotia.svg` | Version ronde, fond bleu clair cerclé de bronze. **La source à modifier.** |
| `avatar-pilotia-transparent.svg` | Même personnage, sans fond. Pour poser sur une couleur, une photo, un bandeau. |
| `avatar-pilotia-512.png` | Photo de profil réseaux sociaux (LinkedIn, Facebook, Instagram). |
| `avatar-pilotia-1024.png` | Version haute définition, fond compris. |
| `avatar-pilotia-transparent-1024.png` | Version haute définition, fond transparent. |

Les PNG sont exportés en densité x2 : le fichier `512` fait en réalité
1024 × 1024 pixels, donc il reste net sur écran Retina.

## Dans Canva

Importe les `.svg` plutôt que les `.png` : Canva les accepte et ils restent nets
à n'importe quelle taille, même agrandis plein écran dans un carrousel.

- Carrousel, bannière, story → `avatar-pilotia-transparent.svg`
- Photo de profil, vignette, pastille « auteur » → `avatar-pilotia.svg`

## Modifier l'avatar

Tout se règle dans le bloc `<style>` en tête de `avatar-pilotia.svg`, sans
toucher au dessin :

| Variable | Effet |
|---|---|
| `--peau` | teint |
| `--peau-ombre` | ombre sous la mâchoire — garder un cran plus sombre que `--peau` |
| `--cheveux` | cheveux **et** barbe |
| `--marine` / `--marine-fonce` | veste et revers |
| `--fond` | disque de fond |
| `--bronze` | anneau et pochette |

Pour **enlever la barbe** : supprimer le groupe `<g id="barbe">` en entier.

Après toute modification, régénérer la version transparente et les PNG — la
version transparente est dérivée de la source, elle ne se met pas à jour seule.

## Deux pièges rencontrés en la fabriquant

1. **Pas de double tiret dans un commentaire XML.** Écrire `--peau` dans un
   commentaire rend le fichier invalide : les navigateurs l'affichent quand même
   en inline dans une page HTML, mais l'ouvrir comme fichier `.svg` (donc
   l'importer dans Canva) échoue silencieusement. C'est pour ça que les
   variables sont citées entre guillemets dans les commentaires.
2. **Les angles des revers doivent rester en retrait de la ligne d'épaule**,
   sinon ils dépassent de la silhouette et forment un bourrelet visible dès
   qu'on agrandit.

## Où il est utilisé sur le site

- `a-propos.html`, section « Qui accompagne », à côté du nom du fondateur.

L'avatar y est déclaré avec `alt=""` : le nom et la fonction figurent juste à
côté, un texte alternatif ne ferait que les répéter au lecteur d'écran.
