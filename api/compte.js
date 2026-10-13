// /api/compte?action=… : connexion et compte de l'espace client
// (brand/espace-client-CONCEPTION.md, § 6, tableau « Adresses »).
//
// Chaque action est déclarée plus bas dans ACTIONS : sa méthode, si elle
// demande une session, et ce qu'elle fait. Interrupteur fermé, seule l'action
// « etat » répond (« pas ouvert ») ; toutes les autres répondent 404.

const crypto = require("crypto");
const { requete } = require("./_base");
const { isConfigured, isValidEmail, sendTransactionalEmail } = require("./_brevo");
const { depasse, ip } = require("./_limites");
const {
  ouvert, origineValide, estJson, corps, repondre, empreinte, hmac, court,
  lireJeton, effacerCookie, lireSession, ouvrirSession,
} = require("./_session");

const ACTIONS = {};

module.exports = async (req, res) => {
  const nom = (req.query || {}).action;
  if (!ouvert()) {
    if (nom === "etat") return repondre(res, 200, { ouvert: false });
    return repondre(res, 404, { ok: false, erreur: "L'espace client n'est pas ouvert." });
  }
  const action = Object.prototype.hasOwnProperty.call(ACTIONS, nom) ? ACTIONS[nom] : null;
  if (!action) return repondre(res, 404, { ok: false, erreur: "Action inconnue." });
  if (req.method !== action.methode) return repondre(res, 405, { ok: false, erreur: "Méthode non autorisée." });
  if (action.methode !== "GET" && (!origineValide(req) || !estJson(req))) {
    return repondre(res, 403, { ok: false, erreur: "Demande refusée." });
  }
  try {
    let compte = null;
    if (action.session) {
      const session = await lireSession(req, res);
      if (!session.compte) {
        return repondre(res, 401, { ok: false, raison: session.raison, erreur: "Connexion requise." });
      }
      compte = session.compte;
    }
    await action.faire(req, res, compte);
  } catch (erreur) {
    // Jamais d'adresse ni de contenu dans les journaux : l'action et le code d'erreur suffisent.
    console.error("compte", nom, erreur.code || erreur.name || "erreur");
    if (!res.headersSent) repondre(res, 500, { ok: false, erreur: "Une erreur est survenue. Réessayez dans un instant." });
  }
};

// ─── État de l'espace : ouvert ou non, connecté ou non (et pourquoi).
ACTIONS.etat = {
  methode: "GET",
  faire: async (req, res) => {
    const session = await lireSession(req, res);
    if (!session.compte) return repondre(res, 200, { ouvert: true, connecte: false, raison: session.raison });
    const c = session.compte;
    const fiche = await requete(
      "select valeur->>'prenom' as prenom from elements where compte_id = $1 and cle = 'fiche'", [c.id]);
    repondre(res, 200, {
      ouvert: true, connecte: true, compte: c.court, email: c.email,
      prenom: (fiche[0] && fiche[0].prenom) || null,
    });
  },
};

// ─── Codes de connexion (§ 3.2 et 5) : un code à 6 chiffres par email, valable
// 10 minutes, 5 essais. La réponse est la même qu'un espace existe ou non.

// Version des conditions d'utilisation acceptées à la création d'un espace :
// la date de conditions-espace.html, à changer avec le texte.
const CONDITIONS = "2026-10-13";

function adresse(valeur) {
  if (typeof valeur !== "string") return null;
  const email = valeur.trim().toLowerCase();
  return email.length <= 200 && isValidEmail(email) ? email : null;
}

function egales(a, b) {
  const x = Buffer.from(a, "hex");
  const y = Buffer.from(b, "hex");
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

function courrielDuCode(code) {
  const lisible = code.slice(0, 3) + " " + code.slice(3);
  return {
    subject: "Votre code Pilotia : " + lisible,
    htmlContent:
      "<p>Bonjour,</p>" +
      "<p>Voici votre code pour entrer dans votre espace Pilotia :</p>" +
      '<p style="font-size:28px;font-weight:700;letter-spacing:.08em">' + lisible + "</p>" +
      "<p>Il est valable 10 minutes et ne sert qu'une fois.</p>" +
      '<p style="color:#475569">Vous n\'avez rien demandé ? Ignorez cet email : sans ce code, ' +
      "personne ne peut entrer dans votre espace.</p>",
    textContent:
      "Bonjour,\n\nVoici votre code pour entrer dans votre espace Pilotia : " + lisible + "\n\n" +
      "Il est valable 10 minutes et ne sert qu'une fois.\n\n" +
      "Vous n'avez rien demandé ? Ignorez cet email : sans ce code, personne ne peut entrer " +
      "dans votre espace.\n",
  };
}

ACTIONS["demander-code"] = {
  methode: "POST",
  faire: async (req, res) => {
    const c = corps(req) || {};
    // Champ leurre : seul un robot le remplit. Réponse normale, rien n'est envoyé.
    if (typeof c.website === "string" && c.website.trim()) return repondre(res, 200, { ok: true });
    const email = adresse(c.email);
    if (!email) return repondre(res, 400, { ok: false, erreur: "Adresse email invalide." });
    if (!isConfigured()) {
      return repondre(res, 503, { ok: false, erreur: "L'envoi des codes n'est pas encore configuré. Réessayez plus tard." });
    }
    const cle = hmac("email:" + email);
    const recent = await requete(
      "select 1 from codes where email_empreinte = $1 and envoye_le > now() - interval '1 minute'", [cle]);
    if (recent.length) {
      return repondre(res, 429, { ok: false, erreur: "Patientez une minute avant de demander un nouveau code." });
    }
    if (await depasse("code:email:" + cle, "hour", 5) || await depasse("code:ip:" + hmac("ip:" + ip(req)), "hour", 20)) {
      return repondre(res, 429, { ok: false, erreur: "Trop de demandes. Réessayez dans une heure." });
    }
    if (await depasse("code:site", "day", 200)) {
      return repondre(res, 429, {
        ok: false,
        erreur: "Le service d'envoi est très demandé aujourd'hui. Réessayez demain, vos outils fonctionnent sans compte.",
      });
    }
    const code = String(crypto.randomInt(0, 1000000)).padStart(6, "0");
    await requete(
      `insert into codes (email_empreinte, code_empreinte, expire_le, essais, envoye_le, verifie_le)
       values ($1, $2, now() + interval '10 minutes', 0, now(), null)
       on conflict (email_empreinte) do update set code_empreinte = excluded.code_empreinte,
         expire_le = excluded.expire_le, essais = 0, envoye_le = now(), verifie_le = null`,
      [cle, hmac("code:" + email + ":" + code)]);
    try {
      await sendTransactionalEmail(Object.assign({ to: email }, courrielDuCode(code)));
    } catch (erreur) {
      await requete("delete from codes where email_empreinte = $1", [cle]);
      console.error("compte demander-code envoi impossible");
      return repondre(res, 502, { ok: false, erreur: "Impossible d'envoyer le code pour le moment. Réessayez dans quelques minutes." });
    }
    repondre(res, 200, { ok: true });
  },
};

ACTIONS["verifier-code"] = {
  methode: "POST",
  faire: async (req, res) => {
    const c = corps(req) || {};
    const email = adresse(c.email);
    const code = typeof c.code === "string" ? c.code.replace(/\s/g, "") : "";
    if (!email || !/^\d{6}$/.test(code)) {
      return repondre(res, 400, { ok: false, erreur: "Entrez le code à 6 chiffres reçu par email." });
    }
    if (await depasse("verif:ip:" + hmac("ip:" + ip(req)), "hour", 30)) {
      return repondre(res, 429, { ok: false, erreur: "Trop d'essais depuis ce réseau. Réessayez dans une heure." });
    }
    const cle = hmac("email:" + email);
    const lignes = await requete(
      "select code_empreinte, essais, expire_le < now() as expire from codes where email_empreinte = $1", [cle]);
    const attendu = lignes[0];
    if (!attendu || attendu.expire) {
      return repondre(res, 410, { ok: false, erreur: "Ce code a expiré. Demandez-en un nouveau." });
    }
    if (attendu.essais >= 5) return repondre(res, 429, { ok: false, erreur: "Trop d'essais. Demandez un nouveau code." });
    if (!egales(attendu.code_empreinte, hmac("code:" + email + ":" + code))) {
      const r = await requete(
        "update codes set essais = essais + 1 where email_empreinte = $1 returning essais", [cle]);
      const reste = Math.max(0, 5 - r[0].essais);
      if (!reste) return repondre(res, 429, { ok: false, erreur: "Trop d'essais. Demandez un nouveau code." });
      return repondre(res, 400, {
        ok: false, essaisRestants: reste,
        erreur: "Ce code ne correspond pas. Il vous reste " + reste + (reste > 1 ? " essais." : " essai."),
      });
    }
    let compte = (await requete("select id from comptes where email = $1", [email]))[0];
    let cree = false;
    if (!compte) {
      // Adresse nouvelle : l'étape Bienvenue demande les conditions ; le code
      // reste valable 15 minutes de plus, le temps de les accepter.
      if (c.conditions !== true) {
        await requete(
          "update codes set verifie_le = now(), expire_le = now() + interval '15 minutes' where email_empreinte = $1 and verifie_le is null",
          [cle]);
        return repondre(res, 200, { ok: true, nouveau: true });
      }
      try {
        compte = (await requete(
          "insert into comptes (email, conditions_version) values ($1, $2) returning id", [email, CONDITIONS]))[0];
        cree = true;
      } catch (erreur) {
        if (erreur.code !== "23505") throw erreur; // créé au même instant par une autre demande
        compte = (await requete("select id from comptes where email = $1", [email]))[0];
      }
      const prenom = typeof c.prenom === "string" ? c.prenom.trim().slice(0, 60) : "";
      if (cree && prenom) {
        await requete(
          "insert into elements (compte_id, cle, valeur, version) values ($1, 'fiche', $2, 1) on conflict do nothing",
          [compte.id, JSON.stringify({ prenom })]);
      }
    }
    await requete("delete from codes where email_empreinte = $1", [cle]);
    await requete("update comptes set vu_le = now(), averti_le = null where id = $1", [compte.id]);
    await ouvrirSession(res, compte.id);
    const fiche = await requete(
      "select valeur->>'prenom' as prenom from elements where compte_id = $1 and cle = 'fiche'", [compte.id]);
    repondre(res, 200, {
      ok: true, connecte: true, cree, compte: court(compte.id), prenom: (fiche[0] && fiche[0].prenom) || null,
    });
  },
};

// ─── Le compte (§ 3.6) : se déconnecter, de cet appareil ou de tous,
// télécharger ses données, supprimer son espace.

ACTIONS.deconnexion = {
  methode: "POST",
  session: true,
  faire: async (req, res) => {
    await requete("delete from sessions where jeton_empreinte = $1", [empreinte(lireJeton(req))]);
    effacerCookie(res);
    repondre(res, 200, { ok: true });
  },
};

// Les sessions sont marquées, pas effacées : chaque autre appareil apprend
// ainsi, à sa prochaine visite, que sa connexion a été fermée (§ 3.7).
ACTIONS["deconnexion-partout"] = {
  methode: "POST",
  session: true,
  faire: async (req, res, compte) => {
    await requete("update sessions set revoquee_le = now() where compte_id = $1 and revoquee_le is null", [compte.id]);
    effacerCookie(res);
    repondre(res, 200, { ok: true });
  },
};

ACTIONS.export = {
  methode: "GET",
  session: true,
  faire: async (req, res, compte) => {
    const iso = (date) => new Date(date).toISOString();
    const info = (await requete("select cree_le, vu_le from comptes where id = $1", [compte.id]))[0];
    const donnees = {
      exporte_le: new Date().toISOString(),
      compte: { email: compte.email, cree_le: iso(info.cree_le), derniere_connexion: iso(info.vu_le) },
      fiche: null, diagnostic: null, plan: null, calculs: null,
    };
    for (const e of await requete("select cle, valeur from elements where compte_id = $1", [compte.id])) {
      donnees[e.cle] = e.valeur;
    }
    const jour = new Date().toISOString().slice(0, 10);
    res.setHeader("Content-Disposition", `attachment; filename="pilotia-mon-espace-${jour}.json"`);
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", "no-store");
    res.status(200).send(JSON.stringify(donnees, null, 2));
  },
};

// Effacement immédiat et définitif : les sessions et les éléments partent en
// cascade avec le compte.
ACTIONS.supprimer = {
  methode: "POST",
  session: true,
  faire: async (req, res, compte) => {
    if ((corps(req) || {}).confirmer !== true) {
      return repondre(res, 400, { ok: false, erreur: "Confirmez la suppression de votre espace." });
    }
    await requete("delete from comptes where id = $1", [compte.id]);
    effacerCookie(res);
    repondre(res, 200, { ok: true });
  },
};
