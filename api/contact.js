// POST /api/contact
// Transmet un message du formulaire de contact par email transactionnel Brevo.
//
// Body attendu (JSON) :
//   { nom, email, entreprise?, profil?, message, consent: true, website: "" }
// Réponse : { ok: true } ou { ok: false, error: "..." }
//
// Choix délibéré : l'expéditeur n'est PAS ajouté à la liste de contacts marketing.
// Il écrit pour obtenir une réponse, pas pour s'abonner — l'inscrire d'office
// serait un détournement de finalité (RGPD art. 5.1.b) et un consentement non donné.

const { isConfigured, isValidEmail, sendTransactionalEmail } = require("./_brevo");

// Longueurs maximales : bornent la charge utile et évitent qu'un champ démesuré
// parte tel quel dans un email.
const LIMITS = { nom: 120, email: 200, entreprise: 160, profil: 80, message: 4000 };

function clean(value, max) {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}

// Le contenu est réinjecté dans un email HTML : sans échappement, un message
// contenant du balisage pourrait altérer l'email reçu.
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json");

  if (req.method !== "POST") {
    res.status(405).json({ ok: false, error: "Méthode non autorisée." });
    return;
  }

  const body = req.body || {};

  // Champ leurre : invisible et hors du parcours au clavier, seul un robot le remplit.
  // On répond 200 sans rien envoyer, pour ne pas renseigner l'émetteur sur le filtrage.
  if (clean(body.website, 100)) {
    res.status(200).json({ ok: true });
    return;
  }

  const nom = clean(body.nom, LIMITS.nom);
  const email = clean(body.email, LIMITS.email);
  const entreprise = clean(body.entreprise, LIMITS.entreprise);
  const profil = clean(body.profil, LIMITS.profil);
  const message = clean(body.message, LIMITS.message);

  if (!nom || !message) {
    res.status(400).json({ ok: false, error: "Merci d'indiquer votre nom et votre message." });
    return;
  }
  if (!isValidEmail(email)) {
    res.status(400).json({ ok: false, error: "Adresse email invalide." });
    return;
  }
  if (body.consent !== true) {
    res.status(400).json({ ok: false, error: "Merci d'accepter le traitement de votre message pour pouvoir l'envoyer." });
    return;
  }

  if (!isConfigured()) {
    res.status(503).json({
      ok: false,
      error: "Le service d'envoi n'est pas encore configuré. Écrivez-nous directement par email en attendant.",
    });
    return;
  }

  const destinataire = process.env.CONTACT_RECIPIENT || process.env.BREVO_SENDER_EMAIL;
  if (!destinataire) {
    console.error("contact: ni CONTACT_RECIPIENT ni BREVO_SENDER_EMAIL n'est défini");
    res.status(503).json({
      ok: false,
      error: "Le service d'envoi n'est pas encore configuré. Écrivez-nous directement par email en attendant.",
    });
    return;
  }

  const html = `
    <p><strong>Nouveau message depuis le site Pilotia</strong></p>
    <p>
      <strong>Nom :</strong> ${escapeHtml(nom)}<br>
      <strong>Email :</strong> ${escapeHtml(email)}<br>
      <strong>Entreprise :</strong> ${escapeHtml(entreprise) || "(non précisée)"}<br>
      <strong>Profil :</strong> ${escapeHtml(profil) || "(non précisé)"}
    </p>
    <p><strong>Message :</strong></p>
    <p style="white-space:pre-wrap">${escapeHtml(message)}</p>
  `;

  try {
    await sendTransactionalEmail({
      to: destinataire,
      subject: `Contact site — ${nom}`,
      htmlContent: html,
      replyTo: { email, name: nom },
    });
    res.status(200).json({ ok: true });
  } catch (err) {
    console.error("contact error:", err);
    res.status(502).json({ ok: false, error: "Impossible d'envoyer votre message pour le moment. Réessayez dans quelques minutes." });
  }
};
