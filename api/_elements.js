// Validation du contenu de l'espace client (brand/espace-client-CONCEPTION.md,
// § 3.4, 3.5 et 4.3). Chaque élément doit avoir la forme attendue et une
// taille bornée ; la fiche est vérifiée champ par champ, par liste fermée ou
// par bornes. Rien d'autre n'entre dans la base.

const CLES = ["fiche", "diagnostic", "plan", "calculs"];
const TAILLES = { fiche: 2048, diagnostic: 32768, calculs: 32768, plan: 262144 };
const OUTILS = ["marge", "taux-horaire", "cotisations", "tva-franchise", "cout-salarie", "delai-encaissement"];

const estObjet = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
const estDate = (v) => typeof v === "string" && !Number.isNaN(Date.parse(v));
const VIDE = Symbol("vide");
const INVALIDE = Symbol("invalide");

// Chaque règle rend la valeur nettoyée, VIDE (champ omis) ou INVALIDE.
const texte = (max) => (v) => {
  if (v === null || v === undefined) return VIDE;
  if (typeof v !== "string") return INVALIDE;
  const t = v.trim();
  if (!t) return VIDE;
  return t.length <= max ? t : INVALIDE;
};
const liste = (valeurs) => (v) => {
  if (v === null || v === undefined || v === "") return VIDE;
  return valeurs.includes(v) ? v : INVALIDE;
};
const entier = (max) => (v) => {
  if (v === null || v === undefined) return VIDE;
  return Number.isInteger(v) && v >= 0 && v <= max ? v : INVALIDE;
};

const FICHE = {
  prenom: texte(60),
  entreprise: texte(120),
  secteur: liste(["restaurant", "boulangerie", "coiffure", "esthetique", "immobilier",
    "batiment", "commerce", "services", "autre"]),
  statut: liste(["principal", "complementaire", "societe", "projet"]),
  tva: liste(["assujetti", "franchise", "inconnu"]),
  chiffreAffaires: entier(1000000000),
  fraisFixes: entier(100000000),
  salaries: entier(10000),
};

const VERIFICATIONS = {
  fiche(v) {
    if (!estObjet(v)) return INVALIDE;
    const propre = {};
    for (const [champ, valeur] of Object.entries(v)) {
      if (!Object.prototype.hasOwnProperty.call(FICHE, champ)) return INVALIDE;
      const r = FICHE[champ](valeur);
      if (r === INVALIDE) return INVALIDE;
      if (r !== VIDE) propre[champ] = r;
    }
    return propre;
  },
  diagnostic(v) {
    const ok = estObjet(v) && typeof v.total === "number" && v.total >= 0 && v.total <= 16
      && estDate(v.date) && estObjet(v.themes);
    return ok ? v : INVALIDE;
  },
  plan(v) {
    const ok = estObjet(v) && estObjet(v.etat) && Array.isArray(v.etat.lignes)
      && (v.resume === null || v.resume === undefined || estObjet(v.resume));
    return ok ? { etat: v.etat, resume: v.resume || null } : INVALIDE;
  },
  calculs(v) {
    if (!estObjet(v)) return INVALIDE;
    for (const [outil, calcul] of Object.entries(v)) {
      const champs = estObjet(calcul) && estObjet(calcul.champs) ? Object.entries(calcul.champs) : null;
      const ok = OUTILS.includes(outil) && champs && champs.length <= 12
        && champs.every(([, c]) => (typeof c === "string" || typeof c === "number") && String(c).length <= 40)
        && typeof calcul.titre === "string" && calcul.titre.length <= 80
        && typeof calcul.resultat === "string" && calcul.resultat.length <= 200
        && estDate(calcul.maj);
      if (!ok) return INVALIDE;
    }
    return v;
  },
};

// { valeur } nettoyée, ou { statut, erreur } à renvoyer tel quel.
function valider(cle, valeur) {
  if (!CLES.includes(cle)) return { statut: 404, erreur: "Élément inconnu." };
  if (Buffer.byteLength(JSON.stringify(valeur)) > TAILLES[cle]) {
    return { statut: 413, erreur: "Trop volumineux pour être enregistré dans votre espace." };
  }
  const propre = VERIFICATIONS[cle](valeur);
  if (propre === INVALIDE) return { statut: 400, erreur: "Contenu invalide." };
  return { valeur: propre };
}

module.exports = { CLES, valider };
