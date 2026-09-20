// Helper partagé pour les appels à l'API Brevo (capture de contact + envoi
// transactionnel). Utilisé par /api/subscribe et /api/generate-report.
//
// Variables d'environnement attendues (à définir dans Vercel → Project →
// Settings → Environment Variables, jamais dans le code) :
//   BREVO_API_KEY   clé API Brevo (Settings → SMTP & API → API Keys)
//   BREVO_LIST_ID   identifiant numérique de la liste de contacts Brevo
//                   (Contacts → Listes → cliquer sur la liste → l'ID est
//                   dans l'URL). Optionnel : sans elle, le contact est
//                   créé/mis à jour mais rattaché à aucune liste.

const BREVO_API_BASE = "https://api.brevo.com/v3";

function isConfigured() {
  return Boolean(process.env.BREVO_API_KEY);
}

function isValidEmail(email) {
  return typeof email === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Crée ou met à jour un contact Brevo. Idempotent : un email déjà connu est
// mis à jour (nouvel attribut SOURCE) plutôt que de provoquer une erreur.
async function upsertContact({ email, attributes }) {
  const apiKey = process.env.BREVO_API_KEY;
  if (!apiKey) {
    throw new Error("BREVO_API_KEY manquante — voir api/_brevo.js pour la configuration requise.");
  }

  // BREVO_LIST_ID est optionnelle et parfois mal renseignée (URL entière collée au
  // lieu du seul numéro, espace, etc.) — un parseInt raté ne doit jamais faire
  // échouer toute la capture de contact, juste être ignoré silencieusement.
  const parsedListId = process.env.BREVO_LIST_ID ? parseInt(process.env.BREVO_LIST_ID, 10) : NaN;
  const listIds = Number.isInteger(parsedListId) ? [parsedListId] : undefined;

  const res = await fetch(`${BREVO_API_BASE}/contacts`, {
    method: "POST",
    headers: {
      "api-key": apiKey,
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify({
      email,
      attributes,
      listIds,
      updateEnabled: true,
    }),
  });

  // Brevo renvoie 201 (créé) ou 204 (mis à jour via updateEnabled) selon les cas.
  if (res.status !== 201 && res.status !== 204) {
    const body = await res.text().catch(() => "");
    throw new Error(`Brevo upsertContact a échoué (${res.status}) : ${body}`);
  }
  return true;
}

// Envoie un email transactionnel, avec pièce jointe PDF optionnelle
// (attachmentBase64 = contenu du fichier encodé en base64).
async function sendTransactionalEmail({ to, toName, subject, htmlContent, attachmentBase64, attachmentName, replyTo }) {
  const apiKey = process.env.BREVO_API_KEY;
  if (!apiKey) {
    throw new Error("BREVO_API_KEY manquante.");
  }

  const payload = {
    sender: { name: "Pilotia", email: process.env.BREVO_SENDER_EMAIL || "contact@pilotia.be" },
    to: [{ email: to, name: toName || undefined }],
    subject,
    htmlContent,
  };

  // Pour une notification de formulaire, l'expéditeur reste Pilotia (contrainte
  // SPF/DKIM du domaine vérifié) : c'est replyTo qui permet de répondre
  // directement à la personne plutôt qu'à soi-même.
  if (replyTo && replyTo.email) {
    payload.replyTo = { email: replyTo.email, name: replyTo.name || undefined };
  }

  if (attachmentBase64 && attachmentName) {
    payload.attachment = [{ content: attachmentBase64, name: attachmentName }];
  }

  const res = await fetch(`${BREVO_API_BASE}/smtp/email`, {
    method: "POST",
    headers: {
      "api-key": apiKey,
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Brevo sendTransactionalEmail a échoué (${res.status}) : ${body}`);
  }
  return true;
}

module.exports = { isConfigured, isValidEmail, upsertContact, sendTransactionalEmail };
