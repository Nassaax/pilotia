// Génère les documents téléchargeables de ressources.html.
//
//   node scripts/generer-pdf.js
//
// Les chiffres cités (INASTI, seuil TVA, ONSS) sont ceux déjà vérifiés et
// affichés sur le site. Ils sont regroupés dans CHIFFRES ci-dessous : en cas
// de mise à jour d'un barème, c'est le seul endroit à corriger.

const fs = require("fs");
const path = require("path");
const PDFDocument = require("pdfkit");

const SORTIE = path.join(__dirname, "..", "downloads");
const MARINE = "#1B2A41";
const BRONZE = "#876231";
const ENCRE = "#1F2937";
const DOUX = "#556070";
const TRAIT = "#D7DEE7";

const CHIFFRES = {
  tauxBas: "20,5 %",
  seuilBas: "75 024,54 €",
  tauxHaut: "14,16 %",
  seuilHaut: "110 562,42 €",
  minTrimestre: "917,58 €",
  maxTrimestre: "5 258,69 €",
  exoneration: "1 922,16 €",
  franchiseTVA: "25 000 €",
  onssEmploye: "environ 25 %",
  onssOuvrier: "environ 30 à 35 %",
};

const AVERTISSEMENT =
  "Document d'information à but pédagogique, établi sur la base de barèmes publics " +
  "susceptibles d'évoluer. Il ne constitue ni un conseil fiscal, ni un conseil comptable, " +
  "ni un conseil juridique. Pilotia n'est pas expert-comptable et n'est inscrit à aucun " +
  "ordre professionnel à ce titre : vérifiez toujours votre situation auprès de votre " +
  "comptable, de votre caisse d'assurances sociales ou de l'administration compétente.";

// ---------------------------------------------------------------- mise en page

function titreSection(doc, texte) {
  if (doc.y > doc.page.height - 190) doc.addPage();
  doc.moveDown(0.7);
  doc.fillColor(BRONZE).font("Helvetica-Bold").fontSize(12.5)
     .text(texte.toUpperCase(), { characterSpacing: 0.6 });
  doc.moveDown(0.35);
  doc.fillColor(ENCRE).font("Helvetica").fontSize(10.5);
}

function para(doc, texte) {
  if (doc.y > doc.page.height - 130) doc.addPage();
  doc.fillColor(ENCRE).font("Helvetica").fontSize(10.5)
     .text(texte, { align: "left", lineGap: 2.5 });
  doc.moveDown(0.5);
}

function puces(doc, items) {
  items.forEach((it) => {
    if (doc.y > doc.page.height - 120) doc.addPage();
    const y = doc.y;
    doc.circle(61, y + 5.5, 2).fill(BRONZE);
    doc.fillColor(ENCRE).font("Helvetica").fontSize(10.5)
       .text(it, 72, y, { width: doc.page.width - 128, lineGap: 2 });
    doc.moveDown(0.3);
  });
  doc.moveDown(0.3);
  doc.x = 56; // sans ça l'indentation des puces contamine tout ce qui suit
}

// Cases à cocher : le document est pensé pour être imprimé et rempli.
function cases(doc, items) {
  items.forEach((it) => {
    if (doc.y > doc.page.height - 120) doc.addPage();
    const y = doc.y;
    doc.roundedRect(57, y + 1, 11, 11, 2).lineWidth(1).stroke(BRONZE);
    doc.fillColor(ENCRE).font("Helvetica").fontSize(10.5)
       .text(it, 76, y, { width: doc.page.width - 132, lineGap: 2 });
    doc.moveDown(0.42);
  });
  doc.moveDown(0.3);
  doc.x = 56;
}

function encadre(doc, texte) {
  if (doc.y > doc.page.height - 170) doc.addPage();
  const haut = doc.y;
  const largeur = doc.page.width - 112;
  doc.font("Helvetica").fontSize(10);
  const hauteur = doc.heightOfString(texte, { width: largeur - 32, lineGap: 2 }) + 24;
  doc.roundedRect(56, haut, largeur, hauteur, 6).fill("#F3E9DA");
  doc.fillColor(ENCRE).font("Helvetica").fontSize(10)
     .text(texte, 72, haut + 12, { width: largeur - 32, lineGap: 2 });
  doc.y = haut + hauteur + 12;
  doc.x = 56;
}

// Tableau simple à colonnes fixes.
function tableau(doc, entetes, lignes, largeurs) {
  if (doc.y > doc.page.height - 200) doc.addPage();
  let y = doc.y;
  let x = 56;
  doc.font("Helvetica-Bold").fontSize(9).fillColor(MARINE);
  entetes.forEach((e, i) => {
    doc.text(e.toUpperCase(), x, y, { width: largeurs[i] - 8 });
    x += largeurs[i];
  });
  y += 16;
  doc.moveTo(56, y - 4).lineTo(doc.page.width - 56, y - 4).lineWidth(1).stroke(TRAIT);

  lignes.forEach((ligne) => {
    if (y > doc.page.height - 110) {
      doc.addPage();
      y = doc.y;
    }
    x = 56;
    let hMax = 0;
    doc.font("Helvetica").fontSize(9.5).fillColor(ENCRE);
    ligne.forEach((cell, i) => {
      const h = doc.heightOfString(cell, { width: largeurs[i] - 8, lineGap: 1.5 });
      hMax = Math.max(hMax, h);
      doc.text(cell, x, y + 4, { width: largeurs[i] - 8, lineGap: 1.5 });
      x += largeurs[i];
    });
    y += hMax + 12;
    doc.moveTo(56, y - 4).lineTo(doc.page.width - 56, y - 4).lineWidth(0.5).stroke(TRAIT);
  });
  doc.y = y + 8;
  doc.x = 56;
}

// Pied de page ajouté a posteriori : la numérotation n'est connue qu'une fois
// tout le contenu écrit.
//
// lineBreak:false et height sont indispensables : un texte de pied de page qui
// déborde de la marge fait créer une page supplémentaire par pdfkit, à chaque
// page — ce qui produisait six pages pour deux pages de contenu, et faisait
// disparaître le pied lui-même.
const PIED = "Pilotia — document d'information. Ne remplace pas l'avis d'un comptable agréé.";

function finaliser(doc) {
  const plage = doc.bufferedPageRange();
  for (let i = 0; i < plage.count; i++) {
    doc.switchToPage(plage.start + i);
    const bas = doc.page.height - 46;
    doc.moveTo(56, bas - 12).lineTo(doc.page.width - 56, bas - 12).lineWidth(0.5).stroke(TRAIT);
    doc.font("Helvetica").fontSize(7.5).fillColor(DOUX)
       .text(PIED, 56, bas, { width: doc.page.width - 150, height: 12, lineBreak: false });
    doc.font("Helvetica-Bold").fontSize(8).fillColor(DOUX)
       .text(`${i + 1} / ${plage.count}`, doc.page.width - 110, bas, {
         width: 54, align: "right", height: 12, lineBreak: false,
       });
  }
  doc.flushPages();
}

function ecrire(doc, nomFichier) {
  // L'avertissement complet en fin de document plutôt qu'en pied de chaque
  // page : il reste lisible et n'alourdit pas la lecture.
  titreSection(doc, "Avertissement");
  doc.fillColor(DOUX).font("Helvetica").fontSize(9)
     .text(AVERTISSEMENT, 56, doc.y, { width: doc.page.width - 112, lineGap: 2 });

  return new Promise((resolve) => {
    const chemin = path.join(SORTIE, nomFichier);
    const flux = fs.createWriteStream(chemin);
    doc.pipe(flux);
    finaliser(doc);
    doc.end();
    flux.on("finish", () => {
      const ko = (fs.statSync(chemin).size / 1024).toFixed(0);
      console.log(`  ${nomFichier.padEnd(48)} ${ko} Ko`);
      resolve();
    });
  });
}

function doc(titre, sousTitre) {
  const d = new PDFDocument({
    size: "A4",
    bufferPages: true,
    margins: { top: 56, bottom: 72, left: 56, right: 56 },
    info: { Title: titre, Author: "Pilotia", Subject: sousTitre, Creator: "Pilotia" },
  });
  d.rect(0, 0, d.page.width, 132).fill(MARINE);
  d.fillColor("#FFFFFF").font("Helvetica-Bold").fontSize(11)
   .text("PILOTIA", 56, 32, { characterSpacing: 2 });
  d.fillColor("#FFFFFF").font("Helvetica-Bold").fontSize(20)
   .text(titre, 56, 54, { width: d.page.width - 112 });
  if (sousTitre) {
    d.fillColor("#C6D2E0").font("Helvetica").fontSize(10)
     .text(sousTitre, 56, d.y + 3, { width: d.page.width - 112 });
  }
  d.y = 164;
  d.x = 56;
  return d;
}

module.exports = { doc, titreSection, para, puces, cases, encadre, tableau, ecrire, CHIFFRES, SORTIE };
