# Dossier Google Business Profile — Pilotia

À déposer **le jour de l'immatriculation à la BCE**, pas avant : Google demande
une preuve d'activité, et une fiche créée puis suspendue est pénible à
récupérer.

Pour une activité comme la tienne, la fiche Google pèse souvent plus lourd que
le site lui-même sur les requêtes locales (« coach entreprise Liège », « aide
gestion indépendant Namur »). C'est le canal le plus rentable et il est gratuit.

---

## 1. La première décision : adresse visible ou zone de service

| | Adresse visible | Zone de service |
|---|---|---|
| Ce que voit le public | Ton adresse complète | Seulement les communes desservies |
| Convient si | Tu reçois des clients sur place | Tu te déplaces chez eux |
| Domiciliation | Acceptée si tu y es joignable | Adresse masquée, mais exigée quand même |

**Recommandation : zone de service.** Tu te déplaces chez tes clients, et une
adresse personnelle publiée sur Google est difficile à retirer ensuite. Google
demande malgré tout une adresse réelle lors de la vérification — elle reste
simplement masquée.

Déclare au maximum **20 communes ou une province**. Ne coche pas toute la
Belgique : une zone trop large dilue le classement au lieu de l'élargir.

---

## 2. Catégories

Le classement local dépend fortement de la catégorie principale. Une seule est
prise en compte comme catégorie forte ; les autres sont secondaires.

- **Principale** : « Conseiller d'entreprise » (ou l'intitulé le plus proche
  proposé par le sélecteur — les libellés exacts varient et ne se saisissent
  pas librement).
- **Secondaires**, deux ou trois maximum : conseil en gestion, service de
  comptabilité *uniquement si tu es en droit de l'exercer*, marketing.

> **Attention.** Ne coche **jamais** une catégorie d'expert-comptable ou de
> conseil fiscal. Ce sont des professions réservées (ITAA) et le site dit
> explicitement que Pilotia n'en relève pas. Une fiche qui contredit tes
> mentions légales est un risque réglementaire, pas une astuce SEO.

---

## 3. Description (750 caractères maximum)

À coller telle quelle :

> Pilotia accompagne les PME, commerçants et indépendants en Belgique
> francophone sur ce qui se voit dans les chiffres : organisation, marges,
> coûts, trésorerie et présence digitale. Diagnostic de départ, plan d'action
> concret, puis suivi régulier des indicateurs qui comptent pour votre
> activité. Outils gratuits en accès libre sur le site : plan de trésorerie
> prévisionnel, calculateurs de cotisations sociales, de coût d'un salarié, de
> marge et de franchise TVA. Pilotia exerce une activité de conseil en gestion
> d'entreprise et n'est ni expert-comptable, ni conseil fiscal, ni avocat.
> Premier appel de cadrage gratuit.

La dernière phrase n'est pas de la modestie : elle protège la fiche.

---

## 4. Services à déclarer

Un par ligne, avec sa description courte. Ils apparaissent dans la fiche et
sont indexés.

| Service | Description courte |
|---|---|
| Diagnostic d'entreprise | Analyse de l'organisation, des marges et de la trésorerie, avec plan d'action. |
| Suivi de gestion | Lecture mensuelle des chiffres et arbitrages, en continu. |
| Gestion administrative | Mise en ordre des documents, des échéances et des processus. |
| Présence digitale | Fiche Google, site, contenus et visibilité locale. |
| Accompagnement au lancement | Cadrage d'une activité indépendante : statut, prix, prévisionnel. |

---

## 5. Questions à amorcer toi-même

Google autorise le propriétaire à poser **et** répondre. Fais-le : sinon
n'importe qui pose la première question, et c'est elle qui s'affiche.

1. *Faut-il déjà être immatriculé pour vous consulter ?* — Non, l'accompagnement
   au lancement porte justement sur cette étape.
2. *Vous remplacez mon comptable ?* — Non. Pilotia travaille l'organisation et
   la gestion ; les actes comptables et fiscaux restent chez un professionnel
   agréé.
3. *Vous vous déplacez ?* — Oui, sur la zone indiquée. Le premier appel de
   cadrage se fait à distance et il est gratuit.
4. *Les outils du site sont-ils vraiment gratuits ?* — Oui, sans inscription,
   et les données saisies restent sur votre appareil.

---

## 6. Photos

La fiche sans photo plafonne. Minimum viable :

- **Logo** : `icon-512.png`.
- **Photo de couverture** : format paysage, 1920 × 1080.
- **3 à 5 photos** : toi au travail, un document de travail lisible, une
  capture du plan de trésorerie. Pas de banque d'images — Google et les
  visiteurs repèrent les photos génériques.

Ajoute-en une par mois : la fraîcheur compte dans le classement local.

---

## 7. Cohérence NAP — la règle qui casse tout si on l'oublie

**N**om, **A**dresse, **P**hone doivent être identiques **au caractère près**
partout : fiche Google, `mentions-legales.html`, `contact.html`, et tout
annuaire. « Rue de la Station 4 » et « rue de la station, 4 » comptent comme
deux entreprises différentes pour les algorithmes locaux.

Fixe la forme canonique une fois, note-la ici, et recopie-la partout.

```
Dénomination : ………
Adresse      : ………
Téléphone    : ………
BCE          : BE 0………
```

---

## 8. Ce qui reste à faire côté site, une fois ces données connues

1. Remplacer les `À COMPLÉTER` de `mentions-legales.html` (art. XII.6 CDE —
   obligation légale, pas une option).
2. Ajouter le bloc `PostalAddress` et le `telephone` au nœud
   `ProfessionalService` de `index.html`, et le passer en `LocalBusiness`.
3. Publier le téléphone en `tel:` dans le pied de page et sur `contact.html`.
4. Relier la fiche Google au site via `sameAs`.

Tant que ces quatre points ne sont pas faits, le SEO local reste théorique :
`areaServed` est déclaré, mais aucune identité vérifiable ne l'appuie.
