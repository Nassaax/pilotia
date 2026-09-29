# Charte graphique — contenus sociaux Pilotia

Référence unique pour tout ce qui est publié sur les réseaux : carrousels,
Reels, vignettes, visuels de publicité. Dérivée du film de lancement, pour que
tout ce qui sort du compte se reconnaisse au premier coup d'œil.

Les valeurs vivent dans `brand/social.css` — ce fichier-ci explique **pourquoi**
elles sont ce qu'elles sont. Ne pas recopier une couleur à la main : importer
le CSS.

---

## 1. Fond

Un bleu-nuit, jamais du noir pur. Le noir absolu écrase les dégradés sur les
écrans OLED et fait ressortir la compression d'Instagram ; le bleu-nuit garde
de la matière.

| Jeton | Valeur | Emploi |
|---|---|---|
| `--void` | `#070B16` | fond de base |
| `--void-lift` | `#0E1628` | centre du dégradé radial |
| `--void-deep` | `#04060E` | bords du dégradé |

Le fond est toujours un **dégradé radial** centré haut, jamais un aplat :
`radial-gradient(120% 70% at 50% 32%, var(--void-lift), var(--void) 58%, var(--void-deep))`.

## 2. Encre

| Jeton | Valeur | Emploi |
|---|---|---|
| `--ink` | `#F1F5F9` | titres, chiffres principaux |
| `--ink-soft` | `#8CA0BC` | légendes, libellés, unités |
| `--ink-faint` | `#63748E` | mentions légales, numérotation |

## 3. Couleur — un seul accent, une alerte rationnée

| Jeton | Valeur | Budget d'emploi |
|---|---|---|
| `--accent` | `#4FD1E8` | **un** élément mis en avant par visuel : un mot du titre, une courbe, un chiffre-clé, le bouton d'appel |
| `--alert` | `#FB7185` | **uniquement** un solde négatif, un point bas, un seuil dépassé. Jamais décoratif, jamais pour « faire joli » |
| `--ok` | `#4ADE80` | un montant positif que l'on oppose explicitement à un négatif. Rare |

Une troisième teinte est presque toujours une erreur. Si un visuel semble en
avoir besoin, c'est qu'il dit deux choses à la fois : le couper en deux.

## 4. Typographie

| Usage | Police | Graisse |
|---|---|---|
| Logotype « Pilotia » | Calistoga | 400 |
| Tout le reste | Inter | 200 (très grands chiffres), 300 (titres), 400 (corps), 500 (accentuation) |

- Les **chiffres sont toujours tabulaires** (`font-variant-numeric: tabular-nums`) :
  sans cela, une animation de compteur fait danser la ligne.
- Interlettrage négatif sur les grands corps (`-0.04em` au-delà de 90 px),
  neutre en dessous.
- Le séparateur de milliers est une **espace ordinaire**, pas l'espace fine
  insécable que produit `toLocaleString` : Instagram recompresse mal l'U+202F.

## 5. Texture

Grain à 5,5 % en `mix-blend-mode: screen`, tuile de 220 px, plus une vignette
radiale. Toujours les deux ensemble : le grain seul fait sale, la vignette
seule fait vide. En vidéo, le décalage du grain est **dérivé de la tête de
lecture**, jamais aléatoire — sinon le rendu image par image n'est pas
reproductible.

## 6. Formats et zones sûres

| Usage | Dimensions | Zone sûre |
|---|---|---|
| Carrousel (fil) | 1080 × 1350 | marge de 90 px sur les quatre bords |
| Reel / Story | 1080 × 1920 | **entre y = 300 et y = 1450** — l'interface d'Instagram mange le reste |
| Site / paysage | 1920 × 1080 | marge de 120 px |

La zone sûre des Reels n'est pas une coquetterie : une première version du film
de lancement avait ses libellés de mois et son dernier carton sous les boutons
de l'application.

## 7. Règles de contenu — non négociables

1. **Aucun chiffre qui ne soit calculé.** Tout montant publié sort de
   l'arithmétique d'un outil du site (`tresorerie.js`, les calculateurs) ou
   d'un texte légal cité. Rien n'est arrondi « pour que ça sonne mieux ».
2. **Un montant illustratif porte la mention « scénario d'exemple »**, et la
   précision qu'il ne représente les résultats d'aucun client.
3. **Aucun témoignage, aucun avis, aucun visage tant qu'il n'y a pas de client
   réel qui l'a écrit.** Publier de faux avis figure sur la liste noire du
   CDE (art. VI.100) : interdit en soi, sanctionnable pénalement.
4. **Aucune métrique de performance** (« +30 % de marge », « 40 clients »)
   tant qu'elle n'est pas mesurée sur des cas réels.
5. Un visuel renvoie vers **un** outil ou **une** action, jamais trois.
6. **Aucun tiret long (« — ») pour relier deux idées**, ni sur les visuels ni
   sur le site : il donne au texte un air rédigé par une IA. On écrit une
   virgule, deux-points, des parenthèses, ou une nouvelle phrase après un point.

## 8. Sujets déjà traités — ne pas refaire

Un compte se décrédibilise vite s'il ressert deux fois le même calcul sous une
autre couverture. Avant d'écrire un nouveau visuel, vérifier cette liste et
l'y ajouter ensuite.

| Sujet | Support | Fichier / lien |
|---|---|---|
| Le rythme trimestriel des échéances | Carrousel | `carrousel-trimestre.html` |
| Le coût réel d'un salarié (× 1,45) | Carrousel | `carrousel-cout-salarie.html` |
| La franchise TVA à 25 000 € | Film court | `film-court.html?f=tva` |
| La marge unitaire et le seuil de rentabilité | Film court | `film-court.html?f=marge` |
| La régularisation des cotisations d'indépendant | Carrousel Canva | `DAHV2lIVqTs` |
| Rentabilité ≠ trésorerie (le délai d'encaissement) | Carrousel Canva | `DAHV2hPWtRA` |
| Service : facture électronique Peppol | Carrousel série Services | `carrousel-service-peppol.html` |
| Service : prévenir les mauvais payeurs | Carrousel série Services | `carrousel-service-mauvais-payeurs.html` |
| Service : affacturage | Carrousel série Services | `carrousel-service-affacturage.html` |
| Service : diagnostic express et complet | Carrousel série Services | `carrousel-service-diagnostic.html` |
| Service : présence digitale | Carrousel série Services | `carrousel-service-presence-digitale.html` |
| Service : devenir indépendant | Carrousel série Services | `carrousel-service-independant.html` |
| Service : accompagnement mensuel | Carrousel série Services | `carrousel-service-accompagnement.html` |
| Service : outils gratuits | Carrousel série Services | `carrousel-service-outils.html` |
| Film « Le mur » : les huit services | Film 9:16 et 16:9 (31,5 s) | `film-services.html`, direction : `film-services-DIRECTION.md` |
| Le vrai calcul du taux horaire (324,58 € par jour) | Carrousel série Services (pédagogique) | `carrousel-edu-taux-horaire.html` |
| Indépendant complémentaire : les trois seuils | Carrousel série Services (pédagogique) | `carrousel-edu-complementaire.html` |
| Facture impayée : professionnel ou particulier | Carrousel série Services (pédagogique) | `carrousel-edu-impaye.html` |
| Les 3 fuites de marge d'un restaurant | Carrousel série Services (pédagogique) | `carrousel-edu-marge-restaurant.html` |
| Chiffrer un chantier | Carrousel série Services (pédagogique) | `carrousel-edu-chantier.html` |

## 9. Cohérence de série

Contrairement à un film de lancement — où la ressemblance entre deux films est
un défaut — un compte social gagne à être reconnaissable. Le gabarit est donc
**volontairement constant** : même fond, même accent, même typographie, même
structure de couverture. Ce qui change d'un post à l'autre, c'est le chiffre et
l'histoire, pas l'habillage.

## 10. Production — les fichiers

Tout est dans `brand/`. Rien ne dépend d'un service extérieur ni d'un compte.

| Fichier | Rôle |
|---|---|
| `social.css` | les jetons et les composants. **Toujours l'importer**, ne jamais recopier une valeur |
| `carrousel-*.html` | un carrousel = un fichier, une `.planche` par image. Capturé en PNG à 1080 × 1350 |
| `film-court.html` | le moteur de films courts. Un film = **une entrée dans l'objet `FILMS`**, le moteur ne change pas |
| `score-court.py` | la bande-son d'un film court, synthétisée à partir de sa durée, de ses frappes et de son instant de résolution |

### Le moteur de films

Aucune bibliothèque d'animation : chaque beat est une **fonction pure du
temps**. Un saut à l'instant T produit toujours la même image, quel que soit
le chemin parcouru — c'est la condition d'un rendu image par image fiable.
Les types de beat disponibles : `carton`, `chips`, `chiffre`, `barres`,
`marque`, tous avec un `chapeau` optionnel.

Pour ajouter un film : copier une entrée de `FILMS`, changer les beats, les
instants de frappe et la mention légale. Compter **environ huit minutes de
calcul** pour quinze secondes à 30 images par seconde.

### Chaîne audio

Son entièrement synthétisé — donc aucune licence à déclarer et aucun risque
de revendication automatique sur les réseaux. Master en deux passes
(`loudnorm` mesure puis corrige), limiteur de crête, puis **mesure du fichier
livré**, pas du mixage source : cible **−14 LUFS, crête vraie ≤ −1 dBTP**.

### Polices

Auto-hébergées depuis `fonts/`, jamais chargées depuis un CDN — un appel à
Google Fonts enverrait l'adresse IP du visiteur aux États-Unis sans son
consentement.

## 11. La voie Canva

Deux carrousels vivent dans le compte Canva plutôt que dans ce dépôt, pour
pouvoir être retouchés sans passer par du code :

| Carrousel | Design |
|---|---|
| La régularisation des cotisations | `DAHV2lIVqTs` |
| Rentabilité n'est pas trésorerie | `DAHV2hPWtRA` |

Ce qu'il faut savoir avant d'en refaire un :

- **La génération automatique de Canva ne sert à rien ici.** Sur deux essais,
  elle a rendu une couverture seule d'un côté, et de l'autre les six pages
  empilées sur une seule avec du faux français et des montants inventés
  (« 5,0000 € »). Les pages sont donc construites à la main, élément par
  élément, à des coordonnées explicites.
- **Le gabarit** est celui de `social.css` transposé : marge de 90 px, fond
  `#070B16` posé en rectangle plein page, sur-titre à y = 90, filet cyan de
  120 × 3 px, pied de page à y = 1232.
- **Ancrer chaque texte en haut** (`update_text_anchoring: start`) *avant* de
  le positionner : sinon Canva recentre le bloc dès que la taille change, et
  l'élément se déplace tout seul.
- **Un nombre ne doit jamais être coupé par un retour à la ligne.** C'est
  arrivé deux fois (« = 7 » / « 790,00 € », puis « 12 000 » / « € HTVA »).
  Soit on réduit le corps pour que la ligne tienne, soit on force la coupure
  avec un `\n` explicite.
- **Une seule police pour tout le carrousel.** Un texte ajouté par l'API prend
  la police par défaut ; un texte hérité d'une génération garde la sienne. Si
  la couverture ne ressemble pas aux autres pages, la supprimer et la recréer.

## 12. La série « Services » : l'exception colorée

Les carrousels pédagogiques restent sur le fond bleu-nuit des sections 1 à 3.
Les carrousels qui **présentent une offre** suivent une autre grammaire, pour
accrocher dans un fil et se lire comme une affiche. Tout est dans
`brand/services.css`.

| Règle | Pourquoi |
|---|---|
| Fond crème `#FFF8EC`, planche finale en couleur pleine | Tranche avec le fil sombre des carrousels pédagogiques : on reconnaît une offre au premier coup d'œil |
| Une couleur par service (Peppol bleu, mauvais payeurs corail, affacturage vert, diagnostic violet, présence digitale rose, indépendants ambre, accompagnement indigo, outils sarcelle) et une couleur « pop » pour surligner | Chaque service garde son identité d'un post à l'autre |
| Cartes à contour marine épais et ombre franche, pastilles inclinées | Le côté ludique vient de la forme, pas de la quantité de couleurs |
| Texte blanc seulement sur `--plein` (4,5:1 minimum) | Le vert et le corail vifs plafonnaient à 3,3:1 |
| Aucun montant ni taux d'offre | Les conditions des partenaires ne sont pas publiques. Seuls chiffres admis : ceux de la loi (40 €, 60 jours) |
| Aucun nom de partenaire financier | Choix du fondateur |

Les règles de contenu de la section 7 s'appliquent sans exception, et la
règle n° 6 aussi : aucun tiret long.

Rendu : chaque `.planche` est capturée en PNG 1080 × 1350, avec un contrôle
qui signale tout texte sortant de la marge de 90 px.
