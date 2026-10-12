# Charte de l'app Pilotia

Référence à reproduire à l'identique dans la future app (iOS, Android ou
web) pour que les clients retrouvent les mêmes repères que sur le site en
mode app. Conception complète : `format-app-CONCEPTION.md`. En cas d'écart,
le site fait foi et cette fiche se corrige.

## Onglets (ordre et libellés fixes)

| # | Libellé | Destination sur le site | Icône |
|---|---|---|---|
| 1 | Accueil | `index.html` | maison |
| 2 | Services | `services.html` | mallette |
| 3 | Rendez-vous | `contact.html` | calendrier avec un plus (bouton central) |
| 4 | Outils | `outils.html` (sous-onglets Outils, Conseils, Guides) | calculatrice |
| 5 | Mon espace | `mon-espace.html` | silhouette |

- Le libellé est toujours écrit sous l'icône ; jamais d'icône seule.
- Onglet actif : couleur d'accent `#0369A1` (sombre : `#4CA9E0`) et pastille
  `#E1EEF6` (sombre : `#16283D`) derrière l'icône. La barre garde ces
  couleurs de marque sur toutes les pages, y compris celles d'un service.
- Bouton central : rond de 60 px, fond d'accent, contour de 2 px et ombre
  décalée de 3 px en marine `#0F172A` (sombre : noir), surélevé de 24 px.
  Cerclé quand on est sur Rendez-vous.
- La barre se masque pendant la saisie au clavier.

## Correspondance des pages et des onglets

| Onglet | Page principale | Pages de détail (lien retour) |
|---|---|---|
| Accueil | `index.html` | aucune |
| Services | `services.html` | `entreprises`, `independants`, `facturation-electronique`, `affacturage`, `marketing-digital`, `offres`, les 5 pages `coaching-*` (« ‹ Services ») |
| Rendez-vous | `contact.html` | aucune |
| Outils | `outils.html`, `conseils.html`, `ressources.html` | `diagnostic`, `rapport-diagnostic`, les 6 `calculateur-*`, `plan-tresorerie`, `generateur-calendrier-contenu` (« ‹ Outils ») ; les 7 articles `conseils-*` (« ‹ Conseils ») |
| Mon espace | `mon-espace.html` | aucune |
| Aucun (menu « Plus ») | | `a-propos`, `methode`, `statistiques`, `parrainage`, `mentions-legales`, `confidentialite`, `cookies`, `cgv`, `accessibilite`, `404` |

## Icônes (grille de 24, trait de 2, extrémités arrondies)

```
Accueil      <path d="M3.5 10.5 12 3.5l8.5 7V20a1 1 0 0 1-1 1h-4.5v-6h-6v6H4.5a1 1 0 0 1-1-1z"/>
Services     <rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8.5 7V5.5a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2V7M3 12.5h18"/>
Rendez-vous  <rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17M12 12.5v5M9.5 15h5"/>
Outils       <rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7h7M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01M8.5 15h.01M12 15h.01M15.5 15h.01M8.5 18h.01M12 18h.01M15.5 18h.01"/>
Mon espace   <circle cx="12" cy="8.5" r="4"/><path d="M4.5 20.5c.8-3.6 3.9-6 7.5-6s6.7 2.4 7.5 6"/>
Retour       <path d="M15 5l-7 7 7 7"/>
```

## Couleurs et typographie

- Marque : marine `#0F172A`, accent `#0369A1`, fond `#F8FAFC`, cartes `#FFFFFF`.
  Mode sombre : fond `#0B1220`, cartes `#16223A`, accent `#4CA9E0`.
- Chaque service garde sa couleur (`style.css`, classes `.svc-*`) : Peppol
  `#1D4ED8`, mauvais payeurs `#C2410C`, affacturage `#157A3B`, diagnostic
  `#6D28D9`, présence digitale `#BE185D`, indépendants `#AD4F0A`, pilotage
  `#4338CA`, outils `#0F766E`.
- Police : Inter (titres en graisse 600 à 700, interlettrage resserré).
- Zones à toucher : 48 × 48 px au moins. Contraste du texte : 4,5:1 au moins.

## Comportements

- **Retour :** sur une page de détail, « ‹ Services », « ‹ Outils » ou
  « ‹ Conseils » ramène toujours à la page principale de l'onglet, jamais à
  l'historique.
- **Menu « Plus » (☰) :** panneau qui monte du bas ; Pilotia (À propos, Notre
  méthode, Statistiques, Parrainage, Instagram) et Informations (Mentions
  légales, Confidentialité, Cookies, Conditions générales, Accessibilité).
- **Pages longues :** encadré « L'essentiel » (trois points au plus, tirés de
  la page), puis sections repliables avec « Tout ouvrir ».
- **Calculateurs :** clavier en chiffres, résultat mis en valeur, l'écran
  descend jusqu'à lui.

## Mon espace, aujourd'hui et demain

- **Aujourd'hui :** les résultats enregistrés sur l'appareil (dernier
  diagnostic, point bas du plan de trésorerie), un « prochain pas » et un
  bouton d'effacement. Aucun compte.
- **Demain :** la connexion de l'espace client s'ajoute sur cet écran, au
  même endroit et sous le même onglet.
