// Accès à la base de l'espace client (brand/espace-client-CONCEPTION.md, § 4.2).
//
// En production : le pilote Neon (requêtes HTTP) sur DATABASE_URL, variable
// posée par l'intégration Neon de Vercel, jamais écrite dans le code. Dans les
// tests : la base en mémoire que tests/espace-client/serveur.js branche avec
// utiliser(). Les tables s'installent toutes seules au premier appel de chaque
// démarrage : il n'y a aucune commande à lancer à la main.
//
// Toutes les requêtes sont paramétrées ($1, $2…) : aucune valeur venue du
// navigateur n'est jamais collée dans le texte d'une requête.

const SCHEMA = [
  `create table if not exists comptes (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    cree_le timestamptz not null default now(),
    vu_le timestamptz not null default now(),
    averti_le timestamptz,
    conditions_version text not null,
    conditions_le timestamptz not null default now()
  )`,
  `create table if not exists sessions (
    jeton_empreinte text primary key,
    compte_id uuid not null references comptes(id) on delete cascade,
    cree_le timestamptz not null default now(),
    expire_le timestamptz not null,
    renouvele_le timestamptz not null default now(),
    revoquee_le timestamptz
  )`,
  "create index if not exists sessions_compte on sessions (compte_id)",
  `create table if not exists codes (
    email_empreinte text primary key,
    code_empreinte text not null,
    expire_le timestamptz not null,
    essais integer not null default 0,
    envoye_le timestamptz not null default now(),
    verifie_le timestamptz
  )`,
  `create table if not exists elements (
    compte_id uuid not null references comptes(id) on delete cascade,
    cle text not null check (cle in ('fiche', 'diagnostic', 'plan', 'calculs')),
    valeur jsonb not null,
    version integer not null,
    maj timestamptz not null default now(),
    primary key (compte_id, cle)
  )`,
  `create table if not exists limites (
    cle text not null,
    fenetre timestamptz not null,
    nombre integer not null default 0,
    primary key (cle, fenetre)
  )`,
  "create table if not exists schema_version (version integer not null)",
  "insert into schema_version (version) select 1 where not exists (select 1 from schema_version)",
];

let executer = null;
let installation = null;

// Remplace le pilote Neon (tests) : fonction (texte, valeurs) -> lignes.
function utiliser(fonction) {
  executer = fonction;
  installation = null;
}

function disponible() {
  return Boolean(executer || process.env.DATABASE_URL);
}

function connecteur() {
  if (!executer) {
    if (!process.env.DATABASE_URL) {
      throw new Error("DATABASE_URL manquante : relier la base Neon au projet Vercel, voir api/_base.js.");
    }
    const { neon } = require("@neondatabase/serverless");
    const sql = neon(process.env.DATABASE_URL);
    executer = (texte, valeurs) => sql.query(texte, valeurs);
  }
  return executer;
}

async function installer(ex) {
  for (const instruction of SCHEMA) {
    try {
      await ex(instruction, []);
    } catch (erreur) {
      // Deux démarrages simultanés peuvent créer la même table au même instant.
      if (erreur.code !== "42P07" && erreur.code !== "23505") throw erreur;
    }
  }
}

async function requete(texte, valeurs) {
  const ex = connecteur();
  if (!installation) {
    installation = installer(ex).catch((erreur) => {
      installation = null;
      throw erreur;
    });
  }
  await installation;
  return ex(texte, valeurs || []);
}

module.exports = { requete, utiliser, disponible };
