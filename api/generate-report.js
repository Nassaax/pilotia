// POST /api/generate-report
// Génère le rapport diagnostic détaillé personnalisé (produit à 19 €, voir
// diagnostic.html → rapport-diagnostic.html) : appelle l'API Claude pour
// rédiger le contenu, le met en page en PDF (pdfkit), tente un envoi par
// email (Brevo, best-effort) et renvoie le PDF directement en réponse.
//
// Variables d'environnement requises :
//   ANTHROPIC_API_KEY   clé API Claude (console.anthropic.com)
//   ANTHROPIC_MODEL     optionnel, défaut "claude-sonnet-5"
//   BREVO_API_KEY       optionnel — sans elle, pas d'email envoyé ni de
//                       contact ajouté, mais le PDF est quand même généré
//                       et renvoyé au visiteur.
//
// Paiement : PAS ENCORE ACTIVÉ (décision explicite — voir rapport-diagnostic.html,
// qui affiche "version test, gratuit pendant le lancement"). Quand Stripe sera
// branché, insérer la vérification du paiement ici, avant l'appel à Claude,
// et ne générer le rapport qu'après confirmation.

const PDFDocument = require("pdfkit");
const { isConfigured: brevoConfigured, isValidEmail, upsertContact, sendTransactionalEmail } = require("./_brevo");

const ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages";

const SYSTEM_PROMPT = `Tu rédiges un rapport diagnostic pour Pilotia, un service de coaching business pour PME et indépendants en Belgique (restaurants, artisans, commerces, futurs indépendants). Le fondateur n'est PAS comptable agréé : ne donne jamais de conseil fiscal, comptable ou juridique précis (pas de montants d'impôts, pas de choix de statut juridique, pas de conseil de restructuration financière formelle). Pour tout ce qui touche à la fiscalité, la comptabilité ou le droit, renvoie explicitement vers un comptable agréé ou un professionnel adapté.

Le ton : chiffré et concret, jamais vague ; réaliste sur les moyens réels d'une petite structure (pas de plan qui suppose une équipe ou un budget que la personne n'a pas) ; direct et sans jargon.

Tu reçois les réponses d'un visiteur à un diagnostic express (8 questions, 4 thèmes : Finances, Personnel & organisation, Marketing digital, Trésorerie & résilience) ainsi que son secteur d'activité, la taille de son équipe et sa plus grande difficulté actuelle en texte libre.

Réponds UNIQUEMENT avec le contenu du rapport, structuré exactement ainsi (respecte ce format ligne par ligne, il sera mis en page automatiquement) :

## Synthèse
Un paragraphe de 3-4 phrases résumant la situation, en te basant sur les réponses ET la difficulté décrite en texte libre.

## Points forts
- Point fort 1, basé sur les réponses où le score est bon
- Point fort 2
(2 à 3 points, uniquement si réellement justifiés par les réponses — sinon dis que les bases restent à construire)

## Points de vigilance
- Point de vigilance 1, basé sur les réponses à faible score ou la difficulté décrite
- Point de vigilance 2
(2 à 4 points)

## Recommandations prioritaires
- Recommandation 1 : action concrète et réalisable rapidement
- Recommandation 2
- Recommandation 3
(3 à 5 recommandations, ordonnées par priorité, chacune actionnable en une phrase claire)

## Prochaines étapes
Un court paragraphe de conclusion qui invite à un accompagnement Pilotia pour aller plus loin, sans être trop commercial.`;

function buildUserPrompt({ diagnostic, secteur, taille, difficulte, prenom }) {
  var lignes = diagnostic.reponses.map(function (r) {
    return "- [" + r.theme + "] " + r.question + " → " + r.reponse;
  }).join("\n");

  var themesScore = Object.keys(diagnostic.themes).map(function (t) {
    return t + " : " + diagnostic.themes[t] + "/4";
  }).join(", ");

  return "Prénom : " + prenom + "\n" +
    "Secteur d'activité : " + secteur + "\n" +
    "Taille de l'équipe : " + taille + "\n" +
    "Score global au diagnostic express : " + diagnostic.total + "/16 (" + diagnostic.pill + ")\n" +
    "Scores par thème : " + themesScore + "\n\n" +
    "Réponses détaillées :\n" + lignes + "\n\n" +
    "Plus grande difficulté actuelle décrite par la personne : " + difficulte;
}

async function callClaude(userPrompt) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new ConfigError("ANTHROPIC_API_KEY manquante côté serveur.");
  }

  const res = await fetch(ANTHROPIC_API_URL, {
    method: "POST",
    headers: {
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: process.env.ANTHROPIC_MODEL || "claude-sonnet-5",
      max_tokens: 1600,
      temperature: 0.6,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: userPrompt }],
    }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error("Appel à Claude échoué (" + res.status + ") : " + body);
  }

  const data = await res.json();
  const text = (data.content || []).map(function (block) { return block.text || ""; }).join("\n");
  if (!text.trim()) {
    throw new Error("Réponse vide de Claude.");
  }
  return text;
}

// Erreur dédiée pour distinguer "pas configuré" (503) d'une vraie erreur (502).
function ConfigError(message) {
  this.name = "ConfigError";
  this.message = message;
}
ConfigError.prototype = Object.create(Error.prototype);

// Parseur minimal du format demandé à Claude (## titres, - listes, paragraphes).
function parseReportSections(text) {
  var lines = text.split("\n");
  var sections = [];
  var current = null;

  lines.forEach(function (line) {
    var trimmed = line.trim();
    if (trimmed.indexOf("## ") === 0) {
      current = { title: trimmed.slice(3).trim(), blocks: [] };
      sections.push(current);
      return;
    }
    if (!current) return;
    if (trimmed.indexOf("- ") === 0) {
      current.blocks.push({ type: "bullet", text: trimmed.slice(2).trim() });
    } else if (trimmed) {
      current.blocks.push({ type: "paragraph", text: trimmed });
    }
  });

  return sections;
}

const BRAND_NAVY = "#0F172A";
const BRAND_GOLD = "#AD7E3F";
const BRAND_INK_SOFT = "#475569";

function buildPdf({ prenom, sections }) {
  return new Promise(function (resolve, reject) {
    try {
      var doc = new PDFDocument({ size: "A4", margins: { top: 60, bottom: 60, left: 56, right: 56 } });
      var chunks = [];
      doc.on("data", function (chunk) { chunks.push(chunk); });
      doc.on("end", function () { resolve(Buffer.concat(chunks)); });
      doc.on("error", reject);

      // En-tête de marque (texte, pas d'image — simple et robuste en serverless)
      doc.fillColor(BRAND_NAVY).font("Helvetica-Bold").fontSize(20).text("PILOTIA", { characterSpacing: 1 });
      doc.moveDown(0.2);
      doc.fillColor(BRAND_GOLD).font("Helvetica").fontSize(10)
        .text("RAPPORT DIAGNOSTIC PERSONNALISÉ".toUpperCase(), { characterSpacing: 1.5 });
      doc.moveDown(1);
      doc.strokeColor(BRAND_GOLD).lineWidth(1.5)
        .moveTo(doc.page.margins.left, doc.y)
        .lineTo(doc.page.width - doc.page.margins.right, doc.y)
        .stroke();
      doc.moveDown(1.2);

      doc.fillColor(BRAND_NAVY).font("Helvetica-Bold").fontSize(15).text("Bonjour " + prenom + ",");
      doc.moveDown(0.8);

      sections.forEach(function (section) {
        doc.fillColor(BRAND_NAVY).font("Helvetica-Bold").fontSize(13).text(section.title);
        doc.moveDown(0.4);
        section.blocks.forEach(function (block) {
          if (block.type === "bullet") {
            doc.fillColor(BRAND_INK_SOFT).font("Helvetica").fontSize(11)
              .text("•  " + block.text, { indent: 10, lineGap: 3 });
          } else {
            doc.fillColor(BRAND_INK_SOFT).font("Helvetica").fontSize(11)
              .text(block.text, { lineGap: 3 });
          }
          doc.moveDown(0.25);
        });
        doc.moveDown(0.8);
      });

      doc.moveDown(1);
      doc.strokeColor("#E2E8F0").lineWidth(1)
        .moveTo(doc.page.margins.left, doc.y)
        .lineTo(doc.page.width - doc.page.margins.right, doc.y)
        .stroke();
      doc.moveDown(0.6);
      doc.fillColor(BRAND_INK_SOFT).font("Helvetica-Oblique").fontSize(9)
        .text("Ce rapport est une estimation pédagogique basée sur vos réponses, pas un conseil fiscal, comptable ou juridique personnalisé. Pour ces sujets, votre comptable agréé reste la référence. — Pilotia, pilotia.be", { lineGap: 2 });

      doc.end();
    } catch (err) {
      reject(err);
    }
  });
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ ok: false, error: "Méthode non autorisée." });
    return;
  }

  const { diagnostic, secteur, taille, difficulte, prenom, email } = req.body || {};

  if (!diagnostic || !Array.isArray(diagnostic.reponses) || !diagnostic.reponses.length) {
    res.status(400).json({ ok: false, error: "Diagnostic manquant — refaites le diagnostic express d'abord." });
    return;
  }
  if (!secteur || !difficulte || !prenom || !isValidEmail(email)) {
    res.status(400).json({ ok: false, error: "Merci de compléter tous les champs avec une adresse email valide." });
    return;
  }

  try {
    const userPrompt = buildUserPrompt({ diagnostic, secteur, taille, difficulte, prenom });
    const reportText = await callClaude(userPrompt);
    const sections = parseReportSections(reportText);

    if (!sections.length) {
      throw new Error("Le rapport généré est vide ou mal formé.");
    }

    const pdfBuffer = await buildPdf({ prenom, sections });

    // Best-effort : ajout du contact + envoi par email. Un échec ici ne doit
    // jamais empêcher le visiteur de récupérer son PDF (déjà généré).
    if (brevoConfigured()) {
      try {
        await upsertContact({
          email,
          attributes: {
            SOURCE: "site-pilotia",
            RESSOURCE: "rapport-diagnostic-19e",
            PRENOM: prenom,
            SECTEUR: secteur,
            SCORE_DIAGNOSTIC: diagnostic.total,
            DATE_INSCRIPTION: new Date().toISOString().slice(0, 10),
          },
        });
        await sendTransactionalEmail({
          to: email,
          toName: prenom,
          subject: "Votre rapport diagnostic Pilotia",
          htmlContent: "<p>Bonjour " + prenom + ",</p><p>Voici votre rapport diagnostic personnalisé, en pièce jointe.</p><p>— L'équipe Pilotia</p>",
          attachmentBase64: pdfBuffer.toString("base64"),
          attachmentName: "pilotia-rapport-diagnostic.pdf",
        });
      } catch (emailErr) {
        console.error("generate-report: envoi email/Brevo a échoué (non bloquant) :", emailErr);
      }
    }

    res.setHeader("Content-Type", "application/pdf");
    res.setHeader("Content-Disposition", 'attachment; filename="pilotia-rapport-diagnostic.pdf"');
    res.status(200).send(pdfBuffer);
  } catch (err) {
    if (err instanceof ConfigError) {
      console.error("generate-report config error:", err.message);
      res.status(503).json({ ok: false, error: "Le générateur de rapport n'est pas encore configuré (clé API manquante). Réessayez plus tard." });
      return;
    }
    console.error("generate-report error:", err);
    res.status(502).json({ ok: false, error: "La génération du rapport a échoué. Réessayez dans un instant." });
  }
};

// Exposé pour les tests uniquement (n'affecte pas le handler par défaut ci-dessus,
// que Vercel appelle directement comme fonction).
module.exports.parseReportSections = parseReportSections;
module.exports.buildPdf = buildPdf;
