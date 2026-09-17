# Pilotis — coaching business, marketing digital et aide simple aux indépendants

Site vitrine pour un service de coaching destiné aux petites entreprises belges (restaurants, entreprises du bâtiment, commerces...) et aux futurs indépendants. Positionnement : premium, épuré, orienté confiance ("pilotis" = les fondations qui portent une construction).

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

Une section **"Ce que Pilotis n'est pas"** a été ajoutée à `a-propos.html`, et les pages restantes ont été relues pour retirer tout vocabulaire d'"analyse financière approfondie" au profit de formulations simples ("comprendre ses chiffres", "repérer ce qui coûte cher"). Les outils de calcul conservés (cotisations INASTI, franchise TVA, marge, coût d'un salarié) appliquent des barèmes publics de façon mécanique — comme le font de nombreux simulateurs grand public — et rappellent chacun que ce n'est pas un conseil comptable ou fiscal personnalisé.

## Décisions déjà prises

- **Nom de marque :** Pilotis
- **Marché cible :** Belgique (législation, fiscalité et cotisations sociales belges — à titre informatif uniquement)
- **Deux parcours, à égalité :**
  - Entreprises déjà en activité (`entreprises.html`) — diagnostic simple, gestion du personnel, marges, marketing digital
  - Futurs indépendants (`independants.html`) — démarches, repères financiers simples, documents de lancement
- **Modèle économique :** freemium — ressources/documents/outils gratuits en haut de tunnel, coaching payant (diagnostic ponctuel ou suivi mensuel) en conversion.

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
  a-propos.html              Positionnement, valeurs, bio (template), section "ce que Pilotis n'est pas"
  statistiques.html           Chiffres clés PME/indépendants Belgique (sourcés)
  contact.html                  Prise de rendez-vous + formulaire

Outils interactifs (JS vanilla, calculs côté client, barèmes publics 2026)
  diagnostic.html                          Diagnostic express noté sur 8 questions / 4 thèmes
  calculateur-cotisations-independant.html   Barème INASTI 2026 — estimation simple
  calculateur-tva-franchise.html             Seuil de franchise TVA (25 000 €, 2026) — information générale
  calculateur-marge.html                     Marge produit/prestation + seuil de rentabilité
  calculateur-cout-salarie.html              Coût réel annuel d'un salarié (charges patronales 2026)
  generateur-calendrier-contenu.html         Calendrier de contenu réseaux sociaux sur 4 semaines, par secteur

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

**Placeholder, à compléter avant mise en ligne :**
- Bio et crédibilité réelles du/des coach(s) (`a-propos.html` contient un template avec [placeholders] — ne pas publier avec des informations inventées, et surtout ne jamais laisser entendre un titre de comptable agréé qui n'est pas détenu)
- Témoignages clients (`index.html` contient 3 exemples explicitement marqués "exemple illustratif" — à remplacer par de vrais retours dès les premiers accompagnements)
- Documents téléchargeables eux-mêmes — PDF/Excel (`ressources.html` ne fait que lister les titres, les liens pointent vers `contact.html`)
- Grille tarifaire (`offres.html`) : chiffres indicatifs de démarrage (490 €, 390 €/mois, 390 € formule lancement) à valider selon votre positionnement réel
- Widget de prise de rendez-vous réel (Cal.com ou équivalent) et backend du formulaire de contact
- Mentions légales, CGV, politique de confidentialité — dénomination légale, numéro d'entreprise, hébergeur
- Logo et identité visuelle définitive (le CSS actuel est une direction provisoire, pas le design final)
- Domaine réel : `robots.txt`, `sitemap.xml` et les balises `og:url` utilisent `pilotis.vercel.app` en placeholder

## Prochaines étapes suggérées

1. Valider le concept et le contenu de cette structure.
2. Personnaliser `a-propos.html` avec un vrai parcours et une vraie photo (sans survendre de titre non détenu).
3. Créer la structure juridique (statut choisi avec un comptable) pour pouvoir remplir les pages légales.
4. Produire les documents téléchargeables réels du kit de lancement et du kit pilotage PME.
5. Passer à un design final une fois le concept validé.
6. Brancher formulaire de contact + prise de rendez-vous + capture d'email sur de vrais outils.
7. Faire vérifier les chiffres légaux restants (INASTI, TVA, ONSS) par un professionnel avant toute communication commerciale — ce sont des estimations pédagogiques basées sur des barèmes publics, pas des avis fiscaux.

## Note technique

Site 100 % statique (HTML/CSS/JS vanilla), sans dépendance ni build — même approche que le site sœur `educateur-financier`. Déployable tel quel sur Vercel/Netlify/GitHub Pages. Tous les liens internes ont été vérifiés (aucun lien cassé).
