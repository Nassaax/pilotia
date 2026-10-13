// /api/menage : ménage de nuit de l'espace client (brand/espace-client-CONCEPTION.md, § 6).
//
// Vercel l'appelle chaque nuit (vercel.json, « crons ») avec l'en-tête
// Authorization: Bearer <CRON_SECRET>. Les tâches planifiées ne tournent que
// sur le site public : tant que l'espace y est fermé, il n'y a rien à faire.
//   1. efface les codes, sessions et compteurs périmés ;
//   2. avertit par email, 50 au plus par nuit, les espaces sans connexion
//      depuis 23 mois ;
//   3. supprime ceux sans connexion depuis 24 mois, avertis depuis 25 jours.
// Le journal ne garde que des nombres : c'est là que Pilotia voit le nombre
// de comptes.

const crypto = require("crypto");
const { requete, disponible } = require("./_base");
const { ouvert } = require("./_session");
const { sendTransactionalEmail } = require("./_brevo");

const MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
  "septembre", "octobre", "novembre", "décembre"];

function autorise(req) {
  const secret = process.env.CRON_SECRET;
  const recu = Buffer.from(req.headers.authorization || "");
  const attendu = Buffer.from("Bearer " + (secret || ""));
  return Boolean(secret) && recu.length === attendu.length && crypto.timingSafeEqual(recu, attendu);
}

function dateLongue(date) {
  const d = new Date(date);
  return d.getUTCDate() + " " + MOIS[d.getUTCMonth()] + " " + d.getUTCFullYear();
}

function avertissement(date) {
  return {
    subject: "Votre espace Pilotia sera supprimé le " + date,
    htmlContent:
      "<p>Bonjour,</p>" +
      "<p>Votre espace Pilotia sera supprimé le " + date + " faute de connexion. Pour le garder, " +
      "connectez-vous simplement avant cette date, depuis l'onglet Mon espace du site Pilotia.</p>" +
      "<p>Sans connexion d'ici là, votre fiche, vos résultats et vos calculs seront effacés définitivement.</p>",
    textContent:
      "Bonjour,\n\nVotre espace Pilotia sera supprimé le " + date + " faute de connexion. Pour le garder, " +
      "connectez-vous simplement avant cette date, depuis l'onglet Mon espace du site Pilotia.\n\n" +
      "Sans connexion d'ici là, votre fiche, vos résultats et vos calculs seront effacés définitivement.\n",
  };
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (!autorise(req)) return res.status(401).json({ ok: false });
  if (!ouvert() || !disponible()) return res.status(200).json({ ok: true, ignore: true });
  try {
    await requete("delete from codes where expire_le < now() - interval '1 hour'");
    await requete("delete from sessions where expire_le < now()");
    await requete("delete from limites where fenetre < now() - interval '2 days'");

    let avertis = 0;
    const aAvertir = await requete(
      `select id, email, vu_le + interval '24 months' as supprime_le from comptes
        where vu_le < now() - interval '23 months' and averti_le is null
        order by vu_le limit 50`);
    for (const c of aAvertir) {
      try {
        await sendTransactionalEmail(Object.assign({ to: c.email }, avertissement(dateLongue(c.supprime_le))));
        await requete("update comptes set averti_le = now() where id = $1", [c.id]);
        avertis += 1;
      } catch (erreur) {
        console.error("menage avertissement impossible");
      }
    }

    const supprimes = await requete(
      `delete from comptes
        where vu_le < now() - interval '24 months'
          and averti_le is not null and averti_le < now() - interval '25 days'
        returning id`);
    const comptes = (await requete("select count(*)::int as n from comptes"))[0].n;
    console.log("menage comptes=" + comptes + " avertis=" + avertis + " supprimes=" + supprimes.length);
    res.status(200).json({ ok: true, comptes, avertis, supprimes: supprimes.length });
  } catch (erreur) {
    console.error("menage", erreur.code || erreur.name || "erreur");
    res.status(500).json({ ok: false });
  }
};
