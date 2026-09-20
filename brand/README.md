# Kit visuel Pilotia

Avatar et illustrations dessinés en vectoriel, aux couleurs exactes du site.
Aucune licence à respecter, aucune attribution : ce sont des fichiers faits sur
mesure pour Pilotia.

## Avatar — version 4

> Historique des écarts : v1 sans référence, v2 avec des lunettes que le
> modèle ne porte pas, v3 d'après photo mais en costume-cravate et barbue.
> La version actuelle est glabre et en t-shirt col rond, à la demande du
> client.

## Avatar — les fichiers

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
| `--cheveux` | cheveux **et** sourcils |
| `--marine` / `--marine-fonce` | t-shirt et bord-côte du col |
| `--fond` | disque de fond |
| `--bronze` | anneau et pochette |

Il n'y a ni groupe `barbe` ni groupe `lunettes` : le personnage est glabre et
sans lunettes.

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

---

# Illustrations

| Fichier | Sujet | Utilisé sur |
|---|---|---|
| `illu-tableau-de-bord.svg` | Indicateurs, courbe de tendance, anneau de répartition | `outils.html` |
| `illu-visibilite-locale.svg` | Résultats de recherche, établissement mis en avant, note en étoiles | `marketing-digital.html` |
| `illu-*-1280.png` | Exports pour Canva et réseaux sociaux (fond blanc) | — |

## Elles changent de couleur toutes seules

Chaque teinte s'écrit `var(«jeton», repli)`, par exemple
`fill="var(--card, #FFFFFF)"`. Ce qui donne deux comportements :

- **Insérées directement dans une page** (c'est le cas sur le site, en SVG
  *inline* et non via `<img>`), elles lisent les jetons de `style.css` et
  suivent donc le thème clair/sombre sans qu'on ait rien à faire.
- **Ouvertes seules** (Canva, réseaux sociaux), aucun jeton n'existe : c'est la
  valeur de repli qui s'applique, en version claire.

Un seul fichier couvre donc les deux usages. À noter : si on les insérait avec
`<img src="...">`, l'héritage ne fonctionnerait plus — une image externe est un
document isolé, coupé des variables de la page.

## Parti pris de contenu

Aucun texte, aucun chiffre : les libellés sont figurés par des barres grises.
Une illustration qui affiche de fausses données ou du faux texte vieillit mal,
se contredit avec le contenu réel de la page, et oblige à la refaire à chaque
changement. Les barres restent justes indéfiniment et n'ont pas besoin d'être
traduites.

## Quatre pièges rencontrés

1. **Pas de double tiret dans un commentaire XML** — voir la section avatar,
   même cause, mêmes conséquences.
2. **`<use href>` seul ne suffit pas.** Les éditeurs restés au SVG 1.1 ne
   reconnaissent que `xlink:href` ; sans lui, les étoiles disparaissent à
   l'import. Les deux attributs sont donc présents.
3. **`clip-path` en CSS est souvent ignoré à l'import.** La demi-étoile utilise
   un vrai élément `<clipPath>`, compris partout.
4. **Un SVG sans `width`/`height` retombe à 300 px.** La règle `.illu` dans
   `style.css` fixe `width:100%` en plus de `max-width`, sinon l'illustration
   reste minuscule quelle que soit la place disponible.
