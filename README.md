# Pilotis — coaching business, marketing digital et pilotage financier

Site vitrine pour un service de coaching destiné aux petites entreprises belges (restaurants, entreprises du bâtiment, commerces...) et aux futurs indépendants. Positionnement : premium, épuré, orienté confiance ("pilotis" = les fondations qui portent une construction).

Ce dépôt contient une **structure complète de site** (27 pages, contenu réel, 8 outils interactifs, direction visuelle provisoire) à valider avant d'investir dans le design final.

Le marketing digital / réseaux sociaux est un **pilier à part entière** de l'offre, pas un simple ajout : page dédiée (`marketing-digital.html`), outil interactif (`generateur-calendrier-contenu.html`), formules tarifaires propres (`offres.html`), et présence dans le diagnostic express, le hub d'outils et les 2 parcours (entreprises et indépendants).

## Décisions déjà prises

- **Nom de marque :** Pilotis
- **Marché cible :** Belgique (législation, fiscalité et cotisations sociales belges)
- **Deux parcours, à égalité :**
  - Entreprises déjà en activité (`entreprises.html`) — diagnostic, gestion du personnel, marges, marketing digital
  - Futurs indépendants (`independants.html`) — statut, prévisionnel financier, documents de lancement
- **Modèle économique :** freemium — ressources/documents/outils gratuits en haut de tunnel, coaching payant (diagnostic ponctuel ou suivi mensuel) en conversion.

## Arborescence du site (27 pages)

```
Cœur du site
  index.html            Accueil — aiguillage vers les 2 parcours, témoignages, 3 leviers
  entreprises.html       Parcours PME existantes
  independants.html      Parcours futurs indépendants
  marketing-digital.html  Pilier marketing digital & réseaux sociaux (diagnostic, offre, FAQ)
  methode.html            Méthode en 4 étapes (écouter / diagnostiquer / décider / piloter)
  offres.html              Tarifs et formules (grille indicative chiffrée, incl. marketing digital)
  ressources.html          Bibliothèque de documents gratuits (lead magnets)
  outils.html               Hub des 8 outils interactifs
  a-propos.html              Positionnement, conviction, valeurs, bio (template à personnaliser)
  statistiques.html           Chiffres clés PME/indépendants Belgique (sourcés)
  contact.html                  Prise de rendez-vous + formulaire

Outils interactifs (JS vanilla, calculs côté client, barèmes 2026)
  diagnostic.html                          Diagnostic express noté sur 8 questions / 4 thèmes
  calculateur-cotisations-independant.html   Barème INASTI 2026
  calculateur-tva-franchise.html             Seuil de franchise TVA (25 000 €, 2026)
  calculateur-marge.html                     Marge produit/prestation + seuil de rentabilité
  calculateur-cout-salarie.html              Coût réel annuel d'un salarié (charges patronales 2026)
  calculateur-tresorerie.html                Prévisionnel de trésorerie sur 12 mois (avec graphique)
  comparateur-statut.html                    Personne physique (IPP) vs société (ISOC)
  generateur-calendrier-contenu.html         Calendrier de contenu réseaux sociaux sur 4 semaines, par secteur

Contenu / SEO
  conseils.html                     Hub des articles
  conseils-marge-restaurant.html      Article — erreurs de marge en restauration
  conseils-chiffrer-chantier.html     Article — bien chiffrer un chantier
  conseils-lancer-independant.html    Article — checklist avant de se lancer

Légal & technique
  mentions-legales.html, confidentialite.html, cgv.html   Pages légales (squelettes à finaliser)
  404.html
  style.css              Direction visuelle provisoire (palette neutre + accent vert foncé/or)
  robots.txt, sitemap.xml, vercel.json   SEO et headers de sécurité (domaine placeholder à mettre à jour)
```

## Ce qui est réel vs. placeholder

**Réel et vérifié par recherche web (sources citées dans `statistiques.html` et dans les encarts "note" de chaque calculateur) :**
- Cotisations sociales indépendant 2026 (INASTI) : 20,5 % jusqu'à 75 024,54 €, 14,16 % jusqu'à 110 562,42 €, exonération au-delà ; cotisation trimestrielle min. 917,58 €, max. 5 258,69 €.
- Seuil de franchise TVA 2026 : 25 000 € de chiffre d'affaires annuel, sans tolérance de dépassement depuis 2025.
- Taux ISOC 2026 : 25 % normal, 20 % taux réduit PME sur la première tranche de 100 000 € de bénéfice (sous conditions, dont rémunération dirigeant ≥ 50 000 €/an).
- Cotisations patronales ONSS 2026 : ~25 % du brut (employés), ~30-35 % (ouvriers) ; réduction "premier engagement" 2 000 €/trimestre à partir d'avril 2026.
- Tranches IPP 2026 (25/40/45/50 %) et quotité exemptée — **estimation indexée**, chiffres officialisés en fin d'année seulement (utilisés dans `comparateur-statut.html`, disclaimer inclus).
- Statistiques PME/faillites Belgique (SPF Économie, Statbel, UCM, GraydonCreditsafe) — voir sources dans `statistiques.html`.

**Placeholder, à compléter avant mise en ligne :**
- Bio et crédibilité réelles du/des coach(s) (`a-propos.html` contient un template avec [placeholders] — ne pas publier avec des informations inventées)
- Témoignages clients (`index.html` contient 3 exemples explicitement marqués "exemple illustratif" — à remplacer par de vrais retours dès les premiers accompagnements)
- Documents téléchargeables eux-mêmes — PDF/Excel (`ressources.html` ne fait que lister les titres, les liens pointent vers `contact.html`)
- Grille tarifaire (`offres.html`) : chiffres indicatifs de démarrage (490 €, 390 €/mois, 390 € formule lancement) à valider selon votre positionnement réel
- Widget de prise de rendez-vous réel (Cal.com ou équivalent) et backend du formulaire de contact
- Mentions légales, CGV, politique de confidentialité — dénomination légale, numéro d'entreprise, hébergeur
- Logo et identité visuelle définitive (le CSS actuel est une direction provisoire, pas le design final)
- Domaine réel : `robots.txt`, `sitemap.xml` et les balises `og:url` utilisent `pilotis.vercel.app` en placeholder

## Prochaines étapes suggérées

1. Valider le concept et le contenu de cette structure.
2. Personnaliser `a-propos.html` avec un vrai parcours et une vraie photo.
3. Créer la structure juridique (statut, numéro d'entreprise) pour pouvoir remplir les pages légales.
4. Produire les documents téléchargeables réels du kit de lancement et du kit pilotage PME.
5. Passer à un design final une fois le concept validé (actuellement volontairement sobre pour ne pas trancher trop tôt sur l'identité visuelle).
6. Brancher formulaire de contact + prise de rendez-vous + capture d'email sur de vrais outils.
7. Faire vérifier tous les chiffres légaux (INASTI, TVA, ISOC, IPP, ONSS) par un comptable avant toute communication commerciale — ce sont des estimations pédagogiques, pas des avis fiscaux.

## Note technique

Site 100 % statique (HTML/CSS/JS vanilla), sans dépendance ni build — même approche que le site sœur `educateur-financier`. Déployable tel quel sur Vercel/Netlify/GitHub Pages. Tous les liens internes ont été vérifiés (aucun lien cassé).
