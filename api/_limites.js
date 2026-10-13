// Compteurs anti-abus de l'espace client (brand/espace-client-CONCEPTION.md, § 5).
//
// Une ligne par clé et par fenêtre (l'heure ou le jour en cours). Les clés
// sont des empreintes : ni adresse email ni adresse IP n'y figurent en clair.
// Le ménage de nuit efface les fenêtres de plus de 2 jours.

const { requete } = require("./_base");

// Compte une demande de plus dans la fenêtre en cours ; vrai si la limite est
// alors dépassée. unite : "hour" ou "day".
async function depasse(cle, unite, maximum) {
  const lignes = await requete(
    `insert into limites (cle, fenetre, nombre) values ($1, date_trunc($2, now()), 1)
     on conflict (cle, fenetre) do update set nombre = limites.nombre + 1
     returning nombre`,
    [cle, unite]);
  return lignes[0].nombre > maximum;
}

// L'adresse IP du visiteur, telle que Vercel la transmet.
function ip(req) {
  return req.headers["x-real-ip"]
    || (req.headers["x-forwarded-for"] || "").split(",")[0].trim()
    || (req.socket && req.socket.remoteAddress)
    || "inconnue";
}

module.exports = { depasse, ip };
