# Format app sur téléphone : document de conception

Conception validée par le fondateur le 12 octobre 2026, partie par partie,
sur maquettes (dossier `format-app/`). Ce document fait foi pour le plan de
travail et pour la future app : toute divergence se corrige ici d'abord.
Précisé le même jour avec les décisions prises en rédigeant le plan de
l'étape 1 (`format-app-PLAN-etape1.md`, « Décisions prises en rédigeant ce
plan ») : § 3.3, 4.2, 4.3, 5.1 et 5.2.

## 1. Objectif et périmètre

Donner au site, sur téléphone et tablette, le comportement d'une application,
pour que les clients retrouvent exactement les mêmes repères dans la future
app Pilotia. Cette app servira à la fois aux outils et rendez-vous (pour tout
le monde) et, plus tard, à un espace client privé avec connexion.

**Dans le périmètre :** une navigation d'app (barre d'onglets, retour, menu
« Plus »), deux nouveaux écrans (Services, Mon espace), l'onglet Outils
réorganisé, le format app de toutes les pages existantes, la mise à jour des
pages Cookies et Confidentialité, une fiche de référence pour la future app.

**Hors périmètre (décisions explicites) :**
- l'installation sur l'écran d'accueil (manifeste, service worker, hors
  ligne) : « pas maintenant » ;
- l'espace client avec connexion ;
- toute réécriture des textes validés ;
- tout changement de calcul dans les outils, des API ou des données envoyées ;
- tout renommage de page (les adresses actuelles restent valables).

## 2. Décisions prises avec le fondateur

| Question | Décision |
|---|---|
| Que fera la future app ? | Les deux : outils et rendez-vous pour tous, espace client privé plus tard. |
| Onglets de la barre du bas | Accueil, Services, Rendez-vous (bouton central), Outils, Mon espace. |
| « Mon espace » avant la connexion | Un espace sur ce téléphone : les résultats que les outils y ont déjà enregistrés. |
| Installation (PWA) | Pas maintenant. |
| Ampleur | Refonte mobile complète : la navigation d'app et le format app de chaque page. |
| Textes trop longs sur téléphone | Encadré « L'essentiel » en haut, puis le détail mot pour mot en sections repliables. Une seule version du texte. |
| Mise en œuvre | Branche séparée et version de test Vercel ; étape 1 (navigation, nouveaux écrans, 6 pages pilotes), puis les pages famille par famille. |

## 3. Navigation (maquette 1)

### 3.1 Barre d'onglets

- **Quand :** largeur d'écran de 1 080 px ou moins, le seuil où le menu du
  haut se replie déjà aujourd'hui. Au-delà, le menu actuel reste seul.
- **Ordre et libellés fixes :** Accueil, Services, Rendez-vous, Outils,
  Mon espace. Chaque onglet a une icône au trait (SVG en ligne, 24 px, trait
  de 2) et son libellé toujours écrit dessous (11,5 px, graisse 600). Aucune
  icône seule.
- **Onglet actif :** couleur d'accent et pastille d'accent clair derrière
  l'icône. `aria-current="page"` sur la page principale de l'onglet,
  `aria-current="true"` sur ses pages de détail.
- **Bouton central « Rendez-vous » :** rond de 60 px, fond d'accent, contour
  et ombre décalée (la signature des boutons principaux), surélevé au-dessus
  de la barre. Il mène à `contact.html`. Sur cette page, il est cerclé et son
  libellé passe à la couleur d'accent.
- **Confort :** zones à toucher d'au moins 48 × 48 px ; barre de 64 px plus
  la zone de sécurité du bas de l'iPhone (`env(safe-area-inset-bottom)`, ce
  qui demande `viewport-fit=cover` dans la balise viewport de chaque page).
- **Clavier :** sur téléphone, la barre se masque tant qu'un champ de saisie
  a le focus, et revient quand il le perd.
- **Rien de caché :** le bas de chaque page reçoit une marge égale à la
  hauteur de la barre ; le dernier contenu reste toujours visible.
- **Fond opaque** (jeton `--card`) et filet `--line` en haut ; le mode sombre
  suit les jetons existants.
- **Balisage :** `<nav aria-label="Navigation principale">` contenant cinq
  liens ordinaires. La barre fonctionne sans JavaScript.

### 3.2 Correspondance des pages et des onglets

| Onglet | Page principale | Pages de détail (lien retour) |
|---|---|---|
| Accueil | `index.html` | aucune |
| Services | `services.html` (nouvelle) | `entreprises`, `independants`, `facturation-electronique`, `affacturage`, `marketing-digital`, `offres`, les 5 pages `coaching-*` (retour « ‹ Services ») |
| Rendez-vous | `contact.html` | aucune |
| Outils | `outils.html`, avec ses sous-onglets `conseils.html` et `ressources.html` | `diagnostic`, `rapport-diagnostic`, les 6 `calculateur-*`, `plan-tresorerie`, `generateur-calendrier-contenu` (retour « ‹ Outils ») ; les 7 articles `conseils-*` (retour « ‹ Conseils ») |
| Mon espace | `mon-espace.html` (nouvelle) | aucune |
| Aucun (menu « Plus ») | | `a-propos`, `methode`, `statistiques`, `parrainage`, `mentions-legales`, `confidentialite`, `cookies`, `cgv`, `accessibilite`, `404` |

### 3.3 Barre du haut (1 080 px ou moins)

À 1 080 px ou moins, la liste de liens actuelle et son panneau déroulant ne
s'affichent plus : la barre d'onglets et le panneau « Plus » les remplacent.
Le bouton ☰ actuel (`#navToggle`) est conservé et ouvre désormais ce panneau.

- **Page principale d'un onglet, ou page du menu « Plus » :** logo (lien vers
  l'accueil) à gauche, bouton ☰ à droite.
- **Page de détail :** lien « ‹ Services », « ‹ Outils » ou « ‹ Conseils » à
  gauche, à la place du logo. Il pointe vers une adresse fixe, jamais vers
  l'historique du navigateur : il fonctionne même si l'on arrive de Google.
- **Le bouton ☰** ouvre le panneau « Plus », qui monte du bas : voile, poignée,
  bouton ✕, fermeture par Échap ou par le voile, focus gardé dans le panneau
  puis rendu au bouton ☰. Contenu :
  - **Pilotia :** À propos, Notre méthode, Statistiques, Parrainage,
    Instagram (nouvel onglet) ;
  - **Informations :** Mentions légales, Confidentialité, Cookies,
    Conditions générales, Accessibilité.
- **Sur ordinateur (plus de 1 080 px) :** le menu actuel ne change pas, sauf
  deux entrées ajoutées au menu « Découvrir » : « Tous les services » (en
  tête) et « Mon espace » (en fin), actives sur leur propre page.

### 3.4 Transitions entre pages

Fondu court (200 ms au plus) entre deux pages, par les transitions de vue
entre documents (`@view-transition { navigation: auto; }`). Les deux barres
restent fixes pendant le fondu. Désactivé si la personne a demandé moins
d'animations ; sans effet sur les navigateurs qui ne le connaissent pas.

## 4. Nouveaux écrans (maquette 2)

### 4.1 Services (`services.html`)

- Titre « Services » et une phrase d'introduction.
- **Votre situation :** deux grandes tuiles, « Entreprise en activité »
  (vers `entreprises.html`, couleur `svc-pilotage`) et « Futur indépendant »
  (vers `independants.html`, couleur `svc-independant`).
- **Nos services,** une ligne par service, à sa couleur :
  - Facture électronique Peppol : « Obligatoire depuis janvier 2026 » ;
  - Affacturage : « Être payé sans attendre l'échéance » ;
  - Présence digitale : « Fiche Google, réseaux, avis clients » ;
  - Offres et tarifs : « Diagnostic, coaching, suivi mensuel ».
- **Votre métier :** cinq pastilles (Restaurant, Boulangerie, Coiffure,
  Esthétique, Agent immobilier) vers les pages `coaching-*`.
- **Pas sûr ?** une carte finale vers le diagnostic express.
- Sous-titres : uniquement des phrases ou faits déjà présents sur le site.
- Sur ordinateur, la même page en grille. Page référencée comme les autres
  (titre, description, canonique, Open Graph, `sitemap.xml`, `llms.txt`).

### 4.2 Mon espace (`mon-espace.html`)

Données lues dans le stockage local du navigateur, sans aucun envoi :
- `pilotia-diagnostic` (existant : score sur 16, libellé, scores par thème
  sur 4, réponses). Le diagnostic y ajoutera la date du test.
- `pilotia-tresorerie-resume` (nouveau) : écrit par le plan de trésorerie à
  chaque calcul, dès que la personne a modifié son plan (le plan d'exemple
  chargé à la première visite n'est pas le sien et ne doit pas s'afficher
  comme tel). Il contient le montant du point bas, son mois et la date de
  mise à jour. Le plan complet reste dans `pilotia-tresorerie` (existant).

Affichage (« cet appareil » plutôt que « ce téléphone » : la page s'affiche
aussi sur ordinateur) :
- En haut, toujours : « Enregistré sur cet appareil uniquement. Rien n'est
  envoyé. »
- **Carte Diagnostic :** score sur 16, libellé, une barre par thème, date.
  Boutons « Refaire » (vers `diagnostic.html`) et « Rapport détaillé » (vers
  `rapport-diagnostic.html`).
- **Carte Plan de trésorerie :** « Point bas : montant, fin du mois », date,
  lien « Ouvrir mon plan ».
- **Votre prochain pas :** deux lignes. D'abord l'outil lié au thème le plus
  faible :
  - Finances : calculateur de marge ;
  - Personnel et organisation : coût d'un salarié ;
  - Présence digitale : générateur de calendrier de contenu ;
  - Trésorerie et résilience : plan de trésorerie, ou le délai
    d'encaissement si un plan existe déjà.

  En cas d'égalité, l'ordre de priorité est : Trésorerie, Finances,
  Personnel, Présence. Ensuite, toujours, l'appel gratuit.
- **Effacer les données de cet appareil :** demande une confirmation, puis
  supprime `pilotia-diagnostic`, `pilotia-tresorerie` et
  `pilotia-tresorerie-resume`.
- **Sans donnée, ou sans JavaScript :** le HTML livré affiche trois points de
  départ (diagnostic, plan de trésorerie, appel gratuit). Le script ne
  remplace ce contenu que s'il trouve des résultats.
- Le jour où la connexion arrive, elle s'ajoute sur cette page.

### 4.3 Onglet Outils et ses sous-onglets

- Un contrôle segmenté « Outils | Conseils | Guides » (trois liens vers
  `outils.html`, `conseils.html` et `ressources.html`, `aria-current` sur
  l'actif) en haut de ces trois pages.
- **`outils.html` sur téléphone :** le diagnostic express mis en avant, puis
  chaque outil sur une ligne (icône à la couleur des outils, titre, sa
  description limitée à deux lignes). Le texte complet de chaque carte reste
  dans la page et s'affiche entièrement sur ordinateur.
- **`conseils.html` et `ressources.html` :** même principe de lignes à toucher
  pour les articles et les documents. Chaque document de `ressources.html`
  garde son formulaire d'envoi par email : il devient une ligne compacte, pas
  un lien sur toute la ligne.

## 5. Format app des pages existantes (maquettes 3A et 3B)

### 5.1 Les briques communes

- **Encadré « L'essentiel » :**
  - trois points au maximum, placés juste avant les boutons du haut de page
    s'il y en a : ce sont eux qui portent l'action principale, sans bouton en
    double ;
  - ses points ne répètent pas la phrase d'introduction affichée juste
    au-dessus ;
  - chaque affirmation et chaque nombre existent déjà dans la page (contrôle
    automatique des nombres) ;
  - pas de tiret long ;
  - affiché aussi sur ordinateur.
- **Sections repliables :**
  - chaque grande section (`h2`) de la page devient repliable sous 760 px
    (téléphones), et toutes sont fermées par défaut ;
  - au-delà de 760 px, tout reste ouvert, sans bouton : le script retire ses
    enveloppes et le HTML reste exactement celui d'origine ;
  - le sur-titre d'une section s'affiche à l'ouverture, en tête de son
    contenu ;
  - le titre reste un vrai `h2`, qui contient un `<button aria-expanded>` ; le
    corps est masqué avec `hidden="until-found"`, pour que la recherche dans
    la page puisse l'ouvrir ;
  - un lien « Tout ouvrir / Tout fermer » ;
  - un lien vers une ancre ouvre la section visée ;
  - l'impression ouvre tout ;
  - sans JavaScript, tout reste ouvert ;
  - les questions fréquentes, déjà en `<details>`, gardent leur
    fonctionnement.
- **Listes à toucher :** lignes d'au moins 56 px (icône, titre, sous-titre,
  chevron), la ligne entière est le lien.
- **Tuiles, pastilles défilantes, cartes à faire glisser** (accroche au
  défilement, sans bibliothèque) pour l'accueil et les pages principales.
- **Formulaires :**
  - champs d'au moins 48 px de haut et police d'au moins 16 px (l'iPhone ne
    zoome pas) ;
  - `inputmode="decimal"` sur les montants ;
  - `autocomplete` adapté sur le formulaire de contact.
- **Résultats de calcul :** affichés dans un bloc mis en valeur, annoncés aux
  lecteurs d'écran (`aria-live="polite"`) ; l'écran descend doucement jusqu'à
  eux (sans animation si la personne a demandé moins d'animations).

### 5.2 Règles par famille de pages

| Famille | Traitement |
|---|---|
| Accueil | Message d'accueil intact, quatre accès rapides (Diagnostic express, Plan de trésorerie, Facture Peppol, Devenir indépendant) à la place des deux boutons du haut, comme sur la maquette, puis les sections actuelles en cartes à faire glisser (piliers, parcours, avis clients ; le film reste en place). |
| Services et métiers | « L'essentiel », puis sections repliables. |
| Outils (diagnostic, calculateurs, plan de trésorerie, générateur) | Calculs inchangés ; formulaires au pouce ; résultat mis en valeur ; étapes suivantes en cartes. |
| Conseils (articles) | « L'essentiel », puis chaque partie de l'article repliable sous son titre exact. |
| Rendez-vous (`contact.html`) | Réservation du créneau en premier ; le formulaire de message dans un repli. |
| Pilotia (à propos, méthode, statistiques, parrainage) | « L'essentiel » si la page compte au moins deux sections `h2`, puis replis. |
| Pages légales | Articles repliables avec « Tout ouvrir ». Pas d'encadré « L'essentiel » : pas de résumé juridique. |
| 404 | Liens directs vers les cinq onglets. |

### 5.3 Ordinateur

Le même HTML sert partout. Sur ordinateur, les encadrés « L'essentiel »
apparaissent, les sections restent ouvertes et les grilles actuelles sont
conservées. Des captures avant/après prouvent que rien d'autre ne bouge.

## 6. Architecture technique

- **Aucun outil de construction ajouté :** le site reste en HTML, CSS et
  JavaScript simples.
- **`style.css` :** les styles de la barre d'onglets, de la barre du haut, du
  panneau « Plus », des briques et des familles. Ils sont regroupés sous un
  titre de section, avec les jetons existants.
- **`app.js` (nouveau, chargé avec `defer` sur toutes les pages) :**
  - le panneau « Plus » ;
  - le masquage de la barre pendant la saisie ;
  - les sections repliables et « Tout ouvrir » ;
  - le défilement vers les résultats ;
  - l'ouverture sur ancre et à l'impression.

  Le code du menu actuel (`animations.js`) reste en place pour l'ordinateur.
- **`mon-espace.js` (nouveau, seulement sur `mon-espace.html`) :** lecture et
  effacement des données locales.
- **Balisage de navigation :** la barre d'onglets et la barre du haut sont
  écrites dans le HTML de chaque page par un script de génération rejoué à
  chaque modification (`scripts/navigation-app.py`). L'onglet actif et le
  lien retour sont donc corrects sans JavaScript.
- **Politique de sécurité (CSP) :** compatible telle quelle (scripts et
  styles du même domaine, aucune ressource tierce).
- **Aucun cookie, aucun traceur.** Les pages Cookies et Confidentialité
  listent les trois clés locales :
  - `pilotia-diagnostic` (avec sa date) ;
  - `pilotia-tresorerie`, déjà utilisée mais absente de la page Cookies,
    oubli corrigé au passage ;
  - `pilotia-tresorerie-resume`.

  Ces pages précisent aussi leur finalité (afficher vos propres résultats),
  leur durée (jusqu'à effacement) et le bouton « Effacer ».

## 7. Déroulé

1. **Branche `format-app`.** Vercel en publie une version de test à une
   adresse fixe, sans connexion et non référencée par les moteurs de
   recherche. Le site public ne change pas jusqu'à la fusion.
2. **Étape 1, validée par le fondateur sur son téléphone :**
   - la navigation complète ;
   - `services.html` et `mon-espace.html` ;
   - les sous-onglets Outils ;
   - six pages pilotes : `index`, `facturation-electronique`,
     `conseils-facture-impayee`, `calculateur-marge`, `contact`,
     `mentions-legales`.
3. **Étape 2,** famille par famille, chacune vérifiée puis montrée :
   1. Outils ;
   2. Services et métiers ;
   3. Conseils ;
   4. Pilotia et 404 ;
   5. Légal.
4. **Validation finale,** puis fusion dans `main` : la mise en ligne.

## 8. Vérifications automatiques (à chaque famille)

- **Texte d'origine :** il est intégralement présent sur chaque page. Le texte
  visible avant et après est comparé, hors encadrés « L'essentiel » et
  navigation.
- **Encadrés « L'essentiel » :** chacun de leurs nombres figure ailleurs dans
  la page. Aucun tiret long dans le texte visible.
- **Tailles d'écran :** aucun défilement horizontal à 360, 390, 768 et
  1 280 px de large ; la barre d'onglets ne recouvre jamais le dernier
  élément de la page.
- **Onglets :** le bon onglet est actif et le bon lien retour apparaît sur
  chacune des 45 pages.
- **Lisibilité :** zones à toucher d'au moins 48 px ; contrastes en clair et
  en sombre (audit existant).
- **Fonctionnement :**
  - liens internes valides ;
  - replis et panneau utilisables au clavier, avec `aria-expanded`
    cohérent ;
  - aucune erreur JavaScript dans la console.
- **Ordinateur :** captures avant/après sur les pages modifiées.

## 9. Livrables annexes

- `brand/charte-app.md`, la fiche de référence pour la future app :
  - onglets et ordre ;
  - icônes (sources SVG) ;
  - jetons de couleur ;
  - correspondance des pages et des onglets ;
  - comportements (retour, « Plus », clavier, replis) ;
  - Mon espace aujourd'hui, et ce qu'il deviendra.
- Pages Cookies et Confidentialité à jour.
- `README.md` : une section « Format app ».
- `sitemap.xml` et `llms.txt` : les deux nouvelles pages.

## 10. Risques et parades

| Risque | Parade |
|---|---|
| Un texte validé modifié ou perdu | Comparaison automatique du texte avant et après. |
| La barre cache un bouton ou un champ | Marge du bas, masquage pendant la saisie, test du dernier élément. |
| Barres de Safari sur iPhone et hauteur d'écran | Barre fixée en bas avec la zone de sécurité, sans hauteur en `vh`. |
| Un chiffre inventé dans un encadré | Contrôle automatique des nombres, relecture humaine au pilote. |
| Contenu replié invisible pour Google | Le texte reste dans le HTML (`hidden="until-found"`). |
| Poids et lenteur | Aucune bibliothèque, icônes SVG en ligne, deux petits scripts. |
