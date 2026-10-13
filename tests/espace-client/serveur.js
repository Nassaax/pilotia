/* Serveur des tests de l'espace client (brand/espace-client-CONCEPTION.md, § 9).
 *
 * Sert le site comme Vercel : les fichiers, les en-têtes de vercel.json et les
 * fonctions api/ avec les aides de Vercel (req.query, req.body, res.status,
 * res.json, res.send). Les fonctions tournent sur une vraie base PostgreSQL en
 * mémoire (PGlite) ; les envois vers Brevo sont interceptés, et tout autre
 * accès au réseau est refusé.
 *
 *   node tests/espace-client/serveur.js   écrit « PORT=… » puis sert
 *
 * Adresses réservées aux tests (le dossier tests n'est jamais publié) :
 *   GET  /__test/courriels  les emails interceptés
 *   POST /__test/sql        {texte, valeurs} : requête directe sur la base
 *   POST /__test/vider      vide la base, les emails et le journal
 *   POST /__test/env        {NOM: "valeur"} : change une variable d'environnement
 *   GET  /__test/journal    ce que les fonctions ont écrit dans la console
 */
"use strict";
const fs = require("fs");
const http = require("http");
const path = require("path");
const { PGlite } = require("@electric-sql/pglite");

const RACINE = path.resolve(__dirname, "..", "..");
const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".ico": "image/x-icon",
  ".woff2": "font/woff2", ".mp4": "video/mp4", ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8", ".pdf": "application/pdf", ".webmanifest": "application/manifest+json",
};

// Les fonctions lisent leur configuration ici, comme sur Vercel.
Object.assign(process.env, {
  ESPACE_CLIENT: "ouvert",
  COMPTES_SECRET: "cle-de-test-espace-client",
  CRON_SECRET: "secret-de-test-du-menage",
  BREVO_API_KEY: "cle-brevo-de-test",
  BREVO_SENDER_EMAIL: "contact@exemple.be",
});
delete process.env.DATABASE_URL;

const base = new PGlite();
const courriels = [];
const journal = [];
for (const nom of ["log", "info", "warn", "error"]) {
  console[nom] = (...morceaux) => { journal.push(morceaux.map(String).join(" ")); };
}

// Brevo est simulé ; TEST_BREVO_ECHEC=1 le fait échouer. Rien d'autre ne sort.
global.fetch = async (cible, options) => {
  if (String(cible).startsWith("https://api.brevo.com/")) {
    if (process.env.TEST_BREVO_ECHEC === "1") return new Response("{}", { status: 500 });
    courriels.push(JSON.parse(options.body));
    return new Response('{"messageId":"test"}', { status: 201 });
  }
  throw new Error("réseau coupé pendant les tests");
};

// Les fonctions de l'espace client prennent la base en mémoire à la place de Neon.
let baseBranchee = false;
function brancherBase() {
  const chemin = path.join(RACINE, "api", "_base.js");
  if (baseBranchee || !fs.existsSync(chemin)) return;
  require(chemin).utiliser(async (texte, valeurs) => (await base.query(texte, valeurs || [])).rows);
  baseBranchee = true;
}

const vercel = JSON.parse(fs.readFileSync(path.join(RACINE, "vercel.json"), "utf8"));
const entetes = (vercel.headers.find((r) => r.source === "/(.*)") || { headers: [] }).headers;

function lireCorps(req) {
  return new Promise((ok) => {
    const morceaux = [];
    req.on("data", (m) => morceaux.push(m));
    req.on("end", () => ok(Buffer.concat(morceaux)));
  });
}

// Les aides que Vercel ajoute aux fonctions Node.
function aides(req, res, corps) {
  const adresse = new URL(req.url, "http://local");
  req.query = Object.fromEntries(adresse.searchParams);
  let lu = false;
  let valeur;
  Object.defineProperty(req, "body", {
    get() {
      if (!lu) {
        lu = true;
        const type = req.headers["content-type"] || "";
        if (!corps.length) valeur = undefined;
        else if (type.startsWith("application/json")) {
          try { valeur = JSON.parse(corps.toString("utf8")); } catch (e) {
            const erreur = new Error("Invalid JSON");
            erreur.statusCode = 400;
            throw erreur;
          }
        } else valeur = corps.toString("utf8");
      }
      return valeur;
    },
  });
  res.status = (code) => { res.statusCode = code; return res; };
  res.json = (objet) => {
    if (!res.getHeader("Content-Type")) res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify(objet));
    return res;
  };
  res.send = (contenu) => {
    if (contenu !== null && typeof contenu === "object" && !Buffer.isBuffer(contenu)) return res.json(contenu);
    res.end(contenu);
    return res;
  };
}

function envoyerJson(res, statut, objet) {
  res.statusCode = statut;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.end(JSON.stringify(objet));
}

async function test(req, res, corps) {
  const adresse = new URL(req.url, "http://local").pathname;
  const donnees = corps.length ? JSON.parse(corps.toString("utf8")) : {};
  if (adresse === "/__test/courriels") return envoyerJson(res, 200, courriels);
  if (adresse === "/__test/journal") return envoyerJson(res, 200, journal);
  if (adresse === "/__test/sql") {
    brancherBase();
    // Les tables doivent exister même si aucune fonction n'a encore tourné.
    if (baseBranchee) await require(path.join(RACINE, "api", "_base.js")).requete("select 1");
    return envoyerJson(res, 200, (await base.query(donnees.texte, donnees.valeurs || [])).rows);
  }
  if (adresse === "/__test/env") {
    for (const [nom, val] of Object.entries(donnees)) {
      if (val === null) delete process.env[nom]; else process.env[nom] = String(val);
    }
    return envoyerJson(res, 200, { ok: true });
  }
  if (adresse === "/__test/vider") {
    const tables = (await base.query(
      "select tablename from pg_tables where schemaname = 'public' and tablename <> 'schema_version'")).rows;
    if (tables.length) await base.query("truncate " + tables.map((t) => t.tablename).join(", ") + " cascade");
    courriels.length = 0;
    journal.length = 0;
    return envoyerJson(res, 200, { ok: true });
  }
  return envoyerJson(res, 404, { erreur: "adresse de test inconnue" });
}

async function api(req, res, corps, nom) {
  const chemin = path.join(RACINE, "api", nom + ".js");
  if (!/^[a-z][a-z-]*$/.test(nom) || !fs.existsSync(chemin)) {
    return envoyerJson(res, 404, { ok: false, erreur: "fonction inconnue" });
  }
  brancherBase();
  aides(req, res, corps);
  try {
    await require(chemin)(req, res);
  } catch (erreur) {
    if (!res.headersSent) envoyerJson(res, erreur.statusCode || 500, { ok: false, erreur: String(erreur.message) });
  }
}

function fichier(req, res) {
  let chemin = decodeURIComponent(new URL(req.url, "http://local").pathname);
  if (chemin.endsWith("/")) chemin += "index.html";
  const complet = path.join(RACINE, path.normalize(chemin));
  if (!complet.startsWith(RACINE + path.sep) || !fs.existsSync(complet) || fs.statSync(complet).isDirectory()) {
    res.statusCode = 404;
    res.setHeader("Content-Type", TYPES[".html"]);
    return res.end(fs.readFileSync(path.join(RACINE, "404.html")));
  }
  res.statusCode = 200;
  res.setHeader("Content-Type", TYPES[path.extname(complet)] || "application/octet-stream");
  res.end(fs.readFileSync(complet));
}

const serveur = http.createServer(async (req, res) => {
  for (const { key, value } of entetes) res.setHeader(key, value);
  const corps = await lireCorps(req);
  const adresse = new URL(req.url, "http://local").pathname;
  try {
    if (adresse.startsWith("/__test/")) return await test(req, res, corps);
    const m = adresse.match(/^\/api\/([^/]+)$/);
    if (m) return await api(req, res, corps, m[1]);
    return fichier(req, res);
  } catch (erreur) {
    if (!res.headersSent) envoyerJson(res, 500, { erreur: String(erreur.message) });
  }
});

serveur.listen(0, "127.0.0.1", () => {
  process.stdout.write("PORT=" + serveur.address().port + "\n");
});
