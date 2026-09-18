// POST /api/subscribe
// Capture un email contre le téléchargement d'un lead magnet (ressources.html,
// outils.html) et l'ajoute à la liste Brevo pour la relance automatique.
//
// Body attendu (JSON) : { "email": "...", "resource": "guide-independant-pdf" }
// Réponse : { "ok": true } ou { "ok": false, "error": "..." }

const { isConfigured, isValidEmail, upsertContact } = require("./_brevo");

module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json");

  if (req.method !== "POST") {
    res.status(405).json({ ok: false, error: "Méthode non autorisée." });
    return;
  }

  if (!isConfigured()) {
    // Configuration manquante côté serveur (clé Brevo pas encore ajoutée dans
    // les variables d'environnement Vercel) — on le dit clairement plutôt que
    // de faire semblant que ça a marché.
    res.status(503).json({ ok: false, error: "Le service d'inscription n'est pas encore configuré. Réessayez plus tard." });
    return;
  }

  const { email, resource } = req.body || {};

  if (!isValidEmail(email)) {
    res.status(400).json({ ok: false, error: "Adresse email invalide." });
    return;
  }

  try {
    await upsertContact({
      email,
      attributes: {
        SOURCE: "site-pilotia",
        RESSOURCE: typeof resource === "string" ? resource.slice(0, 100) : "inconnue",
        DATE_INSCRIPTION: new Date().toISOString().slice(0, 10),
      },
    });
    res.status(200).json({ ok: true });
  } catch (err) {
    console.error("subscribe error:", err);
    res.status(502).json({ ok: false, error: "Impossible d'enregistrer votre email pour le moment." });
  }
};
