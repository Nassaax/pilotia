# Espace client : document de conception

Conception validée par le fondateur le 13 octobre 2026, partie par partie,
sur maquettes (dossier `espace-client/`). Ce document fait foi pour le plan
de travail : toute divergence se corrige ici d'abord. Il prolonge le format
app (`format-app-CONCEPTION.md`), dont l'onglet « Mon espace » avait été
prévu pour accueillir la connexion « le jour venu, au même endroit ».

## 1. Objectif et périmètre

Permettre à un client de créer, s'il le souhaite, un espace personnel où il
retrouve ses résultats sur tous ses appareils et encode une fois les
informations de son entreprise, que les outils reprennent ensuite. Les outils
gratuits restent utilisables sans compte, pour toujours : le compte ajoute
des fonctions, il ne retire rien.

**Dans le périmètre :**
- l'inscription et la connexion par un code reçu par email ;
- Mon espace une fois connecté ;
- la fiche entreprise et le pré-remplissage de quatre calculateurs ;
- l'enregistrement dans l'espace :
  - du diagnostic ;
  - du plan de trésorerie ;
  - du dernier calcul de chacun des six calculateurs ;
- le téléchargement des données, la déconnexion (d'un appareil ou de tous) et la suppression de l'espace ;
- un interrupteur qui garde l'espace fermé sur le site public jusqu'à l'ouverture ;
- les textes légaux d'ouverture, préparés ici et publiés le jour de l'ouverture.

**Hors périmètre (décisions explicites) :**
- l'historique des diagnostics et des versions du plan (« Historique et
  progression » non retenu) : seul le dernier est gardé ;
- le suivi avec Pilotia (rendez-vous, plan d'action, documents, messages) et
  le partage d'un espace avec Pilotia : deuxième version ;
- les coordonnées officielles (numéro d'entreprise, adresse, téléphone) ;
- le mot de passe, la connexion Google, le lien de connexion par email ;
- le changement d'adresse email : pour l'instant, télécharger ses données,
  supprimer l'espace et en recréer un ;
- tout écran d'administration : Pilotia ne voit que le nombre de comptes ;
- l'installation de l'app sur l'écran d'accueil (toujours « pas maintenant ») ;
- tout changement de calcul dans les outils.

## 2. Décisions prises avec le fondateur

| Question | Décision |
|---|---|
| Contenu de la première version | Résultats synchronisés (diagnostic, plan de trésorerie, calculs) et fiche entreprise. |
| Connexion | Un code à 6 chiffres reçu par email. Pas de mot de passe, pas de lien à cliquer. |
| Place du compte | Outils libres pour toujours, compte en plus. |
| Qui voit les données | Le client seul. Pilotia ne voit que le nombre de comptes. |
| Contenu de la fiche | Identité, statut et TVA, chiffres clés facultatifs. Pas de coordonnées officielles. |
| Ouverture | Construire et tester sur la version de test ; l'inscription reste masquée sur le site public par un interrupteur jusqu'à ce que les mentions légales soient complètes. |
| Approche technique | Notre propre service : fonctions Vercel, base Postgres Neon à Francfort, codes envoyés par Brevo, session dans un cookie protégé. |
| Partie 1 (connexion) | Validée telle que la maquette E1. |
| Partie 2 (espace connecté) | Validée, avec la conversion des frais fixes × 12 pour le taux horaire. |
| Partie 3 (données et sécurité) | Validée. |
| Partie 4 (vie privée et ouverture) | Validée ; un espace sans connexion pendant 2 ans est supprimé, après un avertissement un mois avant. |
| Partie 5 (vérifications et livraison) | Validée. |

**Précisions apportées en rédigeant ce document :**
1. **Fermeture à distance.** Une connexion fermée à distance (« Se
   déconnecter de tous mes appareils », ou espace supprimé depuis un autre
   appareil) efface les données Pilotia de l'appareil concerné dès sa
   prochaine visite. C'est plus sûr en cas de téléphone perdu. Seule
   l'expiration après 90 jours sans visite garde les modifications en
   attente sur l'appareil (§ 3.7). La légende de la maquette E3 est mise à
   jour en ce sens.
2. **Résumé du calculateur de marge.** Dans Mon espace, il reprend la marge
   et le seuil : « 12,00 € de marge · 267 ventes / mois ». La maquette
   n'affichait que le seuil.
3. **Code pendant l'étape Bienvenue.** Un code juste pour une nouvelle
   adresse reste valable 15 minutes de plus, le temps de cette étape.
4. **Pages hors moteurs de recherche.** Les trois nouvelles pages portent
   `noindex` jusqu'à l'ouverture ; seule la page des conditions entre
   ensuite dans le plan du site.

## 3. Parcours et écrans

### 3.1 Où l'on entre (maquette E1, écran 1)

Sur `mon-espace.html`, une carte « Votre espace Pilotia » s'ajoute en haut,
au-dessus de ce que la personne a déjà fait sur l'appareil. Elle porte la
signature contour et ombre de la charte, trois avantages, le bouton « Créer
mon espace » et le lien « Déjà un espace ? Se connecter ». Sous la carte :
« Facultatif : tous les outils restent gratuits, avec ou sans espace. »

- La carte n'apparaît que si l'espace est ouvert (§ 7). Interrupteur fermé :
  Mon espace reste exactement celui d'aujourd'hui.
- Les deux liens mènent à `connexion.html` ; le lien « Se connecter » ajoute
  `?mode=connexion`, qui ne change que le titre de l'écran.
- Aucune autre page ne propose l'espace avant l'ouverture. À l'ouverture, le
  plan de trésorerie le mentionne dans ses textes (§ 8.3).

### 3.2 Connexion par code (maquette E1, écrans 2 à 5)

Une seule page, `connexion.html`, en trois étapes. Chaque étape remplace la
précédente, le focus passe au titre de la nouvelle étape et les erreurs sont
annoncées (`role="alert"`). Barre d'onglets : « Mon espace » actif, lien
retour « Mon espace ».

1. **L'adresse email.**
   - Titre « Créer mon espace », ou « Me connecter » en mode connexion.
   - Texte : « Entrez votre adresse email : vous recevrez un code à 6
     chiffres pour entrer. Pas de mot de passe à retenir. »
   - Champ `type="email"`, `autocomplete="email"`.
   - Bouton « Recevoir mon code ».
   - Sous le bouton : « Votre adresse sert uniquement à vous connecter. Elle
     n'est ajoutée à aucune liste d'envoi. »
   - Un champ leurre invisible écarte les robots, comme sur le formulaire de
     contact.
   - La réponse est la même, que l'adresse ait déjà un espace ou non.
2. **Le code.**
   - Titre « Entrez votre code ».
   - « Envoyé à {adresse}. Modifier » : le lien ramène à l'étape 1.
   - Un seul champ de 6 chiffres, présenté en six cases :
     `inputmode="numeric"`, `autocomplete="one-time-code"`, collage accepté.
   - Bouton « Valider ».
   - « Valable 10 minutes, une seule fois. Rien reçu ? Regardez dans vos
     courriers indésirables. »
   - « Renvoyer le code », actif après une minute.
   - Erreurs :
     - « Ce code ne correspond pas. Il vous reste N essais. » ;
     - « Ce code a expiré. » avec le bouton « Recevoir un nouveau code » ;
     - après 5 essais faux : « Trop d'essais. Demandez un nouveau code. ».
3. **Bienvenue** (création seulement).
   - Titre « Votre espace est presque prêt ».
   - Champ « Votre prénom (facultatif) ».
   - Encadré « Déjà sur cet appareil » : les résultats qui rejoindront
     l'espace (diagnostic avec sa date, plan de trésorerie s'il a été
     modifié). Rien sur l'appareil : l'encadré n'apparaît pas.
   - Case obligatoire « J'accepte les conditions d'utilisation de l'espace
     client », avec un lien vers `conditions-espace.html`.
   - Bouton « Créer mon espace ».
   - Sous le bouton : « Visible par vous seul. Vous pourrez tout télécharger
     ou tout supprimer depuis Mon espace. »
   - Une personne qui a déjà un espace saute cette étape et arrive
     directement sur Mon espace.

**L'email du code** (expéditeur « Pilotia », envoyé par Brevo) :

> Objet : Votre code Pilotia : 482 913
>
> Bonjour,
>
> Voici votre code pour entrer dans votre espace Pilotia :
>
> **482 913**
>
> Il est valable 10 minutes et ne sert qu'une fois.
>
> Vous n'avez rien demandé ? Ignorez cet email : sans ce code, personne ne
> peut entrer dans votre espace.

Ni publicité ni lien à cliquer. Le code figure dans l'objet pour se lire
dans la notification. L'email existe aussi en version texte.

**Règles :**
- code à 6 chiffres tiré au hasard, valable 10 minutes, utilisable une seule
  fois, 5 essais au maximum ;
- une demande de code remplace la précédente ;
- un code juste pour une adresse sans espace reste valable 15 minutes de
  plus, le temps de l'étape Bienvenue ;
- connexion gardée 90 jours sur l'appareil, prolongée à chaque visite (au
  plus une fois par jour) ;
- sans JavaScript, la page affiche : « Activez JavaScript pour utiliser votre
  espace client. Les outils gratuits fonctionnent sans. »

### 3.3 Mon espace, connecté (maquette E2, écrans 1 et 2)

Ordre de la page :

1. **Titre** « Mon espace », puis « Bonjour {prénom} » (sans prénom :
   rien) et la ligne « Enregistré dans votre espace. Visible par vous
   seul. », avec l'icône bouclier.
2. **Fiche,** en une ligne : nom de l'entreprise, puis « secteur · statut »,
   avec un chevron. Le geste mène à `ma-fiche.html`. Fiche vide : une carte
   « Complétez votre fiche entreprise : les calculateurs partiront de vos
   chiffres » et un bouton.
3. **« Mes résultats » :** les cartes du diagnostic et du plan de trésorerie
   d'aujourd'hui, inchangées (le score par thème reste affiché).
4. **« Mes derniers calculs » :** une ligne par calculateur déjà utilisé, du
   plus récent au plus ancien, avec le titre de l'outil, son résultat et la
   date (« 12 oct. », espace insécable). Le geste rouvre l'outil sur ces
   chiffres. Aucun calcul : la section n'apparaît pas.
5. **« Votre prochain pas » :** comme aujourd'hui.
6. **« Pour votre entreprise »,** seulement si la fiche le permet : la page
   du métier et l'article qui va avec le statut (tableau ci-dessous).
   Chaque ligne reprend le titre de la page, sans « | Pilotia ».
7. **« Mon compte » :**
   - « Télécharger mes données » ;
   - « Se déconnecter » ;
   - « Se déconnecter de tous mes appareils » ;
   - « Supprimer mon espace », en rouge ;
   - puis « Connecté avec {adresse} ».

Le bouton actuel « Effacer les données de cet appareil » n'apparaît pas une
fois connecté : « Se déconnecter » joue ce rôle.

| Réponse dans la fiche | Ligne « Pour votre entreprise » |
|---|---|
| Restaurant, café | `coaching-restaurant.html` |
| Boulangerie, pâtisserie | `coaching-boulangerie.html` |
| Coiffure | `coaching-coiffeur.html` |
| Esthétique, institut de beauté | `coaching-esthetique.html` |
| Agent immobilier | `coaching-agent-immobilier.html` |
| Bâtiment, travaux | `conseils-chiffrer-chantier.html` |
| Services, conseil, freelance | `conseils-taux-horaire-independant.html` |
| Commerce, Autre | (aucune) |
| Statut « complémentaire » | `conseils-independant-complementaire.html` |
| Statut « en projet » | `conseils-lancer-independant.html` |

### 3.4 Ma fiche entreprise (maquette E2, écrans 3 et 4)

Page `ma-fiche.html`, onglet « Mon espace », lien retour « Mon espace ».
- Chapeau : « Remplie une fois, elle pré-remplit vos calculateurs. Chaque
  champ est facultatif. »
- Bouton « Enregistrer ma fiche », qui enregistre directement dans l'espace.
- Retour : « Fiche enregistrée. » et retour sur Mon espace.
- Sous chaque réponse utile, en couleur d'accent, l'outil qu'elle pré-remplit.

| Champ | Type | Valeurs acceptées | Pré-remplit |
|---|---|---|---|
| Prénom | texte | 60 caractères au plus | (salutation) |
| Nom de l'entreprise | texte | 120 caractères au plus | (fiche, Mon espace) |
| Métier ou secteur | liste | `restaurant`, `boulangerie`, `coiffure`, `esthetique`, `immobilier`, `batiment`, `commerce`, `services`, `autre` | « Pour votre entreprise » |
| Votre statut | choix | `principal`, `complementaire`, `societe`, `projet` (libellés : Indépendant à titre principal, Indépendant à titre complémentaire, Société (gérant, administrateur), En projet, pas encore lancé) | calculateur de cotisations |
| TVA | choix | `assujetti`, `franchise`, `inconnu` (Assujetti à la TVA, Franchise des petites entreprises, Je ne sais pas) | (fiche) |
| Chiffre d'affaires annuel, hors TVA (€) | nombre entier | 0 à 1 000 000 000 | franchise TVA |
| Frais fixes mensuels (€) | nombre entier | 0 à 100 000 000 | marge ; taux horaire (× 12) |
| Nombre de salariés | nombre entier | 0 à 10 000 | (fiche) |

Le prénom saisi à l'étape Bienvenue est le prénom de la fiche : une seule
source.

### 3.5 Calculateurs : pré-remplissage et calculs gardés (maquette E2, écran 5)

Script `compte-outils.js`, chargé sur les six calculateurs, après leurs
propres scripts. Pour une personne sans compte, il ne fait rien : les
calculateurs se comportent exactement comme aujourd'hui.

| Identifiant | Page | Champs gardés | Recalcul | Résultat affiché dans Mon espace | Pré-rempli par la fiche |
|---|---|---|---|---|---|
| `marge` | `calculateur-marge.html` | `prixVente`, `coutRevient`, `fraisFixes`, `margeUnitaire` | `calculerMarge()`, `calculerSeuil()` | `#margeEuro` · `#seuilVentes` | `fraisFixes` ← frais fixes mensuels |
| `taux-horaire` | `calculateur-taux-horaire.html` | `revenuNet`, `fraisPro`, `conges`, `maladie`, `occupation`, `heuresJour` | `calculerTarif()` | `#outJour` | `fraisPro` ← frais fixes mensuels × 12 |
| `cotisations` | `calculateur-cotisations-independant.html` | `revenu`, `statut` | `calculer()` | `#out-trimestre` | `statut` ← `principal` ou `complementaire` (`complement` dans la liste de l'outil) |
| `tva-franchise` | `calculateur-tva-franchise.html` | `ca` | `verifier()` | `#out-statut`, sans le symbole de tête | `ca` ← chiffre d'affaires annuel |
| `cout-salarie` | `calculateur-cout-salarie.html` | `brutMensuel`, `typeContrat`, `premierEngagement` | `calculerCout()` | `#out-cout` | (rien) |
| `delai-encaissement` | `calculateur-delai-encaissement.html` | `montant`, `avances`, `duree`, `delai`, `retard`, `parallele` | `calculerDelai()` | `#dsoJours` | (rien) |

L'identifiant est la clé du calcul dans l'élément `calculs` (§ 4.1).

**Ordre de priorité à l'ouverture d'un calculateur :**
1. le dernier calcul gardé de la personne pour cet outil ;
2. sinon la fiche, pour les champs du tableau ;
3. sinon les chiffres d'exemple de l'outil.

**Signalement :**
- **Dernier calcul repris :** bandeau « Vos derniers chiffres, enregistrés le
  {date}. »
- **Fiche reprise :** bandeau « Pré-rempli avec votre fiche entreprise.
  Modifier ma fiche ». Chaque champ concerné porte la pastille « De votre
  fiche », ou « De votre fiche (× 12) » pour le taux horaire.

**Garder un calcul :**
- Le calcul est gardé quand la personne a touché un champ ou un bouton de
  calcul et que le résultat a changé, une seconde après la dernière
  modification.
- Les chiffres d'exemple affichés à l'ouverture ne sont jamais gardés.
- Un seul calcul par outil, le dernier.
- Ce qui est gardé : la valeur de chaque champ, le texte du résultat, le
  titre de l'outil et la date.

Le coût d'un salarié, le délai d'encaissement et le plan de trésorerie ne
sont pas pré-remplis : aucun de leurs champs ne correspond exactement à un
chiffre de la fiche, et rien n'est deviné.

### 3.6 Mon compte (maquettes E2, écran 2, et E3, écran 3)

- **Télécharger mes données :** un fichier
  `pilotia-mon-espace-AAAA-MM-JJ.json` qui contient :
  - l'adresse, les dates de création et de dernière connexion ;
  - la fiche, le diagnostic, le plan et les calculs.
- **Se déconnecter :**
  - confirmation : « Se déconnecter de cet appareil ? Vos résultats restent
    dans votre espace et disparaissent de cet appareil. » ;
  - effets : la connexion est fermée et toutes les données Pilotia de
    l'appareil sont effacées ;
  - retour sur Mon espace avec : « Vous êtes déconnecté. Vos données restent
    dans votre espace. »
- **Se déconnecter de tous mes appareils :**
  - toutes les connexions de l'espace sont fermées ;
  - cet appareil est vidé tout de suite, comme pour « Se déconnecter » ;
  - chaque autre appareil efface ses données Pilotia à sa prochaine visite
    du site (§ 3.7), ce qui sert en cas de téléphone perdu.
- **Supprimer mon espace :**
  - feuille de confirmation (maquette E3) : « Supprimer votre espace ? Votre
    fiche, vos résultats et vos calculs seront effacés définitivement, de
    votre espace et de cet appareil. Pour les garder, téléchargez d'abord vos
    données. Vos outils restent utilisables sans compte. » ;
  - boutons « Supprimer définitivement » (rouge) et « Annuler » ;
  - effets : effacement immédiat, sans délai de grâce, puis Mon espace sans
    compte et le message « Votre espace a été supprimé. »

### 3.7 Cas particuliers (maquette E3)

- **Deux versions du plan :**
  - **Quand :** le plan a été modifié sur cet appareil alors que l'espace en
    contient une version plus récente, que l'appareil n'avait pas lue.
  - **Feuille :** « Votre plan a aussi changé sur un autre appareil. Il a été
    modifié dans votre espace le {date} à {heure}, pendant que vous le
    modifiiez ici. Lequel garder ? »
  - **Boutons :** « Garder celui de cet appareil » et « Reprendre celui de
    mon espace ».
  - **Note :** « La version écartée est remplacée. Pour garder les deux,
    exportez d'abord celle-ci (bouton en bas du plan). »
  - **Seul cas où l'on demande :** pour le diagnostic et les calculs, la
    version la plus récente l'emporte sans question.
- **Connexion expirée** (90 jours sans visite) :
  - les données de l'appareil sont gardées ;
  - Mon espace affiche l'encadré « Votre connexion a expiré. Vos dernières
    modifications sont gardées sur cet appareil. Reconnectez-vous pour les
    enregistrer dans votre espace. » avec le bouton « Me reconnecter » ;
  - à la reconnexion, les modifications en attente partent selon les règles
    du § 4.3.
- **Connexion fermée à distance** (« Se déconnecter de tous mes appareils »
  depuis un autre appareil, ou espace supprimé) :
  - à sa prochaine visite, l'appareil efface ses données Pilotia ;
  - Mon espace affiche : « Votre connexion a été fermée depuis un autre
    appareil. Les données de votre espace ne sont plus sur celui-ci. »
- **Autre compte sur le même appareil :** si l'on se connecte à un autre
  espace que celui dont l'appareil garde les données, ces données sont
  effacées de l'appareil avant la connexion, après confirmation (« Les
  données d'un autre espace sont sur cet appareil. Elles y seront effacées ;
  elles restent dans leur espace. »).
- **Interrupteur refermé** pendant qu'on est connecté :
  - l'espace disparaît de l'écran et les données restent sur l'appareil ;
  - l'enregistrement reprend à la réouverture.

### 3.8 Plan de trésorerie

- **Ligne d'état :** une ligne vide et cachée, ajoutée sous les boutons
  d'export de « 7. Garder votre plan ». Une fois connecté, elle affiche
  « Enregistré dans votre espace. », ou « En attente d'enregistrement : votre
  connexion a expiré. »
- **« Effacer mon plan et repartir de l'exemple » :** le plan de l'espace
  est effacé aussi. Un plan revenu à l'exemple (non modifié) compte comme
  « pas de plan ».
- **« Réimporter un plan » :** l'import vaut modification, il est donc
  enregistré dans l'espace.
- **Plan plus récent dans l'espace** que la copie de l'appareil, sans
  modification locale en attente : la copie est remplacée et la page se
  recharge une fois d'elle-même.

## 4. Données

### 4.1 Sur l'appareil

Les trois clés actuelles ne changent pas : `pilotia-diagnostic`,
`pilotia-tresorerie` et `pilotia-tresorerie-resume`. Une seule clé nouvelle,
présente seulement quand on est connecté (ou en attente de reconnexion) :

`pilotia-espace` :
```json
{
  "compte": "identifiant court de l'espace, non secret",
  "prenom": "Marie",
  "fiche": { "...": "copie de la fiche" },
  "calculs": { "marge": { "titre": "...", "champs": {}, "resultat": "...", "maj": "2026-10-12T14:05:00Z" } },
  "sync": { "diagnostic": { "version": 3, "empreinte": "..." }, "plan": {}, "calculs": {}, "fiche": {} },
  "expire": false
}
```

- **Pas d'adresse email sur l'appareil :** Mon espace la demande au serveur
  pour l'afficher.
- **La clé est effacée** à la déconnexion et à la suppression, avec les trois
  autres.

### 4.2 Dans l'espace (base Postgres Neon, Francfort)

| Table | Colonnes | Rôle |
|---|---|---|
| `comptes` | `id` (uuid), `email` (unique, en minuscules), `cree_le`, `vu_le`, `averti_le`, `conditions_version`, `conditions_le` | Un espace par adresse. |
| `sessions` | `jeton_empreinte` (SHA-256), `compte_id`, `cree_le`, `expire_le`, `renouvele_le`, `revoquee_le` | Connexions ; effacées avec le compte. Une connexion fermée à distance est marquée (`revoquee_le`) et gardée jusqu'à son expiration, pour que l'appareil concerné l'apprenne. |
| `codes` | `email_empreinte` (HMAC), `code_empreinte` (HMAC), `expire_le`, `essais`, `envoye_le`, `verifie_le` | Un code en cours par adresse. |
| `elements` | `compte_id`, `cle` (`fiche`, `diagnostic`, `plan`, `calculs`), `valeur` (jsonb), `version` (entier), `maj` | Le contenu de l'espace, une ligne par élément. |
| `limites` | `cle` (empreinte), `fenetre`, `nombre` | Compteurs anti-abus, effacés après 2 jours. |
| `schema_version` | `version` | Évolutions futures du schéma. |

- **Création automatique des tables :** le premier appel après un démarrage
  installe les tables manquantes (`create table if not exists`, sous verrou
  `pg_advisory_xact_lock`). Il n'y a aucune commande à lancer à la main.
- **Suppressions en cascade :** supprimer un compte efface ses sessions et
  ses éléments.

### 4.3 Synchronisation

- **Principe :** l'original est dans l'espace et l'appareil en garde une
  copie. Les outils ne lisent que la copie : ils s'ouvrent aussi vite
  qu'aujourd'hui.
- **Pages concernées :** `compte.js` est chargé sur :
  - `mon-espace.html`, `connexion.html` et `ma-fiche.html` ;
  - `diagnostic.html` et `rapport-diagnostic.html` ;
  - `plan-tresorerie.html` ;
  - les six calculateurs.

  Sans la clé `pilotia-espace`, il ne fait aucune requête, sauf sur
  `mon-espace.html` et `connexion.html`. Ces deux pages demandent l'état
  (espace ouvert ou fermé) pour afficher ou non la carte et le formulaire.
  `ma-fiche.html` sans connexion renvoie vers `connexion.html`.
- **Lecture :** à l'ouverture de chaque page et au retour sur l'onglet,
  l'appareil lit l'espace : une seule requête renvoie le contenu et la
  version de chaque élément.
  - Un élément plus récent dans l'espace, sans modification locale en
    attente, remplace la copie.
  - Exception : la fiche n'a jamais de modification locale, elle est
    enregistrée directement.
- **Écriture :**
  - **Détection :** toutes les 3 secondes tant que la page est visible, puis
    quand elle passe en arrière-plan ou se ferme, l'appareil compare chaque
    clé à l'empreinte de sa dernière version enregistrée.
  - **Envoi :** une différence part avec la version sur laquelle elle
    s'appuie. Le dernier envoi part en `keepalive`, pour survivre à la
    fermeture de la page.
  - **Contrôle :** le serveur refuse l'envoi si l'espace a changé entre-temps
    (réponse 409 avec la version actuelle).
- **Résolution d'un refus :**
  - **diagnostic :** le plus récent (champ `date`) l'emporte ;
  - **calculs :** fusion outil par outil, le plus récent (`maj`) l'emporte ;
  - **plan :** feuille « Deux versions du plan » (§ 3.7) ;
  - **fiche :** la page relit la version de l'espace et affiche « Votre fiche
    a été modifiée sur un autre appareil : voici la dernière version. »
- **Première connexion d'un appareil :**
  - ce qui n'existe que d'un côté rejoint l'autre ;
  - diagnostic présent des deux côtés : le plus récent ;
  - plan présent des deux côtés et modifié sur l'appareil : feuille « Deux
    versions du plan » si les contenus diffèrent ;
  - plan d'exemple sur l'appareil : il est remplacé sans question.
- **Sans réseau :** la modification reste en attente sur l'appareil et part à
  la visite suivante.
- **Connexion refusée (401) :** la réponse dit pourquoi.
  - **Pas de cookie, ou `expiree` :** le cookie est arrivé à son terme (le
    navigateur ne l'envoie plus), ou la connexion a dépassé sa durée.
    L'appareil garde ses données, marque `expire` et arrête d'envoyer.
  - **`fermee` :** un cookie est présenté, mais sa connexion a été fermée à
    distance ou n'existe plus (espace supprimé). L'appareil efface ses
    données Pilotia.

  Dans les deux cas, voir le § 3.7.
- **Tailles maximales :**

  | Élément | Taille maximale |
  |---|---|
  | fiche | 2 Ko |
  | diagnostic | 32 Ko |
  | calculs | 32 Ko |
  | plan | 256 Ko |

  Au-delà, l'envoi est refusé (413) et Mon espace l'indique.

## 5. Sécurité

- **Cookie de connexion :**
  - nom `__Host-pilotia-session`, valeur aléatoire de 32 octets ;
  - attributs `HttpOnly`, `Secure`, `SameSite=Strict`, `Path=/` ;
  - durée 90 jours, renouvelée au plus une fois par jour ;
  - la base n'en garde que l'empreinte SHA-256.
- **Codes :**
  - tirés par `crypto.randomInt` ;
  - conservés sous forme d'empreinte HMAC (clé `COMPTES_SECRET`) et comparés
    en temps constant ;
  - l'adresse email des tables `codes` et `limites` est elle aussi une
    empreinte.
- **Limites anti-abus :**

  | Action | Limite |
  |---|---|
  | Demande de code, par adresse | 5 par heure, et une minute entre deux demandes |
  | Demande de code, par réseau (empreinte d'IP) | 20 par heure |
  | Codes envoyés, pour tout le site | 200 par jour, pour laisser au formulaire de contact et aux rapports leur part des 300 emails quotidiens de Brevo |
  | Vérification, par code | 5 essais |
  | Vérification, par réseau | 30 par heure |

  - **Limite atteinte :** réponse 429 avec un message clair.
  - **Plafond du site atteint :** « Le service d'envoi est très demandé
    aujourd'hui. Réessayez demain, vos outils fonctionnent sans compte. »
- **Origine :**
  - toute demande qui modifie quelque chose (POST, PUT) doit venir du site
    lui-même (en-tête `Origin` identique à l'hôte) et être au format JSON ;
  - sinon : 403.
- **Cloisonnement :**
  - chaque lecture et chaque écriture passent par la session ;
  - aucune adresse n'accepte d'identifiant de compte venu du navigateur ;
  - un test vérifie qu'on ne peut pas lire l'espace d'un autre.
- **Contenu :**
  - la fiche est validée champ par champ, par liste fermée ou par bornes ;
  - le diagnostic, le plan et les calculs doivent être des objets JSON de
    forme attendue ;
  - tout texte est affiché avec `textContent`, jamais en HTML ;
  - les requêtes SQL sont toutes paramétrées.
- **Réponses :** `Cache-Control: no-store` sur toutes les réponses de l'espace.
- **Journaux :**
  - jamais d'adresse email ni de contenu, seulement des codes d'erreur ;
  - le ménage de nuit écrit le nombre de comptes, et rien d'autre.
- **Ce qui ne change pas :**
  - la politique de sécurité du site (CSP), puisque tout passe par `/api`
    sur le même domaine ;
  - aucune bibliothèque dans le navigateur.
- **Région :** toutes les fonctions tournent à Francfort (`fra1`), y compris
  contact, guides et rapport, qui tournent aujourd'hui aux États-Unis
  (région par défaut).

## 6. Architecture technique

**Fonctions (`api/`) :**

| Fichier | Rôle |
|---|---|
| `api/compte.js` (nouveau) | Connexion et compte : `etat`, `demander-code`, `verifier-code`, `deconnexion`, `deconnexion-partout`, `export`, `supprimer` (paramètre `action`). |
| `api/donnees.js` (nouveau) | Lecture (GET) et écriture (PUT, paramètre `cle`) des éléments de l'espace, avec contrôle de version. |
| `api/menage.js` (nouveau) | Ménage de nuit, appelé par Vercel avec `CRON_SECRET`. |
| `api/_base.js` (nouveau) | Accès à la base : pilote Neon en production, base remplaçable dans les tests ; installation du schéma. |
| `api/_session.js` (nouveau) | Cookie, sessions, contrôle d'origine, interrupteur. |
| `api/_limites.js` (nouveau) | Compteurs anti-abus. |
| `api/_elements.js` (nouveau) | Validation de la fiche et des autres éléments, tailles maximales. |
| `api/_brevo.js` | Inchangé ; l'email du code utilise `sendTransactionalEmail` avec une version texte. |

Les fichiers qui commencent par `_` ne deviennent pas des fonctions : le site
passe de trois à six fonctions.

**Adresses :**

| Action | Requête | Connexion requise | Réponse |
|---|---|---|---|
| État | `GET /api/compte?action=etat` | non | `{ouvert:false}`, `{ouvert:true, connecte:false, raison}` ou `{ouvert:true, connecte:true, compte, email, prenom}`. `raison` vaut `null` sans cookie, `expiree` si la connexion a dépassé sa durée, `fermee` si elle a été fermée à distance ou n'existe plus ; les autres adresses répondent 401 avec la même `raison`. |
| Demander un code | `POST /api/compte?action=demander-code` `{email, website}` | non | `{ok:true}`, que l'adresse ait un espace ou non ; 429 si limite ; 502 si l'envoi échoue |
| Vérifier le code | `POST /api/compte?action=verifier-code` `{email, code, prenom?, conditions?}` | non | espace existant : connexion et cookie ; nouvelle adresse sans `conditions:true` : `{ok:true, nouveau:true}`, code non consommé ; avec `conditions:true` : création, connexion et cookie ; erreurs 400 (`essaisRestants`), 410 (expiré), 429 (essais épuisés) |
| Se déconnecter | `POST /api/compte?action=deconnexion` | oui | cookie effacé |
| Tous les appareils | `POST /api/compte?action=deconnexion-partout` | oui | toutes les sessions marquées fermées (`revoquee_le`), cookie de cet appareil effacé |
| Télécharger | `GET /api/compte?action=export` | oui | fichier JSON (`Content-Disposition: attachment`) |
| Supprimer | `POST /api/compte?action=supprimer` `{confirmer:true}` | oui | compte effacé, cookie effacé |
| Lire l'espace | `GET /api/donnees` | oui | `{elements:{cle:{valeur, version, maj}}}` |
| Écrire un élément | `PUT /api/donnees?cle=plan` `{valeur, version}` | oui | `{ok, version, maj}` ; 409 `{actuel}` ; 413 trop grand ; `valeur:null` efface l'élément |
| Ménage | `GET /api/menage` (Vercel, chaque nuit) | `CRON_SECRET` | `{ok, comptes}` |

Interrupteur fermé : `etat` répond `{ouvert:false}` et toutes les autres
adresses répondent 404, sauf le ménage, qui ne fait rien.

**Navigateur :**

| Fichier | Rôle |
|---|---|
| `compte.js` (nouveau) | État de connexion, synchronisation (§ 4.3), feuille « Deux versions du plan », déconnexion. Expose `window.PilotiaCompte`. |
| `compte-outils.js` (nouveau) | Pré-remplissage et calculs gardés des six calculateurs (§ 3.5). |
| `connexion.js` (nouveau) | Les trois étapes de `connexion.html`. |
| `fiche.js` (nouveau) | Le formulaire de `ma-fiche.html`. |
| `mon-espace.js` | Vue connectée, carte d'invitation, « Mon compte », encadré « connexion expirée ». La vue sans compte ne change pas. |
| `style.css` | Nouvelle section « Espace client », avec les jetons existants. |

Tous ces scripts sont en ES5, chargés avec `defer`, sans bibliothèque.

**Pages :**
- `connexion.html`, `ma-fiche.html` et `conditions-espace.html`, créées avec
  `scripts/nouvelle-page.py`, avec la navigation écrite par
  `scripts/navigation-app.py` (onglet « Mon espace », retour « Mon
  espace »).
- Les trois pages portent `noindex` et restent hors du plan du site. À
  l'ouverture, `conditions-espace.html` perd son `noindex` et entre dans
  `sitemap.xml`.

**Configuration :**
- **`vercel.json` :**
  - `"regions": ["fra1"]` ;
  - une tâche planifiée `{"path": "/api/menage", "schedule": "17 3 * * *"}`
    (une fois par jour, comme le permet l'offre gratuite) ;
  - les en-têtes actuels inchangés.
- **`package.json` :** `@neondatabase/serverless` à version exacte, publiée
  depuis plus de deux semaines.
- **Tests :** la base locale `@electric-sql/pglite` n'est installée que dans
  `tests/espace-client/` (son propre `package.json`), jamais publiée.

| Variable | Rôle | Version de test | Site public |
|---|---|---|---|
| `ESPACE_CLIENT` | `ouvert` ouvre l'espace ; toute autre valeur ou absence le ferme | `ouvert` | absente jusqu'à l'ouverture |
| `DATABASE_URL` | Base Neon (posée par l'intégration Vercel) | base `pilotia-test` | base `pilotia`, créée à l'ouverture |
| `COMPTES_SECRET` | Clé des empreintes HMAC, 32 octets aléatoires | oui | oui, différente |
| `CRON_SECRET` | Protège le ménage de nuit | (inutile : les tâches planifiées ne tournent que sur le site public) | oui |
| `BREVO_API_KEY`, `BREVO_SENDER_EMAIL` | Envoi des codes | à ajouter à « Preview » | existantes |

**Ménage de nuit (`api/menage.js`) :**
- **Purge :** codes expirés depuis plus d'une heure, sessions expirées
  (fermées à distance ou non), compteurs de plus de 2 jours.
- **Avertissement :** espaces sans connexion depuis 23 mois et jamais
  avertis. Ils reçoivent un email (« Votre espace Pilotia sera supprimé le
  {date} faute de connexion. Pour le garder, connectez-vous simplement avant
  cette date. »), 50 au plus par nuit.
- **Suppression :** espaces sans connexion depuis 24 mois, avertis depuis au
  moins 25 jours.
- **Remise à zéro :** une connexion efface l'avertissement.
- **Journal :** une ligne avec le nombre de comptes, sans donnée personnelle.
  C'est ainsi que Pilotia voit le nombre de comptes (journaux Vercel, ou
  table `comptes` dans la console Neon).

## 7. Interrupteur et ouverture

**Deux temps :**
1. **Construction :**
   - branche `espace-client`, avec sa version de test Vercel (interrupteur
     ouvert, base `pilotia-test`) ;
   - après validation par le fondateur, le code peut rejoindre `main` avec
     l'interrupteur fermé ;
   - rien ne change pour les visiteurs : la carte reste cachée, les trois
     nouvelles pages ne sont liées nulle part et portent `noindex`, les
     textes légaux sont inchangés.
2. **Ouverture** (le jour où la liste ci-dessous est complète) :
   - fusion de la branche `espace-client-ouverture`, qui porte les textes du
     § 8 et l'identité de l'éditeur ;
   - base de production créée ;
   - interrupteur ouvert sur le site public ;
   - essai réel.

**Liste pour ouvrir au public :**
1. Structure immatriculée : dénomination, numéro BCE, siège et email de
   contact, reportés dans les mentions légales, la confidentialité et les
   conditions.
2. Nom de domaine propre, et domaine authentifié chez Brevo (SPF, DKIM,
   DMARC). Sans cela, les codes risquent d'arriver dans les indésirables, ou
   d'être refusés.
3. Accords de traitement (DPA) acceptés avec Vercel, Neon et Brevo. Celui
   d'Anthropic est déjà noté pour le rapport.
4. Base de production `pilotia` créée chez Neon (Francfort) et reliée au
   seul site public.
5. Conditions d'utilisation relues par un juriste (recommandé).
6. Fiche de l'espace client ajoutée au registre des traitements (§ 8.5).
7. Le jour J :
   - fusion de `espace-client-ouverture` ;
   - variables `ESPACE_CLIENT=ouvert`, `COMPTES_SECRET` et `CRON_SECRET` en
     production ;
   - essai complet avec une vraie adresse.

**Refermer :** retirer `ESPACE_CLIENT` (ou lui donner une autre valeur) et
redéployer prend une minute. Les outils continuent de marcher et les données
restent intactes.

## 8. Textes d'ouverture (à relire par le fondateur)

Publiés le jour de l'ouverture seulement : aujourd'hui, ces pages promettent
« aucun compte », ce qui reste vrai tant que l'espace est fermé. Ils sont
rédigés au style des pages actuelles (apostrophes typographiques, espaces
insécables), sans tiret long. La date de « Dernière mise à jour » devient
celle de l'ouverture.

### 8.1 Politique de confidentialité (`confidentialite.html`)

**En résumé,** remplacé par :

> Ce site ne dépose qu’un seul cookie, et seulement si vous vous connectez à
> votre espace client : il garde votre connexion. Il n’utilise aucun outil de
> mesure d’audience et ne comporte aucun traceur publicitaire. Vos données ne
> sont ni vendues, ni louées, ni transmises à des tiers à des fins
> commerciales. Nous ne collectons que ce que vous nous envoyez
> volontairement, par un formulaire ou par votre espace client, et uniquement
> pour vous rendre le service demandé.

**§ 3, trois lignes ajoutées au tableau :**

| Traitement | Données | Finalité | Base légale | Conservation |
|---|---|---|---|---|
| Espace client | Adresse email ; prénom et fiche entreprise (nom, secteur, statut, régime TVA, chiffre d’affaires, frais fixes, nombre de salariés), tous facultatifs ; résultats que vous enregistrez (diagnostic, plan de trésorerie, derniers calculs) ; dates de création et de dernière connexion | Vous permettre de retrouver vos résultats sur vos appareils et de pré-remplir les outils | Exécution du contrat : conditions d’utilisation de l’espace client (art. 6.1.b) | Jusqu’à la suppression de votre espace ; suppression automatique après 2 ans sans connexion, après un email d’avertissement un mois avant |
| Codes de connexion | Adresse email, code à usage unique (conservé sous forme d’empreinte) | Vérifier que vous êtes titulaire de l’adresse | Exécution du contrat (art. 6.1.b) | 10 minutes, effacé au plus tard le lendemain |
| Protection contre les abus | Empreintes de l’adresse IP et de l’adresse email, nombre de demandes | Limiter les demandes de code et les essais répétés | Intérêt légitime à sécuriser le service (art. 6.1.f) | 2 jours au plus |

**§ 3, paragraphe « Les calculateurs ne transmettent rien »,** remplacé par :

> **Sans espace client, les calculateurs ne transmettent rien.** Le
> calculateur de cotisations, celui du coût d’un salarié, celui de marge,
> celui de la franchise TVA, le générateur de calendrier de contenu et le
> diagnostic express fonctionnent intégralement dans votre navigateur. Les
> chiffres que vous y saisissez ne quittent pas votre appareil, sauf si vous
> choisissez de demander un rapport détaillé ou d’enregistrer vos résultats
> dans votre espace client. Même dans ce cas, personne chez Pilotia ne
> consulte le contenu de votre espace : aucun écran ne le permet, et seul le
> nombre de comptes est suivi. Un accès technique à la base de données n’a
> lieu qu’à votre demande, ou pour réparer une panne.

**§ 4, stockage local :**
- **Introduction :** « Le site n’utilise aucun cookie, hormis le cookie de
  connexion de l’espace client décrit dans la politique cookies. Il peut en
  revanche enregistrer quatre éléments… »
- **Ligne ajoutée au tableau :**
  - clé `pilotia-espace` ;
  - contenu : « Si vous êtes connecté à votre espace client : une copie de
    votre fiche et de vos derniers calculs, et l’état de leur enregistrement
    dans votre espace » ;
  - rôle : « Faire fonctionner les outils sans attendre le réseau, et
    enregistrer vos modifications dans votre espace » ;
  - durée : « Jusqu’à la déconnexion ».
- **Paragraphe final :** « Sans espace client, ces données restent sur votre
  appareil : elles ne sont pas transmises à nos serveurs […]. Avec un espace
  client, elles sont aussi enregistrées dans votre espace (point 3), et la
  déconnexion les efface de l’appareil. »

**§ 5, destinataires et sous-traitants :**

| Prestataire | Rôle | Lieu de traitement |
|---|---|---|
| Vercel Inc. | Hébergement du site et exécution des fonctions serveur | Fonctions exécutées à Francfort (Allemagne) ; société établie aux États-Unis, diffusion mondiale du site |
| Neon (À VÉRIFIER : dénomination exacte dans l’accord de traitement) | Base de données de l’espace client | Union européenne (Francfort, Allemagne) |
| Brevo (Sendinblue SAS) | Envoi des emails, dont les codes de connexion, et gestion des contacts | Union européenne (France) |
| Anthropic PBC | Inchangé | Inchangé |

Le paragraphe sur les transferts hors de l’Union cite désormais « Vercel,
Neon et Anthropic ».

**§ 7, ajout :**

> Si vous avez un espace client, vous exercez vous-même plusieurs de ces
> droits depuis Mon espace : télécharger toutes vos données (accès et
> portabilité), corriger votre fiche (rectification) et supprimer votre
> espace (effacement).

**§ 9, ajout :**

> Pour l’espace client : connexion par code à usage unique ; cookie de
> connexion inaccessible aux scripts de la page et réservé à ce site ; codes
> et clés de connexion conservés uniquement sous forme d’empreinte ; limites
> contre les tentatives répétées ; base de données hébergée dans l’Union
> européenne.

### 8.2 Politique de cookies (`cookies.html`)

**En une phrase,** remplacée par :

> Ce site ne dépose qu’un seul cookie, et seulement si vous vous connectez à
> votre espace client : il garde votre connexion. Ce cookie est strictement
> nécessaire au service que vous demandez : il n’y a donc pas de bandeau de
> consentement à afficher.

**§ 1 :** « Ce site ne dépose aucun cookie, n’utilise aucun outil… » devient
« Ce site ne dépose aucun cookie de mesure ou de publicité, n’utilise aucun
outil… ». Un tableau est ajouté sous le titre « Le cookie de connexion » :
- nom `__Host-pilotia-session` ;
- contenu : un identifiant de connexion aléatoire, sans information
  personnelle ;
- rôle : vous garder connecté à votre espace client ;
- durée : 90 jours, prolongée à chaque visite, et supprimé à la déconnexion ;
- consentement requis : non, strictement nécessaire au service que vous
  demandez ;
- précision : il n’est déposé que si vous vous connectez, aucun script ne
  peut le lire, et il n’est envoyé qu’à ce site.

**§ 2 :**
- « Trois informations » devient « Quatre informations ».
- « elles ne sont jamais jointes aux requêtes réseau et ne quittent jamais
  votre appareil » devient « elles ne sont jamais jointes aux requêtes
  réseau. Sans espace client, elles ne quittent jamais votre appareil ; avec
  un espace client, leur contenu est aussi enregistré dans votre espace, à
  votre demande ».
- La ligne `pilotia-espace` est ajoutée, comme au § 8.1 ; consentement
  requis : « Non, strictement nécessaire au service que vous venez de
  demander ».

**§ 3, ajout :**

> Si vous êtes connecté, « Se déconnecter » efface ces données de l’appareil :
> elles restent dans votre espace. « Supprimer mon espace » les efface
> partout.

### 8.3 Plan de trésorerie (`plan-tresorerie.html`)

**« 7. Garder votre plan » :**

> **Sans compte, vos chiffres ne quittent jamais votre appareil.** Tout est
> calculé dans votre navigateur et enregistré localement : rien n'est envoyé
> à Pilotia, et personne d'autre que vous n'y a accès.
>
> La contrepartie : cet enregistrement est propre à ce navigateur. Il
> disparaît si vous videz vos données de navigation, et ne suit pas sur un
> autre appareil. **Exportez votre plan** pour le conserver, ou créez votre
> espace Pilotia, gratuit et facultatif : votre plan vous suivra sur
> téléphone et ordinateur, visible par vous seul.

(« espace Pilotia » est un lien vers `mon-espace.html`.)

**Questions fréquentes, trois réponses modifiées :**
- **« Est-ce que Pilotia voit mes chiffres ? »**

  > Non. Sans compte, tout est calculé dans votre navigateur et enregistré
  > sur votre appareil : aucun montant n'est envoyé à Pilotia. C'est
  > vérifiable : la page fonctionne hors connexion une fois chargée. Si vous
  > choisissez de créer votre espace client, votre plan y est aussi
  > enregistré pour vous suivre d'un appareil à l'autre : il reste visible
  > par vous seul, et personne chez Pilotia ne le consulte.
- **« Pourquoi ne pas connecter directement ma banque ? »** La fin devient :

  > Pilotia n'a ni l'un ni l'autre, et tient à ce que vos chiffres ne
  > quittent votre appareil que si vous le choisissez. La saisie manuelle est
  > le prix assumé de ce choix.
- **« Mes données suivent-elles si je change d'ordinateur ? »**

  > Sans compte, non : l'enregistrement est propre à ce navigateur, sur cet
  > appareil, et disparaît si vous videz vos données de navigation. Utilisez
  > le bouton d'export pour conserver votre plan, ou créez votre espace
  > client, gratuit et facultatif : votre plan vous suivra alors sur tous vos
  > appareils.

Les données structurées (`FAQPage`, dans l'en-tête de la page) reprennent ces
trois réponses, sous leur forme courte actuelle. La réponse « Faut-il payer,
ou laisser une adresse e-mail ? » ne change pas : l'outil reste sans
inscription.

**Autres fichiers mis à jour à l'ouverture :**
- `README.md` : sa section cookies ;
- `llms.txt` : la ligne « aucun cookie déposé » devient « un seul cookie, de
  connexion à l'espace client facultatif » ;
- `sitemap.xml` : ajout de `conditions-espace.html` ;
- tests de texte : ces changements sont listés, un par un, parmi les
  exceptions autorisées.

### 8.4 Conditions d'utilisation de l'espace client (`conditions-espace.html`)

Page créée dès la construction (elle est liée depuis l'étape Bienvenue), avec
`noindex` et l'identité « À COMPLÉTER » comme les mentions légales actuelles.
Texte proposé, à faire relire par un juriste :

> **Conditions d’utilisation de l’espace client**
>
> **1. Objet.** Les présentes conditions encadrent l’utilisation de l’espace
> client Pilotia, un service gratuit et facultatif qui permet d’enregistrer
> une fiche entreprise et les résultats des outils du site (diagnostic
> express, plan de trésorerie, derniers calculs) pour les retrouver sur
> plusieurs appareils. L’éditeur du service est identifié dans les mentions
> légales : À COMPLÉTER.
>
> **2. Accès.** L’espace client est gratuit. Il n’est pas nécessaire pour
> utiliser les outils du site, qui restent librement accessibles sans
> compte. Sa création suppose une adresse email valide dont vous avez
> l’usage, et l’acceptation des présentes conditions.
>
> **3. Connexion.** La connexion se fait par un code à usage unique envoyé à
> votre adresse email. Toute personne qui a accès à votre boîte email peut
> donc entrer dans votre espace : il vous appartient de la protéger. En cas
> de perte d’un appareil, la fonction « Se déconnecter de tous mes
> appareils » met fin à toutes les connexions en cours.
>
> **4. Vos données.** Les informations que vous enregistrez dans votre
> espace vous appartiennent. Elles ne servent qu’à vous rendre le service :
> les afficher, les synchroniser entre vos appareils et pré-remplir les
> outils. Pilotia ne les consulte pas, ne les vend pas et ne les utilise à
> aucune fin commerciale. Leur traitement est décrit dans la politique de
> confidentialité. Vous pouvez à tout moment les télécharger, les corriger ou
> les supprimer depuis Mon espace.
>
> **5. Nature des outils.** Les outils et leurs résultats sont fournis à
> titre indicatif, à partir des informations que vous saisissez. Ils ne
> constituent ni une comptabilité, ni une déclaration, ni un conseil fiscal,
> juridique ou financier, et ne remplacent pas l’avis d’un professionnel
> (comptable, conseil fiscal, avocat). Les décisions prises à partir de ces
> résultats relèvent de votre seule appréciation.
>
> **6. Disponibilité.** Pilotia s’efforce de garder le service accessible,
> sans pouvoir garantir une disponibilité continue : une maintenance, une
> panne ou une cause extérieure peut l’interrompre. Les données présentes sur
> votre appareil restent utilisables pendant une interruption. Si le service
> devait fermer définitivement, vous en seriez informé par email au moins
> 30 jours à l’avance, avec la possibilité de télécharger vos données.
>
> **7. Durée et suppression.** Vous pouvez supprimer votre espace à tout
> moment depuis Mon espace : la suppression est immédiate et définitive. Un
> espace où aucune connexion n’a eu lieu pendant 2 ans est supprimé, après un
> email d’avertissement envoyé un mois avant. Pilotia peut suspendre ou
> supprimer un espace utilisé de façon abusive (tentatives d’intrusion,
> surcharge volontaire du service, usage contraire à la loi), après vous en
> avoir informé, sauf urgence.
>
> **8. Responsabilité.** Le service est gratuit et ses résultats sont
> indicatifs. Rien dans les présentes conditions n’exclut ni ne limite la
> responsabilité de Pilotia en cas de dol ou de faute grave, ni dans les cas
> où la loi l’interdit.
>
> **9. Modification des conditions.** Ces conditions peuvent évoluer. En cas
> de modification importante, vous en êtes informé par email au moins
> 30 jours avant son entrée en vigueur ; vous pouvez alors supprimer votre
> espace si vous ne l’acceptez pas.
>
> **10. Droit applicable et litiges.** Les présentes conditions sont soumises
> au droit belge. En cas de difficulté, écrivez d’abord à Pilotia : À
> COMPLÉTER (email). Si vous agissez en tant que consommateur, vous
> conservez la protection des règles impératives de votre pays de résidence
> et pouvez vous adresser au Service de médiation pour le consommateur
> (mediationconsommateur.be).

`conditions_version` vaut la date de la version acceptée (par exemple
`2026-10-13`). Une nouvelle version importante suit le § 9 des conditions.

### 8.5 Fiche du registre des traitements

À recopier dans le registre de Pilotia (article 30 du RGPD) :

| Rubrique | Contenu |
|---|---|
| Traitement | Espace client Pilotia |
| Responsable | À COMPLÉTER (identité de l’éditeur) |
| Finalités | Permettre aux utilisateurs qui le souhaitent de retrouver leurs résultats et leur fiche entreprise sur plusieurs appareils, et de pré-remplir les outils du site |
| Bases légales | Exécution du contrat, conditions d’utilisation acceptées (art. 6.1.b) ; intérêt légitime pour la sécurité du service, limites anti-abus (art. 6.1.f) |
| Personnes concernées | Utilisateurs du site ayant créé un espace : indépendants, dirigeants de petites entreprises, porteurs de projet |
| Données | Adresse email ; prénom ; fiche entreprise (nom, secteur, statut, régime TVA, chiffre d’affaires, frais fixes, nombre de salariés), facultative ; résultats enregistrés (diagnostic, plan de trésorerie, derniers calculs) ; dates de création et de connexion ; empreintes techniques (sessions, codes, IP pendant 2 jours au plus) |
| Destinataires | Aucun destinataire commercial. Sous-traitants : Vercel (hébergement et fonctions, Francfort), Neon (base de données, Francfort), Brevo (envoi des emails, France) |
| Transferts hors UE | Vercel et Neon sont des sociétés établies aux États-Unis : garanties de leurs accords de traitement (clauses contractuelles types, Data Privacy Framework), À VÉRIFIER dans chaque accord |
| Durées | Jusqu’à suppression par l’utilisateur ; suppression après 2 ans sans connexion, avertissement un mois avant ; codes 10 minutes (25 au plus pour une création) ; sessions 90 jours renouvelables ; compteurs anti-abus 2 jours |
| Sécurité | HTTPS et HSTS ; cookie `HttpOnly`, `Secure`, `SameSite=Strict` ; codes et jetons conservés sous forme d’empreinte ; limites anti-abus ; contrôle d’origine ; données hébergées dans l’UE ; aucun écran d’administration ; journaux sans donnée personnelle |

## 9. Vérifications automatiques

- **Suite existante :** toutes les vérifications du format app passent
  toujours (`tests/format-app`). Les trois nouvelles pages sont ajoutées au
  tableau des onglets. Sans compte, rien ne change :
  - texte identique au mot près ;
  - ordinateur identique au pixel près ;
  - contraste, zones à toucher, aucun tiret long.
- **Nouvelles vérifications (`tests/espace-client`) :**
  - **Montage :** un serveur local fait tourner les vraies fonctions `api/`
    sur une vraie base Postgres en mémoire (PGlite). Les emails sont
    interceptés et lus par les tests ; aucun envoi réel.
  - **Adresses :**
    - code juste, faux, expiré, épuisé ;
    - création avec et sans conditions ;
    - réponse identique pour une adresse inconnue ;
    - limites (adresse, réseau, site) ;
    - versions et refus 409 ;
    - tailles maximales ;
    - export complet ;
    - suppression en cascade.
  - **Sécurité :**
    - attributs du cookie ;
    - origine étrangère refusée (403) ;
    - aucun moyen de lire ou d'écrire l'espace d'un autre ;
    - texte piégé dans la fiche affiché sans être interprété ;
    - requêtes SQL paramétrées (recherche automatique de concaténation) ;
    - aucune adresse email dans les journaux.
  - **Parcours sur téléphone simulé (Playwright, 390 px) :**
    - création avec l'encadré « Déjà sur cet appareil » ;
    - fiche et calculateurs pré-remplis (dont le × 12) ;
    - calcul gardé puis repris ;
    - déconnexion qui vide l'appareil ;
    - téléchargement ;
    - suppression.
  - **Deux appareils simulés :**
    - un plan créé sur l'un apparaît sur l'autre ;
    - feuille « Deux versions du plan » et ses deux choix ;
    - diagnostic le plus récent gardé ;
    - fusion des calculs ;
    - connexion expirée puis reprise ;
    - connexion fermée à distance, qui vide l'autre appareil ;
    - changement de compte sur un même appareil.
  - **Interrupteur fermé :**
    - aucune carte ;
    - adresses fermées (404) ;
    - aucune requête sur les pages d'outils ;
    - Mon espace identique à aujourd'hui.
  - **Ménage :** purge, avertissement à 23 mois, suppression à 24 mois,
    remise à zéro par une connexion, plafond de 50 emails.
  - **Accessibilité :**
    - focus à chaque étape et erreurs annoncées ;
    - zones à toucher de 48 px ;
    - contrastes en clair et en sombre ;
    - feuilles utilisables au clavier.
  - **Sans JavaScript :** message clair sur `connexion.html` et
    `ma-fiche.html`.

## 10. Déroulé

1. **Ce document,** relu par le fondateur.
2. **Plan de travail détaillé** (`espace-client-PLAN.md`), produit comme
   celui du format app : déroulé à blanc dans une copie de travail, puis
   rejoué sur une copie neuve.
3. **Construction** sur la branche `espace-client`, avec deux étapes à la
   charge du fondateur, guidées pas à pas (environ 10 minutes) :
   1. **Base de test :** dans Vercel, Storage, créer une base Neon (offre
      gratuite, région Francfort) nommée `pilotia-test`, reliée à
      l'environnement Preview seulement, jamais à Production.
   2. **Réglages Brevo :** dans Vercel, Settings, Environment Variables,
      ajouter « Preview » à `BREVO_API_KEY` et `BREVO_SENDER_EMAIL`. Ces
      variables protégées ne peuvent pas être lues, donc pas recopiées.

   `ESPACE_CLIENT` et `COMPTES_SECRET` (Preview) sont posées par Claude,
   avec l'accord du fondateur au moment venu.
4. **Version de test :** essai par le fondateur avec sa vraie adresse, sur
   téléphone et sur ordinateur.
5. **Fusion dans `main`,** interrupteur fermé : rien de visible.
6. **Ouverture** selon le § 7.

## 11. Risques et parades

| Risque | Parade |
|---|---|
| Un code n'arrive pas (indésirables, refus) | Domaine propre authentifié chez Brevo avant l'ouverture ; conseil « Regardez dans vos courriers indésirables » ; renvoi après une minute. |
| Quota d'emails Brevo épuisé | Plafond de 200 codes par jour pour l'espace, connexion gardée 90 jours. |
| Quota gratuit de Neon atteint (base en pause jusqu'au mois suivant) | Base qui s'endort après 5 minutes, données légères ; usage à surveiller dans la console Neon ; offre payante à l'usage si besoin. |
| Un plan écrasé par un autre appareil | Contrôle de version et feuille « Deux versions du plan » ; jamais d'écrasement silencieux. |
| Modification perdue à la fermeture de la page | Envoi toutes les 3 secondes, puis en `keepalive` à la fermeture ; à défaut, la modification attend sur l'appareil. |
| Vol de la base | Codes et jetons sous forme d'empreinte ; aucune donnée bancaire ni sensible. |
| Prise de contrôle par la boîte email | Codes à usage unique de 10 minutes, 5 essais ; « Se déconnecter de tous mes appareils ». |
| Texte légal qui ne correspond plus au service | Textes d'ouverture préparés ici, publiés seulement à l'ouverture ; interrupteur fermé jusque-là. |
| Panne de l'espace | Les outils lisent la copie de l'appareil et continuent de marcher ; l'interrupteur se referme en une minute. |
