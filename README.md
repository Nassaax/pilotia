# Pilotia — accompagnement d'entreprise, présence digitale et aide simple aux indépendants

Site vitrine pour un service de coaching destiné aux petites entreprises belges (restaurants, entreprises du bâtiment, commerces...) et aux futurs indépendants. Positionnement : premium, épuré, orienté confiance ("Pilotia" = piloter son entreprise, garder le cap et les commandes).

Ce dépôt contient une **structure complète de site** (25 pages, contenu réel, 6 outils interactifs, direction visuelle provisoire) à valider avant d'investir dans le design final.

## Périmètre du service — important

Le fondateur n'est **pas comptable agréé** (bachelier, pas de titre professionnel protégé). Le site est volontairement limité à des tâches simples et ne doit jamais donner l'impression d'un service comptable, fiscal ou de conseil en restructuration financière. Trois missions claires :

1. **Résoudre des problèmes simples pour les indépendants** — démarches, checklists, estimations basées sur des barèmes publics (cotisations, TVA).
2. **Aider les entrepreneurs en difficulté** — diagnostic organisationnel et repérage de marge, pas de restructuration financière formelle (on oriente vers un comptable / expert en réorganisation si besoin).
3. **Faciliter la promotion sur les réseaux sociaux** — le pilier le plus développé du site.

En conséquence, ont été **retirés** du site (voir historique git) :
- Le comparateur de statut personne physique / société (calcul IPP vs ISOC) — trop proche du conseil fiscal personnalisé.
- Le simulateur de trésorerie prévisionnelle sur 12 mois — "le plan prévisionnel n'est pas pour moi" (demande explicite).
- Le "modèle de plan financier prévisionnel" téléchargeable — remplacé par une simple checklist des charges à prévoir.

Une section **"Ce que Pilotia n'est pas"** a été ajoutée à `a-propos.html`, et les pages restantes ont été relues pour retirer tout vocabulaire d'"analyse financière approfondie" au profit de formulations simples ("comprendre ses chiffres", "repérer ce qui coûte cher"). Les outils de calcul conservés (cotisations INASTI, franchise TVA, marge, coût d'un salarié) appliquent des barèmes publics de façon mécanique — comme le font de nombreux simulateurs grand public — et rappellent chacun que ce n'est pas un conseil comptable ou fiscal personnalisé.

## Décisions déjà prises

- **Nom de marque :** Pilotia
- **Marché cible :** Belgique (législation, fiscalité et cotisations sociales belges — à titre informatif uniquement)
- **Deux parcours, à égalité :**
  - Entreprises déjà en activité (`entreprises.html`) — diagnostic simple, gestion du personnel, marges, présence digitale
  - Futurs indépendants (`independants.html`) — démarches, repères financiers simples, documents de lancement
- **Modèle économique :** freemium — ressources/documents/outils gratuits en haut de tunnel, coaching payant (diagnostic ponctuel ou suivi mensuel) en conversion, plus deux automatisations de revenu/capture ajoutées ci-dessous.

## Arborescence du site (25 pages)

```
Cœur du site
  index.html            Accueil — aiguillage vers les 2 parcours, témoignages, 3 leviers
  entreprises.html       Parcours PME existantes
  independants.html      Parcours futurs indépendants
  marketing-digital.html  Pilier présence digitale & réseaux sociaux (diagnostic, offre, FAQ)
  methode.html            Méthode en 4 étapes (écouter / diagnostiquer / décider / piloter)
  offres.html              Tarifs et formules (grille indicative chiffrée, incl. présence digitale)
  ressources.html          Bibliothèque de documents gratuits (lead magnets)
  outils.html               Hub des 6 outils interactifs
  a-propos.html              Positionnement, valeurs, bio (template), section "ce que Pilotia n'est pas"
  statistiques.html           Chiffres clés PME/indépendants Belgique (sourcés)
  contact.html                  Prise de rendez-vous + formulaire

Outils interactifs (JS vanilla, calculs côté client, barèmes publics 2026)
  diagnostic.html                          Diagnostic express noté sur 8 questions / 4 thèmes
  rapport-diagnostic.html                    Rapport détaillé payant (19 €), généré par IA à partir du diagnostic
  calculateur-cotisations-independant.html   Barème INASTI 2026 — estimation simple
  calculateur-tva-franchise.html             Seuil de franchise TVA (25 000 €, 2026) — information générale
  calculateur-marge.html                     Marge produit/prestation + seuil de rentabilité
  calculateur-cout-salarie.html              Coût réel annuel d'un salarié (charges patronales 2026)
  generateur-calendrier-contenu.html         Calendrier de contenu réseaux sociaux sur 4 semaines, par secteur

Automatisation de revenu (fonctions serverless Vercel, voir "Note technique")
  api/subscribe.js         Capture d'email (ressources.html, outils.html) → ajoute le contact dans Brevo
  api/generate-report.js    Rapport diagnostic détaillé : appelle Claude, génère un PDF, tente l'envoi par email
  api/_brevo.js              Helper partagé (appels API Brevo)

Contenu / SEO
  conseils.html                     Hub des articles
  conseils-marge-restaurant.html      Article — erreurs de marge en restauration
  conseils-chiffrer-chantier.html     Article — bien chiffrer un chantier
  conseils-lancer-independant.html    Article — checklist avant de se lancer (statut = orientation vers comptable)

Légal & technique
  mentions-legales.html, confidentialite.html, cgv.html   Pages légales (squelettes à finaliser)
  404.html
  style.css              Direction visuelle provisoire (palette neutre + accent vert foncé/or)
  robots.txt, sitemap.xml, vercel.json   SEO et headers de sécurité (domaine placeholder à mettre à jour)
```

## Ce qui est réel vs. placeholder

**Réel et vérifié par recherche web (barèmes publics, cités dans `statistiques.html` et les encarts "note" de chaque outil) :**
- Cotisations sociales indépendant 2026 (INASTI) : 20,5 % jusqu'à 75 024,54 €, 14,16 % jusqu'à 110 562,42 €, exonération au-delà ; cotisation trimestrielle min. 917,58 €, max. 5 258,69 €.
- Seuil de franchise TVA 2026 : 25 000 € de chiffre d'affaires annuel, sans tolérance de dépassement depuis 2025.
- Cotisations patronales ONSS 2026 : ~25 % du brut (employés), ~30-35 % (ouvriers) ; réduction "premier engagement" 2 000 €/trimestre à partir d'avril 2026.
- Statistiques PME/faillites Belgique (SPF Économie, Statbel, UCM, GraydonCreditsafe) — voir sources dans `statistiques.html`.
- Bio du fondateur (`a-propos.html`) : Nasser Yasini, bachelier en comptabilité, expérience en fiduciaire, gestion des salaires et immobilier — pas de titre de comptable agréé revendiqué.
- Témoignages clients (`index.html` contient 5 vrais retours clients, attribués par prénom et métier : Sylvain coiffeur, Sarah esthéticienne, Gabriel boulanger, Farah agent immobilier, Lucas restaurateur).
- Réservation d'appel : `contact.html` renvoie vers le vrai lien Cal.com (https://cal.com/pilotia/call), créneaux de 15 minutes.
- Logo réel (fourni par le client) : favicon/apple-touch-icon, image de partage réseaux sociaux, en-tête du PDF de lancement, et header/footer du site (bascule automatique clair/sombre).
- Bouton de bascule thème clair/sombre dans le header (toutes pages), indépendant du réglage système, préférence mémorisée par visiteur.
- **Capture d'email réelle sur les lead magnets** (`ressources.html`, `outils.html`) : le guide PDF "Les étapes pour devenir indépendant" est maintenant derrière un formulaire email → `api/subscribe.js` → contact ajouté dans Brevo, puis téléchargement immédiat. Nécessite `BREVO_API_KEY` (voir `.env.example`) ; sans elle, le formulaire répond une erreur claire au lieu de faire semblant.
- **Rapport diagnostic détaillé payant** (`rapport-diagnostic.html`, 19 €) : reprend les réponses du diagnostic express + quelques questions complémentaires, génère un rapport PDF personnalisé via l'API Claude (`api/generate-report.js`), tente l'envoi par email (Brevo) et le propose en téléchargement immédiat dans tous les cas. **Le paiement n'est pas encore activé** (décision explicite) — la page affiche "version test, gratuit pendant le lancement" ; brancher Stripe Checkout avant l'appel à Claude quand vous serez prêt à facturer. Nécessite `ANTHROPIC_API_KEY`.

- **Les 8 documents téléchargeables existent réellement** et sont générés par `scripts/documents.js` (contenu) + `scripts/generer-pdf.js` (mise en page), via `pdfkit`. Relancer avec `node scripts/documents.js` après toute correction de contenu. Répartition : fiches courtes en accès libre, guides complets derrière la capture d'email.

- **Plan de trésorerie prévisionnel** (`plan-tresorerie.html` + `tresorerie.js`) : projection du solde mois par mois sur 3, 6 ou 12 mois, point bas anticipé, seuil de sécurité, plan mensuel détaillé, export JSON et CSV. Saisie manuelle, **aucune connexion bancaire** — l'open banking (DSP2) suppose un agrément ou un agrégateur payant. Les données restent dans le `localStorage` du visiteur : rien ne transite par le serveur, donc aucun traitement de données d'entreprise à sécuriser ni à déclarer. Cotisations sociales et TVA sont pré-remplies en fréquence **trimestrielle**, le rythme belge qui crée les creux de trésorerie. Les **factures engagées** (à encaisser / à payer, avec date d'échéance) entrent dans la projection au mois de leur échéance et cessent de compter une fois cochées « réglée » ; une échéance dépassée est rattachée au premier mois avec une alerte. Format de données versionné, avec migration douce des plans enregistrés.

**Placeholder, à compléter avant mise en ligne :**
- Photo ou avatar du fondateur sur `a-propos.html` — l'avatar vectoriel produit n'a pas été retenu, l'emplacement attend une vraie photo ou un avatar fourni
- Grille tarifaire (`offres.html`) : chiffres indicatifs de démarrage (490 €, 390 €/mois, 390 € formule lancement) à valider selon votre positionnement réel
- **`BREVO_API_KEY` et `ANTHROPIC_API_KEY`** — variables d'environnement à créer dans Vercel pour activer la capture d'email et le rapport IA (voir `.env.example`). Sans elles, ces fonctionnalités répondent une erreur claire plutôt que de planter silencieusement.
- **Paiement du rapport diagnostic (19 €)** — le flux technique est prêt (formulaire → IA → PDF → email) mais le paiement Stripe n'est pas branché ; le rapport est actuellement généré gratuitement, avec une mention "version test" visible sur la page.
- **Identité légale** — les pages juridiques sont rédigées mais comportent des marqueurs `[À COMPLÉTER]` bien visibles : dénomination exacte, forme juridique, numéro BCE, siège, email professionnel. À remplir dès l'immatriculation, **avant** toute prestation payante.
- Domaine réel : `robots.txt`, `sitemap.xml`, `llms.txt`, le JSON-LD et les balises `og:url`/`og:image` utilisent `pilotis-murex.vercel.app`, qui est le **vrai domaine Vercel actuel** (vérifié via l'API Vercel). À remplacer partout une fois `pilotia.be` actif.

## Conformité, vie privée et accessibilité

Audit réalisé le 20 septembre 2026 sur l'ensemble des 34 pages.

**Ce que le site collecte réellement** — inventaire vérifié, pas déclaratif :
- `contact.html` → `api/contact.js` : nom, email, entreprise (facultatif), profil, message. Consentement explicite obligatoire. L'expéditeur n'est **pas** ajouté à la liste marketing (détournement de finalité).
- `ressources.html` / `outils.html` → `api/subscribe.js` : email seul, contre le guide PDF.
- `rapport-diagnostic.html` → `api/generate-report.js` : prénom, email, secteur, taille d'équipe, difficulté, réponses au diagnostic.
- Journaux techniques Vercel : IP, horodatage, page, navigateur.
- **Les six calculateurs et le diagnostic express ne transmettent rien** : tout se calcule dans le navigateur.

**Cookies : il n'y en a aucun.** Aucun outil de mesure d'audience, aucun pixel, aucune iframe tierce. Seulement deux clés `localStorage` (`pilotia-theme`, `pilotia-diagnostic`), toutes deux couvertes par l'exemption « strictement nécessaire » de l'article 5.3 ePrivacy. **Aucun bandeau de consentement n'est donc requis** — `cookies.html` documente ce raisonnement et liste ce qui le ferait basculer (analytics, paiement en ligne, iframe de réservation, script tiers).

**Correctif RGPD majeur : polices auto-hébergées.** Les polices étaient chargées depuis `fonts.googleapis.com` / `fonts.gstatic.com`, ce qui transmettait l'IP de chaque visiteur à Google LLC (États-Unis) à chaque page vue, sans consentement ni nécessité. Elles sont désormais servies depuis `fonts/` (sous-ensembles latin/latin-ext uniquement, Inter en police variable : 598 Ko → 208 Ko). La CSP a été resserrée en conséquence. **Vérifié : l'audit navigateur ne relève plus aucune requête sortante vers un tiers sur les 34 pages.**

**Pages juridiques** (`mentions-legales.html`, `confidentialite.html`, `cgv.html`, `cookies.html`, `accessibilite.html`) :
- CGV rédigées en **B2B** (obligation de moyens, pas de droit de rétractation, clause d'exclusion des consommateurs, intérêts de retard loi du 2 août 2002), régime **franchise de TVA art. 56bis**.
- **Aucun lien vers la plateforme ODR européenne** : elle a définitivement fermé le 20 juillet 2025 et la mention n'est plus obligatoire. Beaucoup de modèles de CGV en circulation y renvoient encore à tort.
- Exclusion explicite des actes réservés aux professions réglementées (ITAA, conseil fiscal, conseil juridique).

**Accessibilité** — contrastes calculés, pas estimés :
- `--gold` passait à 3,20:1 sur `--paper-alt` alors que `.eyebrow` fait 12px : assombri en `#876231` (4,89:1). Variante mode sombre `#C69B62` ajoutée.
- Bordures de champs à 1,18:1 → nouveau jeton `--line-strong` (3,25:1), requis par le critère 1.4.11 puisque le fond du champ est blanc comme la page.
- `--danger` n'avait pas de variante sombre (3,61:1) → `#F87171`.
- Lien d'évitement et repère `<main>` ajoutés sur les 34 pages ; hiérarchie de titres corrigée (plus aucun saut h1→h3) ; `alt` du logo d'en-tête rendu explicite et logo de pied de page passé en décoratif.
- **40 paires de couleurs vérifiées en clair et en sombre : 0 échec.**

**Accessibilité pour les agents IA** : `llms.txt` (résumé structuré + mises en garde sur les professions réglementées), JSON-LD `ProfessionalService` + `WebSite` sur l'accueil, `robots.txt` autorisant explicitement les principaux crawlers IA.

**Ce qui reste à faire côté conformité :**
1. Remplir les marqueurs `[À COMPLÉTER]` dès l'immatriculation BCE.
2. Signer les accords de sous-traitance (art. 28 RGPD) avec Brevo, Vercel et Anthropic.
3. Tenir un **registre des traitements** (art. 30) — l'exemption « moins de 250 salariés » ne joue pas ici, les traitements clients n'étant pas occasionnels.
4. Confirmer dans le contrat Anthropic que les contenus envoyés ne servent pas à l'entraînement, puis retirer le marqueur correspondant dans `confidentialite.html`.
5. Faire relire les CGV et la politique de confidentialité par un juriste avant la première facturation.

## Prochaines étapes suggérées

1. **Créer les comptes Brevo et Anthropic, ajouter les clés dans Vercel** (voir `.env.example`) pour activer la capture d'email et le rapport IA — sans ça, ces deux fonctionnalités répondent une erreur claire aux visiteurs.
2. **Brancher Stripe** sur `api/generate-report.js` pour faire payer réellement les 19 € du rapport détaillé (le code est prêt à recevoir cette étape, voir le commentaire en tête du fichier).
3. Personnaliser `a-propos.html` avec un vrai parcours et une vraie photo (sans survendre de titre non détenu).
4. Créer la structure juridique (statut choisi avec un comptable) pour pouvoir remplir les pages légales.
5. Produire les documents téléchargeables réels du kit de lancement et du kit pilotage PME.
6. Passer à un design final une fois le concept validé.
8. Faire vérifier les chiffres légaux restants (INASTI, TVA, ONSS) par un professionnel avant toute communication commerciale — ce sont des estimations pédagogiques basées sur des barèmes publics, pas des avis fiscaux.
9. Faire relire le contenu généré par `api/generate-report.js` sur quelques cas réels avant de pousser le trafic dessus — c'est un prompt système qui encadre le ton et interdit le conseil fiscal/comptable, mais une relecture humaine reste utile au lancement.

## Vocabulaire retenu

Décidé avec le client, appliqué sur l'ensemble du site :

| Ancien terme | Terme retenu | Pourquoi |
|---|---|---|
| « coaching business » | **accompagnement d'entreprise** | « Coaching » sonne anglo-saxon et flou pour un indépendant belge ; « accompagnement » est le mot courant du secteur. |
| « marketing digital » | **présence digitale** | Le contenu réel porte sur les réseaux sociaux, la fiche Google, les avis et le référencement — pas sur de l'achat média. |
| « pilotage financier » | **gestion administrative** | Aligne la baseline sur les trois volets réellement proposés. |

« Coaching commercial » est **conservé** : c'est le nom que le client donne lui-même à cette prestation, et il désigne une discipline précise.

Les noms de fichiers (`coaching-*.html`, `marketing-digital.html`) n'ont **pas** été renommés : changer une URL casse les liens existants et le référencement. À faire plus tard si besoin, avec des redirections dans `vercel.json`.

## Note technique

Le site reste **majoritairement statique** (HTML/CSS/JS vanilla, aucun build), mais inclut désormais un dossier `api/` de **fonctions serverless Vercel** (Node.js) pour tout ce qui touche aux clés API et aux emails côté serveur — jamais exposées au navigateur :
- `api/subscribe.js` — capture d'email pour les lead magnets (Brevo).
- `api/generate-report.js` — génération du rapport diagnostic payant (Claude + PDF via `pdfkit` + email).
- `api/contact.js` — formulaire de contact (email transactionnel Brevo, consentement + champ leurre anti-robots).
- `api/_brevo.js` — helper partagé.

`package.json` liste la seule dépendance (`pdfkit`) ; Vercel l'installe automatiquement au déploiement. En local, `npm install` puis un serveur de dev capable de servir `/api/*.js` (ex. `vercel dev`) sont nécessaires pour tester ces routes — le reste du site continue de fonctionner en pur statique (`file://` ou n'importe quel serveur de fichiers). Tous les liens internes ont été vérifiés (aucun lien cassé), et les deux flux serveur ont été testés en simulant leurs réponses API (succès et erreur) via Playwright.
