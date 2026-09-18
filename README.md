# Pilotia — coaching business, marketing digital et aide simple aux indépendants

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
  - Entreprises déjà en activité (`entreprises.html`) — diagnostic simple, gestion du personnel, marges, marketing digital
  - Futurs indépendants (`independants.html`) — démarches, repères financiers simples, documents de lancement
- **Modèle économique :** freemium — ressources/documents/outils gratuits en haut de tunnel, coaching payant (diagnostic ponctuel ou suivi mensuel) en conversion, plus deux automatisations de revenu/capture ajoutées ci-dessous.

## Arborescence du site (25 pages)

```
Cœur du site
  index.html            Accueil — aiguillage vers les 2 parcours, témoignages, 3 leviers
  entreprises.html       Parcours PME existantes
  independants.html      Parcours futurs indépendants
  marketing-digital.html  Pilier marketing digital & réseaux sociaux (diagnostic, offre, FAQ)
  methode.html            Méthode en 4 étapes (écouter / diagnostiquer / décider / piloter)
  offres.html              Tarifs et formules (grille indicative chiffrée, incl. marketing digital)
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

**Placeholder, à compléter avant mise en ligne :**
- Photo du fondateur sur `a-propos.html` (le champ a été retiré en attendant une vraie photo professionnelle — à réintégrer quand elle sera disponible)
- La plupart des documents téléchargeables listés sur `ressources.html` restent à produire — seul "Les étapes pour devenir indépendant" existe (et est maintenant derrière la capture d'email, voir plus haut)
- Grille tarifaire (`offres.html`) : chiffres indicatifs de démarrage (490 €, 390 €/mois, 390 € formule lancement) à valider selon votre positionnement réel
- Backend du formulaire de contact libre (envoi d'email) — le lien Cal.com est déjà branché, seul ce formulaire reste à connecter
- **`BREVO_API_KEY` et `ANTHROPIC_API_KEY`** — variables d'environnement à créer dans Vercel pour activer la capture d'email et le rapport IA (voir `.env.example`). Sans elles, ces fonctionnalités répondent une erreur claire plutôt que de planter silencieusement.
- **Paiement du rapport diagnostic (19 €)** — le flux technique est prêt (formulaire → IA → PDF → email) mais le paiement Stripe n'est pas branché ; le rapport est actuellement généré gratuitement, avec une mention "version test" visible sur la page.
- Mentions légales, CGV, politique de confidentialité — dénomination légale, numéro d'entreprise, hébergeur
- Domaine réel : `robots.txt`, `sitemap.xml` et les balises `og:url`/`og:image` utilisent `pilotis-nassaaxs-projects.vercel.app` en placeholder — à mettre à jour une fois `pilotia.be` (ou équivalent) actif

## Prochaines étapes suggérées

1. **Créer les comptes Brevo et Anthropic, ajouter les clés dans Vercel** (voir `.env.example`) pour activer la capture d'email et le rapport IA — sans ça, ces deux fonctionnalités répondent une erreur claire aux visiteurs.
2. **Brancher Stripe** sur `api/generate-report.js` pour faire payer réellement les 19 € du rapport détaillé (le code est prêt à recevoir cette étape, voir le commentaire en tête du fichier).
3. Personnaliser `a-propos.html` avec un vrai parcours et une vraie photo (sans survendre de titre non détenu).
4. Créer la structure juridique (statut choisi avec un comptable) pour pouvoir remplir les pages légales.
5. Produire les documents téléchargeables réels du kit de lancement et du kit pilotage PME.
6. Passer à un design final une fois le concept validé.
7. Brancher le formulaire de contact libre (envoi d'email) — Cal.com et les deux automatisations ci-dessus sont déjà branchés.
8. Faire vérifier les chiffres légaux restants (INASTI, TVA, ONSS) par un professionnel avant toute communication commerciale — ce sont des estimations pédagogiques basées sur des barèmes publics, pas des avis fiscaux.
9. Faire relire le contenu généré par `api/generate-report.js` sur quelques cas réels avant de pousser le trafic dessus — c'est un prompt système qui encadre le ton et interdit le conseil fiscal/comptable, mais une relecture humaine reste utile au lancement.

## Note technique

Le site reste **majoritairement statique** (HTML/CSS/JS vanilla, aucun build), mais inclut désormais un dossier `api/` de **fonctions serverless Vercel** (Node.js) pour tout ce qui touche aux clés API et aux emails côté serveur — jamais exposées au navigateur :
- `api/subscribe.js` — capture d'email pour les lead magnets (Brevo).
- `api/generate-report.js` — génération du rapport diagnostic payant (Claude + PDF via `pdfkit` + email).
- `api/_brevo.js` — helper partagé.

`package.json` liste la seule dépendance (`pdfkit`) ; Vercel l'installe automatiquement au déploiement. En local, `npm install` puis un serveur de dev capable de servir `/api/*.js` (ex. `vercel dev`) sont nécessaires pour tester ces routes — le reste du site continue de fonctionner en pur statique (`file://` ou n'importe quel serveur de fichiers). Tous les liens internes ont été vérifiés (aucun lien cassé), et les deux flux serveur ont été testés en simulant leurs réponses API (succès et erreur) via Playwright.
