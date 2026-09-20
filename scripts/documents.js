// Contenu des documents téléchargeables.
//
//   node scripts/documents.js
//
// La mise en page vit dans generer-pdf.js ; ce fichier ne contient que le texte,
// pour qu'une correction de contenu ne demande jamais de toucher au rendu.

const fs = require("fs");
const path = require("path");
const L = require("./generer-pdf");
const { doc, titreSection, para, puces, cases, encadre, tableau, ecrire, CHIFFRES, SORTIE } = L;

// ─────────────────────────────────── 1. Checklist des charges à prévoir (libre)
async function checklistCharges() {
  const d = doc("Checklist des charges à prévoir",
    "Ce qu'un indépendant belge met de côté chaque trimestre");

  para(d, "La première année d'activité surprend rarement par le chiffre d'affaires : elle surprend par ce qu'il faut en retirer. Cette fiche liste les postes à provisionner, dans l'ordre où ils tombent.");

  titreSection(d, "À provisionner chaque trimestre");
  cases(d, [
    `Cotisations sociales — appelées trimestriellement par votre caisse d'assurances sociales. Barème 2026 : ${CHIFFRES.tauxBas} du revenu net imposable jusqu'à ${CHIFFRES.seuilBas}, puis ${CHIFFRES.tauxHaut} jusqu'à ${CHIFFRES.seuilHaut}. Cotisation minimale à titre principal : ${CHIFFRES.minTrimestre} par trimestre.`,
    `TVA — si vous y êtes assujetti. En dessous de ${CHIFFRES.franchiseTVA} de chiffre d'affaires annuel, le régime de franchise permet de ne pas la facturer, mais vous ne la récupérez pas non plus sur vos achats.`,
    "Impôt des personnes physiques — aucun précompte n'est retenu à la source pour un indépendant. Sans versements anticipés, la note arrive en une fois, majorée.",
    "Assurances professionnelles — responsabilité civile, et selon le métier : décennale, protection juridique, assurance du matériel ou du véhicule.",
    "Pension libre complémentaire (PLCI) — facultative, mais déductible et souvent la seule pension complémentaire d'un indépendant.",
  ]);

  titreSection(d, "La règle des trois enveloppes");
  para(d, "Le moyen le plus simple de ne jamais être pris de court : à chaque encaissement, répartir immédiatement plutôt que de piocher dans un compte unique.");
  tableau(d,
    ["Enveloppe", "Part indicative", "À quoi elle sert"],
    [
      ["Charges sociales et fiscales", "25 à 35 % du net encaissé", "Cotisations, impôt, versements anticipés"],
      ["Fonctionnement", "selon activité", "Achats, loyer, assurances, véhicule, outils"],
      ["Vous", "le reste", "Votre rémunération, une fois les deux premières couvertes"],
    ],
    [160, 110, 213]);
  encadre(d, "Ces pourcentages sont un point de départ, pas une règle. Le bon taux dépend de vos revenus réels, de votre statut et de votre situation familiale. Faites-le valider une fois par votre comptable, puis appliquez-le mécaniquement.");

  titreSection(d, "Les deux oublis les plus fréquents");
  puces(d, [
    `La régularisation des premières années. Un débutant cotise d'abord sur une base provisoire, puis l'administration régularise deux à trois ans plus tard sur les revenus réels. Si l'activité a bien démarré, le rattrapage peut représenter plusieurs milliers d'euros — pour une année déjà dépensée.`,
    `Le dépassement du seuil de franchise TVA. Franchir ${CHIFFRES.franchiseTVA} en cours d'année fait basculer dans le régime normal : il faut alors facturer la TVA, la déclarer et la reverser. Mieux vaut le voir venir que le découvrir.`,
  ]);

  await ecrire(d, "pilotia-checklist-charges-a-prevoir.pdf");
}

// ─────────────────────────── 2. Checklist visibilité digitale locale (libre)
async function checklistVisibilite() {
  const d = doc("Checklist visibilité locale",
    "Les bases à mettre en place pour être trouvé, sans budget publicitaire");

  para(d, "Être visible localement ne demande pas d'acheter de la publicité. Cela demande d'occuper correctement les endroits où vos clients cherchent déjà. Voici l'ordre dans lequel s'y prendre : chaque étape rend la suivante plus efficace.");

  titreSection(d, "Étape 1 — La fiche d'établissement Google");
  para(d, "C'est le point de départ, et de loin le meilleur rapport effort/résultat. Une fiche complète apparaît dans la recherche locale et dans Maps, gratuitement.");
  cases(d, [
    "Fiche revendiquée et vérifiée (Google Business Profile)",
    "Nom, adresse et numéro de téléphone strictement identiques partout ailleurs sur le web",
    "Catégorie principale précise, et catégories secondaires pertinentes",
    "Horaires à jour, y compris les jours de fermeture exceptionnelle",
    "Au moins dix photos réelles : devanture, intérieur, produits, équipe",
    "Description rédigée avec les mots que vos clients emploient, pas votre jargon métier",
    "Lien vers votre site ou, à défaut, vers votre page de contact",
  ]);

  titreSection(d, "Étape 2 — Les avis clients");
  para(d, "Le volume et la fraîcheur des avis pèsent autant que la note moyenne. Un établissement à 4,3 avec trente avis récents inspire plus confiance qu'un 5,0 avec quatre avis datant de deux ans.");
  cases(d, [
    "Une méthode simple et répétable pour demander un avis (QR code en caisse, lien en bas de facture, message après prestation)",
    "Réponse à tous les avis, positifs comme négatifs, sous quelques jours",
    "Réponses aux avis négatifs rédigées à froid, factuelles, sans polémique",
    "Aucun achat d'avis, aucun faux avis : c'est une pratique commerciale déloyale sanctionnée",
  ]);

  titreSection(d, "Étape 3 — La cohérence des informations");
  para(d, "Les moteurs recoupent vos coordonnées d'un site à l'autre. Une adresse écrite de trois façons différentes affaiblit tout le reste.");
  cases(d, [
    "Même libellé exact partout : site, Google, Facebook, Instagram, annuaires, pages jaunes",
    "Un seul numéro de téléphone public",
    "Adresse écrite à l'identique (abréviations, numéro de boîte, code postal)",
  ]);

  titreSection(d, "Étape 4 — Le site, même minimal");
  cases(d, [
    "Une page qui dit clairement ce que vous faites, pour qui, et où",
    "Coordonnées visibles sans avoir à chercher",
    "Affichage correct sur téléphone — c'est là que se fait l'essentiel des recherches locales",
    "Chargement rapide : au-delà de trois secondes, une partie des visiteurs est déjà repartie",
    "Mentions légales conformes (article XII.6 du Code de droit économique)",
  ]);

  titreSection(d, "Étape 5 — Les réseaux sociaux, mais pas tous");
  para(d, "Mieux vaut un seul réseau tenu correctement que trois abandonnés. Choisissez celui où se trouvent vos clients, pas celui qui vous plaît.");
  cases(d, [
    "Un seul réseau principal choisi et assumé",
    "Un rythme tenable sur la durée — une publication par semaine vaut mieux que cinq puis plus rien",
    "Profil complet : secteur, zone desservie, moyen de contact",
    "Publications qui montrent le travail réel plutôt que des images génériques",
  ]);

  encadre(d, "Ordre de priorité si vous ne faites qu'une seule chose ce mois-ci : la fiche Google, puis les avis. Les deux ensemble produisent davantage qu'un budget publicitaire équivalent à plusieurs centaines d'euros par mois.");

  await ecrire(d, "pilotia-checklist-visibilite-locale.pdf");
}

// ───────────────────────────────── 3. Modèle de suivi mensuel simple (libre)
async function suiviMensuel() {
  const d = doc("Modèle de suivi mensuel",
    "Un repère visuel à tenir en dix minutes par mois");

  para(d, "Ce document n'est pas un outil comptable et ne remplace aucune obligation légale. C'est un repère de gestion : douze lignes qui montrent d'un coup d'œil si l'activité progresse, stagne ou se dégrade.");

  titreSection(d, "Comment s'en servir");
  puces(d, [
    "Remplir une ligne par mois, toujours au même moment — par exemple le premier lundi.",
    "Utiliser les montants hors TVA si vous y êtes assujetti, et les montants réellement encaissés sinon.",
    "Ne pas chercher la précision comptable : un ordre de grandeur juste vaut mieux qu'un chiffre exact obtenu trois mois trop tard.",
    "Comparer chaque mois au même mois de l'année précédente plutôt qu'au mois précédent : la saisonnalité fausse toute autre comparaison.",
  ]);

  titreSection(d, "Tableau à remplir");
  const mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
  tableau(d,
    ["Mois", "Chiffre d'affaires", "Achats et charges", "Reste", "Remarque"],
    mois.map((m) => [m, "", "", "", ""]),
    [70, 100, 100, 70, 143]);

  titreSection(d, "Les trois questions à se poser en le remplissant");
  puces(d, [
    "Le « reste » couvre-t-il ma rémunération ET mes provisions de charges ? Si non, le problème n'est pas la trésorerie mais la marge ou le prix.",
    "Quel poste d'achats a le plus bougé depuis trois mois, et pourquoi ?",
    "Y a-t-il un mois où tout s'est bien passé ? Qu'est-ce qui était différent ce mois-là ?",
  ]);

  encadre(d, "Un suivi tenu six mois de suite vaut infiniment plus qu'un tableau parfait abandonné au bout de trois semaines. Si dix minutes par mois vous semblent trop, réduisez les colonnes plutôt que d'arrêter.");

  await ecrire(d, "pilotia-modele-suivi-mensuel.pdf");
}

// ────────────────────────────── 4. Guide des statuts en Belgique (contre email)
async function guideStatuts() {
  const d = doc("Guide des statuts en Belgique",
    "Comprendre les options avant d'en discuter avec votre comptable");

  para(d, "Le choix du statut engage votre fiscalité, votre protection sociale et votre responsabilité personnelle pour des années. Ce guide sert à arriver informé chez votre comptable — pas à décider seul.");

  titreSection(d, "Première question : personne physique ou société ?");
  para(d, "C'est la bifurcation principale. Tout le reste en découle.");
  tableau(d,
    ["", "Personne physique", "Société (SRL le plus souvent)"],
    [
      ["Création", "Simple et peu coûteuse : guichet d'entreprises, inscription BCE", "Acte notarié, plan financier, capital de départ suffisant"],
      ["Responsabilité", "Illimitée — votre patrimoine personnel est engagé", "Limitée aux apports, sauf faute de gestion"],
      ["Imposition", "Impôt des personnes physiques, par tranches progressives", "Impôt des sociétés, puis imposition de ce que vous vous versez"],
      ["Comptabilité", "Simplifiée dans la plupart des cas", "Complète, avec comptes annuels à déposer"],
      ["Bascule fréquente", "En dessous d'un certain bénéfice", "Au-delà, quand l'écart d'imposition compense les frais"],
    ],
    [80, 200, 203]);
  encadre(d, "Le seuil de bascule ne se résume pas à un chiffre de chiffre d'affaires : il dépend de votre bénéfice, de votre situation familiale, de ce que vous voulez vous verser et de votre besoin de protection patrimoniale. C'est exactement la question à poser à un comptable agréé.");

  titreSection(d, "Deuxième question : à titre principal, complémentaire ou étudiant ?");
  puces(d, [
    "À titre principal — votre activité indépendante est votre occupation principale. Cotisations sociales pleines, avec un minimum trimestriel de " + CHIFFRES.minTrimestre + ". C'est ce statut qui ouvre les droits complets (pension, maladie, allocations familiales).",
    "À titre complémentaire — vous exercez par ailleurs une activité salariée d'au moins un mi-temps. Cotisations calculées sur les revenus réels, sans minimum « titre principal », mais droits sociaux ouverts par l'activité salariée.",
    "Étudiant-indépendant — statut spécifique sous conditions d'âge et d'inscription dans un établissement d'enseignement, avec un régime de cotisations allégé.",
    "Conjoint aidant — statut propre pour la personne qui assiste régulièrement un indépendant sans être elle-même titulaire de l'activité.",
  ]);

  titreSection(d, "Les démarches, dans l'ordre");
  cases(d, [
    "Vérifier les accès à la profession éventuellement requis pour votre activité (certaines professions restent réglementées, les règles varient selon la Région)",
    "Ouvrir un compte bancaire professionnel distinct — obligatoire pour les assujettis TVA, et de toute façon indispensable pour tenir ses comptes",
    "S'inscrire à la Banque-Carrefour des Entreprises via un guichet d'entreprises agréé, et obtenir son numéro d'entreprise",
    "S'affilier à une caisse d'assurances sociales pour indépendants, au plus tard le jour du début d'activité",
    "S'affilier à une mutuelle en qualité d'indépendant",
    "Activer le numéro de TVA, ou demander expressément le régime de franchise si le chiffre d'affaires attendu reste sous " + CHIFFRES.franchiseTVA,
    "Souscrire les assurances professionnelles correspondant au métier",
    "Mettre en place la comptabilité, seul ou avec un comptable, dès le premier euro",
  ]);

  titreSection(d, "Le régime de franchise de TVA, en clair");
  para(d, `Sous ${CHIFFRES.franchiseTVA} de chiffre d'affaires annuel, vous pouvez demander à ne pas facturer la TVA. Vos factures portent alors la mention « Régime particulier de franchise des petites entreprises — TVA non applicable, article 56bis du Code de la TVA ».`);
  puces(d, [
    "Avantage : des prix plus légers pour une clientèle de particuliers, et une administration nettement allégée.",
    "Inconvénient : vous ne récupérez aucune TVA sur vos achats, investissements et matériel. Une activité qui achète beaucoup y perd.",
    "Vigilance : le seuil s'apprécie sur l'année civile. Le franchir en cours d'année fait basculer dans le régime normal.",
  ]);

  titreSection(d, "Ce que ce guide ne fait pas");
  para(d, "Il ne choisit pas à votre place, ne tient pas compte de votre situation familiale et patrimoniale, et n'intègre pas les aides régionales éventuellement disponibles. Le choix se valide avec un comptable agréé : une heure de consultation coûte moins cher qu'une année sous un statut inadapté.");

  await ecrire(d, "pilotia-guide-statuts-belgique.pdf");
}

// ───────────────── 5. Plan de présence digitale des 4 premières semaines (email)
async function planPresence() {
  const d = doc("Plan de présence digitale",
    "Quatre semaines pour poser des bases solides, sans budget publicitaire");

  para(d, "Ce plan part d'un principe : la visibilité gratuite se construit avant d'envisager la moindre publicité. Chaque semaine demande environ deux heures, découpables en sessions de vingt minutes.");

  titreSection(d, "Semaine 1 — Mettre de l'ordre avant de publier");
  para(d, "Publier sur des fondations bancales gaspille l'effort. Cette semaine ne produit rien de visible, et c'est la plus rentable.");
  cases(d, [
    "Revendiquer et compléter la fiche d'établissement Google",
    "Uniformiser nom, adresse et téléphone partout où ils apparaissent",
    "Rassembler dix à quinze photos réelles et exploitables",
    "Écrire en une phrase ce que vous faites, pour qui, et dans quelle zone",
    "Lister les cinq questions que vos clients posent systématiquement",
  ]);

  titreSection(d, "Semaine 2 — Choisir son terrain");
  para(d, "Un réseau tenu correctement bat trois réseaux à l'abandon. Le bon critère n'est pas votre préférence, mais la présence de vos clients.");
  cases(d, [
    "Choisir UN réseau principal et s'y tenir trois mois",
    "Compléter le profil : activité, zone, moyen de contact direct",
    "Repérer cinq concurrents ou confrères et noter ce qui fonctionne chez eux",
    "Définir un rythme tenable — une publication par semaine suffit pour commencer",
  ]);

  titreSection(d, "Semaine 3 — Produire de quoi tenir deux mois");
  para(d, "Les cinq questions notées en semaine 1 sont votre matière première : chacune fait une publication utile, et répond réellement à quelqu'un.");
  cases(d, [
    "Rédiger huit publications d'avance à partir des questions clients",
    "Alterner trois registres : le travail réalisé, la réponse à une question, la coulisse du métier",
    "Préparer les visuels correspondants (photo réelle plutôt qu'image de banque)",
    "Programmer les publications, ou bloquer un créneau fixe dans l'agenda",
  ]);

  titreSection(d, "Semaine 4 — Enclencher les avis et mesurer");
  cases(d, [
    "Mettre en place une demande d'avis systématique après chaque prestation",
    "Répondre à tous les avis existants, même anciens",
    "Noter trois chiffres de départ : nombre d'avis, note moyenne, appels reçus ce mois",
    "Fixer la date du prochain point, dans trois mois",
  ]);

  titreSection(d, "Pourquoi pas de publicité au départ");
  para(d, "Un budget publicitaire amplifie ce qui existe. Si la fiche est incomplète, les avis rares et le site lent, la publicité amène des visiteurs sur une vitrine mal rangée — et le budget part sans retour. Les quatre semaines ci-dessus rangent la vitrine. Après seulement, la question de la publicité devient légitime, et elle coûte alors moins cher pour un meilleur résultat.");

  encadre(d, "Un repère utile : trois mois après avoir mis ces bases en place, comparez vos trois chiffres de départ. Si les avis ont progressé et les appels avec, continuez sans rien payer. Sinon, c'est le positionnement qu'il faut revoir — pas le budget.");

  await ecrire(d, "pilotia-plan-presence-digitale.pdf");
}

// ────────────────── 6. Grille de diagnostic organisationnel (contre email)
async function grilleDiagnostic() {
  const d = doc("Grille de diagnostic organisationnel",
    "Vingt questions pour repérer où ça coince réellement");

  para(d, "Répondez par oui ou non, sans nuance et sans indulgence. Une réponse hésitante compte comme un non. Le total en fin de grille n'a d'intérêt que comparé à lui-même, six mois plus tard.");

  const bloc = (titre, intro, questions) => {
    titreSection(d, titre);
    if (intro) para(d, intro);
    cases(d, questions);
  };

  bloc("A. Vos chiffres", "Cinq questions sur ce que vous savez de votre activité.", [
    "Je connais ma marge sur mes trois produits ou prestations les plus vendus",
    "Je sais combien mon activité doit générer chaque mois pour couvrir toutes mes charges",
    "Je consulte un chiffre de gestion au moins une fois par mois",
    "Je sais quel client ou quel produit me rapporte le plus — et lequel me coûte",
    "Je peux dire à quoi ressemblera ma trésorerie dans trois mois",
  ]);

  bloc("B. Votre organisation", "Cinq questions sur le fonctionnement quotidien.", [
    "Les tâches récurrentes sont écrites quelque part, pas seulement dans ma tête",
    "L'entreprise peut tourner une semaine sans moi",
    "Je sais chaque semaine ce qui est prioritaire, sans y réfléchir longuement",
    "Les documents administratifs sont classés au fil de l'eau, pas en urgence",
    "Je ne refais pas deux fois la même recherche d'information",
  ]);

  bloc("C. Vos clients", "Cinq questions sur la relation commerciale.", [
    "Je sais d'où viennent mes clients actuels",
    "J'ai un moyen simple de recontacter d'anciens clients",
    "Mes prix ont été calculés, pas alignés sur ceux du voisin",
    "Je sais dire non à une demande qui ne rentre pas dans mon activité",
    "Je relance systématiquement les devis restés sans réponse",
  ]);

  bloc("D. Votre visibilité", "Cinq questions sur la manière dont on vous trouve.", [
    "On me trouve en cherchant mon métier et ma commune",
    "Ma fiche d'établissement est complète et à jour",
    "Je reçois des avis clients régulièrement, pas seulement par à-coups",
    "Quelqu'un qui ne me connaît pas comprend ce que je fais en dix secondes",
    "Je publie à un rythme régulier, même faible",
  ]);

  titreSection(d, "Lecture des résultats");
  tableau(d,
    ["Total de oui", "Ce que ça indique", "Par où commencer"],
    [
      ["16 à 20", "Base solide. Les gains restants sont des ajustements fins.", "Le bloc où il reste le plus de non"],
      ["11 à 15", "Ça tourne, mais des pertes passent inaperçues.", "Le bloc A si les chiffres manquent, sinon le bloc B"],
      ["6 à 10", "Plusieurs fondations manquent en même temps.", "Bloc A d'abord : sans chiffres, le reste se pilote à l'aveugle"],
      ["0 à 5", "L'activité repose entièrement sur votre présence quotidienne.", "Une seule chose à la fois, en commençant par la marge"],
    ],
    [80, 220, 183]);

  encadre(d, "Un score bas n'est pas un jugement : c'est la situation ordinaire d'une entreprise qui a grandi sans qu'on ait eu le temps de structurer. Ce qui compte, c'est l'écart entre deux passages de la grille.");

  await ecrire(d, "pilotia-grille-diagnostic-organisationnel.pdf");
}

// ─────────────────────── 7. Tableau de calcul de marge (CSV, ouvrable dans Excel)
function tableauMarge() {
  const lignes = [
    "Tableau de calcul de marge - Pilotia",
    "Renseignez les colonnes B a D. Les colonnes E a G se calculent seules.",
    "",
    "Produit ou prestation;Prix de vente HTVA;Cout direct (matiere/achat);Temps passe (min);Marge unitaire;Taux de marge;Marge par heure",
    "Exemple - plat du jour;18,00;6,50;12;=B5-C5;=SI(B5=0;\"\";E5/B5);=SI(D5=0;\"\";E5/D5*60)",
    ";;;;=B6-C6;=SI(B6=0;\"\";E6/B6);=SI(D6=0;\"\";E6/D6*60)",
    ";;;;=B7-C7;=SI(B7=0;\"\";E7/B7);=SI(D7=0;\"\";E7/D7*60)",
    ";;;;=B8-C8;=SI(B8=0;\"\";E8/B8);=SI(D8=0;\"\";E8/D8*60)",
    ";;;;=B9-C9;=SI(B9=0;\"\";E9/B9);=SI(D9=0;\"\";E9/D9*60)",
    ";;;;=B10-C10;=SI(B10=0;\"\";E10/B10);=SI(D10=0;\"\";E10/D10*60)",
    ";;;;=B11-C11;=SI(B11=0;\"\";E11/B11);=SI(D11=0;\"\";E11/D11*60)",
    ";;;;=B12-C12;=SI(B12=0;\"\";E12/B12);=SI(D12=0;\"\";E12/D12*60)",
    ";;;;=B13-C13;=SI(B13=0;\"\";E13/B13);=SI(D13=0;\"\";E13/D13*60)",
    ";;;;=B14-C14;=SI(B14=0;\"\";E14/B14);=SI(D14=0;\"\";E14/D14*60)",
    "",
    "Lecture :",
    "La marge par heure est souvent plus parlante que le taux de marge.",
    "Un produit a 70% de marge qui demande une heure de travail rapporte",
    "moins qu'un produit a 35% servi en dix minutes.",
    "",
    "Document pedagogique. Ne remplace pas une comptabilite analytique",
    "ni l'avis d'un comptable agree.",
  ];
  // Separateur point-virgule et encodage Windows-1252 : c'est ce qu'attend
  // Excel en configuration francophone, sinon tout atterrit dans une colonne.
  const contenu = "﻿" + lignes.join("\r\n") + "\r\n";
  const chemin = path.join(SORTIE, "pilotia-tableau-calcul-marge.csv");
  fs.writeFileSync(chemin, contenu, "utf8");
  const ko = (fs.statSync(chemin).size / 1024).toFixed(1);
  console.log(`  pilotia-tableau-calcul-marge.csv                 ${ko} Ko`);
}

(async () => {
  console.log("Génération des documents :");
  await checklistCharges();
  await checklistVisibilite();
  await suiviMensuel();
  await guideStatuts();
  await planPresence();
  await grilleDiagnostic();
  tableauMarge();
  console.log("Terminé.");
})();
