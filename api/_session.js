// Interrupteur, contrôle d'origine, cookie et session de l'espace client
// (brand/espace-client-CONCEPTION.md, § 5 et 7).
//
// Variables d'environnement (Vercel → Settings → Environment Variables) :
//   ESPACE_CLIENT   « ouvert » ouvre l'espace ; toute autre valeur le ferme.
//   COMPTES_SECRET  clé des empreintes HMAC (codes, adresses, réseaux) :
//                   32 octets aléatoires, différente en test et en production.

const crypto = require("crypto");
const { requete } = require("./_base");

const COOKIE = "__Host-pilotia-session";
const DUREE = 90 * 24 * 3600; // 90 jours, en secondes, prolongés à chaque visite

function ouvert() {
  return process.env.ESPACE_CLIENT === "ouvert";
}

// Une demande qui modifie quelque chose doit venir du site lui-même. Le http
// n'est admis que pour le serveur de test, sur la machine locale.
function origineValide(req) {
  const origine = req.headers.origin;
  const hote = req.headers.host;
  if (!origine || !hote) return false;
  if (origine === "https://" + hote) return true;
  return /^(127\.0\.0\.1|localhost)(:\d+)?$/.test(hote) && origine === "http://" + hote;
}

function estJson(req) {
  return (req.headers["content-type"] || "").startsWith("application/json");
}

// Le corps JSON de la demande, ou null s'il manque ou ne se lit pas.
function corps(req) {
  try {
    const c = req.body;
    return c && typeof c === "object" && !Array.isArray(c) ? c : null;
  } catch (erreur) {
    return null;
  }
}

function repondre(res, statut, objet) {
  res.setHeader("Cache-Control", "no-store");
  res.status(statut).json(objet);
}

function empreinte(texte) {
  return crypto.createHash("sha256").update(String(texte)).digest("hex");
}

function hmac(texte) {
  const cle = process.env.COMPTES_SECRET;
  if (!cle) throw new Error("COMPTES_SECRET manquante : voir api/_session.js.");
  return crypto.createHmac("sha256", cle).update(String(texte)).digest("hex");
}

// Identifiant court d'un espace, sans secret : il dit à un appareil si les
// données qu'il garde appartiennent à l'espace qui vient de se connecter.
function court(id) {
  return empreinte(id).slice(0, 16);
}

function lireJeton(req) {
  for (const morceau of (req.headers.cookie || "").split(";")) {
    const i = morceau.indexOf("=");
    if (i > 0 && morceau.slice(0, i).trim() === COOKIE) return morceau.slice(i + 1).trim() || null;
  }
  return null;
}

function poserCookie(res, jeton) {
  res.setHeader("Set-Cookie", `${COOKIE}=${jeton}; Path=/; Max-Age=${DUREE}; HttpOnly; Secure; SameSite=Strict`);
}

function effacerCookie(res) {
  res.setHeader("Set-Cookie", `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Strict`);
}

// La session de la demande : { compte: {id, email, court} } si elle est
// ouverte ; sinon { raison } : null sans cookie, « expiree » si elle a dépassé
// sa durée, « fermee » si elle a été fermée à distance ou n'existe plus.
// Une session ouverte est prolongée au plus une fois par jour.
async function lireSession(req, res) {
  const jeton = lireJeton(req);
  if (!jeton) return { raison: null };
  const lignes = await requete(
    `select s.compte_id, c.email, s.revoquee_le is not null as fermee,
            s.expire_le < now() as expiree, s.renouvele_le < now() - interval '1 day' as a_prolonger
       from sessions s join comptes c on c.id = s.compte_id
      where s.jeton_empreinte = $1`,
    [empreinte(jeton)]);
  const s = lignes[0];
  if (!s || s.fermee) return { raison: "fermee" };
  if (s.expiree) return { raison: "expiree" };
  if (s.a_prolonger) {
    await requete(
      "update sessions set expire_le = now() + interval '90 days', renouvele_le = now() where jeton_empreinte = $1",
      [empreinte(jeton)]);
    await requete("update comptes set vu_le = now(), averti_le = null where id = $1", [s.compte_id]);
    poserCookie(res, jeton);
  }
  return { compte: { id: s.compte_id, email: s.email, court: court(s.compte_id) } };
}

module.exports = {
  ouvert, origineValide, estJson, corps, repondre, empreinte, hmac, court,
  lireJeton, poserCookie, effacerCookie, lireSession,
};

// ─── Ouverture d'une session, après un code juste : un jeton aléatoire dans
// le cookie, et seulement son empreinte dans la base.
async function ouvrirSession(res, compteId) {
  const jeton = crypto.randomBytes(32).toString("base64url");
  await requete(
    "insert into sessions (jeton_empreinte, compte_id, expire_le) values ($1, $2, now() + interval '90 days')",
    [empreinte(jeton), compteId]);
  poserCookie(res, jeton);
}

module.exports.ouvrirSession = ouvrirSession;
