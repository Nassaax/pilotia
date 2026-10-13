// /api/donnees : lire et écrire le contenu de l'espace client
// (brand/espace-client-CONCEPTION.md, § 4.3 et 6).
//
//   GET                              { ok, elements: { cle: { valeur, version, maj } } }
//   PUT ?cle=… { valeur, version }   { ok, valeur, version, maj }
//
// « version » est celle sur laquelle s'appuie l'appareil (0 : rien encore).
// Si l'espace a changé depuis, l'écriture est refusée (409) avec la version
// actuelle, pour que l'appareil décide (conception, § 4.3). valeur null
// efface l'élément.

const { requete } = require("./_base");
const { ouvert, origineValide, estJson, corps, repondre, lireSession } = require("./_session");
const { CLES, valider } = require("./_elements");

function element(ligne) {
  return ligne ? { valeur: ligne.valeur, version: ligne.version, maj: new Date(ligne.maj).toISOString() } : null;
}

async function lire(compteId, cle) {
  return element((await requete(
    "select valeur, version, maj from elements where compte_id = $1 and cle = $2", [compteId, cle]))[0]);
}

async function ecrire(req, res, compteId) {
  const cle = (req.query || {}).cle;
  const c = corps(req);
  if (!CLES.includes(cle)) return repondre(res, 404, { ok: false, erreur: "Élément inconnu." });
  if (!c || !("valeur" in c) || !Number.isInteger(c.version) || c.version < 0) {
    return repondre(res, 400, { ok: false, erreur: "Demande invalide." });
  }
  if (c.valeur === null) {
    const efface = await requete(
      "delete from elements where compte_id = $1 and cle = $2 and version = $3 returning cle", [compteId, cle, c.version]);
    const actuel = efface.length ? null : await lire(compteId, cle);
    if (actuel) return repondre(res, 409, { ok: false, conflit: true, actuel });
    return repondre(res, 200, { ok: true, valeur: null, version: 0, maj: null });
  }
  const v = valider(cle, c.valeur);
  if (v.erreur) return repondre(res, v.statut, { ok: false, erreur: v.erreur });
  const texte = JSON.stringify(v.valeur);
  const lignes = c.version === 0
    ? await requete(
      `insert into elements (compte_id, cle, valeur, version) values ($1, $2, $3, 1)
       on conflict do nothing returning version, maj`, [compteId, cle, texte])
    : await requete(
      `update elements set valeur = $3, version = version + 1, maj = now()
        where compte_id = $1 and cle = $2 and version = $4 returning version, maj`, [compteId, cle, texte, c.version]);
  if (!lignes.length) return repondre(res, 409, { ok: false, conflit: true, actuel: await lire(compteId, cle) });
  repondre(res, 200, { ok: true, valeur: v.valeur, version: lignes[0].version, maj: new Date(lignes[0].maj).toISOString() });
}

module.exports = async (req, res) => {
  if (!ouvert()) return repondre(res, 404, { ok: false, erreur: "L'espace client n'est pas ouvert." });
  if (req.method !== "GET" && req.method !== "PUT") return repondre(res, 405, { ok: false, erreur: "Méthode non autorisée." });
  if (req.method === "PUT" && (!origineValide(req) || !estJson(req))) {
    return repondre(res, 403, { ok: false, erreur: "Demande refusée." });
  }
  try {
    const session = await lireSession(req, res);
    if (!session.compte) return repondre(res, 401, { ok: false, raison: session.raison, erreur: "Connexion requise." });
    if (req.method === "PUT") return await ecrire(req, res, session.compte.id);
    const elements = {};
    for (const l of await requete(
      "select cle, valeur, version, maj from elements where compte_id = $1", [session.compte.id])) {
      elements[l.cle] = element(l);
    }
    repondre(res, 200, { ok: true, elements });
  } catch (erreur) {
    console.error("donnees", req.method, erreur.code || erreur.name || "erreur");
    if (!res.headersSent) repondre(res, 500, { ok: false, erreur: "Une erreur est survenue. Réessayez dans un instant." });
  }
};
