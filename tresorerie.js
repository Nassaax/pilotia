/* Plan de trésorerie prévisionnel — Pilotia
 *
 * Tout se calcule et se stocke dans le navigateur : aucune donnée financière
 * ne part vers un serveur. C'est un choix, pas une limite technique — ces
 * chiffres n'ont aucune raison de transiter par nous, et cela évite au passage
 * d'avoir à sécuriser et déclarer un traitement de données d'entreprise.
 *
 * La sauvegarde vit donc dans localStorage, propre à un navigateur. D'où le
 * bouton d'export : c'est le seul moyen de retrouver son plan sur un autre
 * appareil, ou après un vidage de cache.
 */
(function () {
  "use strict";

  var racine = document.getElementById("treso");
  if (!racine) return;

  var CLE = "pilotia-tresorerie";
  var VERSION = 2;

  // Catégories pré-remplies au rythme belge : les cotisations sociales et la
  // TVA tombent par trimestre, et c'est précisément ce qui crée les trous de
  // trésorerie que personne n'avait vus venir.
  var MODELE = {
    version: VERSION,
    soldeDepart: 12000,
    moisDepart: null, // rempli au premier chargement avec le mois en cours
    horizon: 12,
    seuil: 5000,
    lignes: [
      { id: 1, sens: "in", categorie: "Ventes / prestations", montant: 8200, frequence: "mensuel", decalage: 0 },
      { id: 2, sens: "in", categorie: "Acomptes clients", montant: 1500, frequence: "mensuel", decalage: 0 },
      { id: 3, sens: "out", categorie: "Achats et matières", montant: 2800, frequence: "mensuel", decalage: 0 },
      { id: 4, sens: "out", categorie: "Salaires et ONSS", montant: 3200, frequence: "mensuel", decalage: 0 },
      { id: 5, sens: "out", categorie: "Loyer et charges", montant: 950, frequence: "mensuel", decalage: 0 },
      { id: 6, sens: "out", categorie: "Assurances", montant: 180, frequence: "mensuel", decalage: 0 },
      { id: 7, sens: "out", categorie: "Comptable", montant: 150, frequence: "mensuel", decalage: 0 },
      { id: 8, sens: "out", categorie: "Cotisations sociales", montant: 1700, frequence: "trimestriel", decalage: 0 },
      { id: 9, sens: "out", categorie: "TVA à reverser", montant: 2400, frequence: "trimestriel", decalage: 0 },
    ],
    // Factures déjà engagées mais pas encore passées en banque. C'est ce qui
    // sépare une projection vague d'une projection juste : une grosse facture
    // client qui tombe le 12 du mois suivant déplace le point bas.
    factures: [],
  };

  var MOIS_COURTS = ["janv.", "févr.", "mars", "avr.", "mai", "juin",
                     "juil.", "août", "sept.", "oct.", "nov.", "déc."];
  var MOIS_LONGS = ["janvier", "février", "mars", "avril", "mai", "juin",
                    "juillet", "août", "septembre", "octobre", "novembre", "décembre"];

  var etat = charger();
  var prochainId = etat.lignes.reduce(function (m, l) { return Math.max(m, l.id); }, 0) + 1;

  // ───────────────────────────────────────────────── persistance

  function charger() {
    var brut = null;
    try { brut = localStorage.getItem(CLE); } catch (e) {}
    if (brut) {
      try {
        var d = JSON.parse(brut);
        if (d && Array.isArray(d.lignes)) {
          // Migration douce : un plan enregistré avant l'ajout des factures
          // reste valable, on lui ajoute simplement le champ manquant.
          if (d.version === 1) { d.factures = []; d.version = 2; }
          if (d.version === VERSION) {
            if (!Array.isArray(d.factures)) d.factures = [];
            return d;
          }
        }
      } catch (e) {}
    }
    var neuf = JSON.parse(JSON.stringify(MODELE));
    var maintenant = new Date();
    neuf.moisDepart = maintenant.getFullYear() + "-" + pad(maintenant.getMonth() + 1);
    return neuf;
  }

  function sauver() {
    try { localStorage.setItem(CLE, JSON.stringify(etat)); } catch (e) {}
  }

  function pad(n) { return (n < 10 ? "0" : "") + n; }

  // ───────────────────────────────────────────────── calcul

  function montantDuMois(ligne, index) {
    var dec = ligne.decalage || 0;
    switch (ligne.frequence) {
      case "mensuel": return ligne.montant;
      case "trimestriel": return (index % 3 === dec % 3) ? ligne.montant : 0;
      case "annuel": return (index % 12 === dec % 12) ? ligne.montant : 0;
      case "ponctuel": return (index === dec) ? ligne.montant : 0;
      default: return 0;
    }
  }

  // Rang du mois projeté dans lequel tombe une date (0 = premier mois).
  // Renvoie null si la date est absente ou illisible, un nombre négatif si
  // elle est antérieure au début de la projection.
  function indexDuMois(iso, an, mo) {
    if (!iso) return null;
    var p = String(iso).split("-");
    var a = parseInt(p[0], 10), m = parseInt(p[1], 10);
    if (!a || !m) return null;
    return (a - an) * 12 + (m - 1 - mo);
  }

  function calculer() {
    var parts = (etat.moisDepart || "").split("-");
    var an = parseInt(parts[0], 10) || new Date().getFullYear();
    var mo = (parseInt(parts[1], 10) || 1) - 1;

    var mois = [];
    var solde = etat.soldeDepart;
    for (var i = 0; i < etat.horizon; i++) {
      var d = new Date(an, mo + i, 1);
      var entrees = 0, sorties = 0, detail = {};
      etat.lignes.forEach(function (l) {
        var m = montantDuMois(l, i);
        if (!m) return;
        if (l.sens === "in") entrees += m; else sorties += m;
        var cle = l.sens + "|" + l.categorie;
        detail[cle] = (detail[cle] || 0) + m;
      });

      // Factures engagées : elles comptent dans le mois de leur échéance, et
      // seulement tant qu'elles ne sont pas réglées. Une échéance déjà passée
      // est rattachée au premier mois projeté : l'argent n'est toujours pas là.
      etat.factures.forEach(function (fa) {
        if (fa.regle) return;
        var idx = indexDuMois(fa.echeance, an, mo);
        if (idx === null) return;
        if (idx < 0) idx = 0;
        if (idx !== i) return;
        if (fa.sens === "in") entrees += fa.montant; else sorties += fa.montant;
        var c = fa.sens + "|" + (fa.sens === "in" ? "Factures à encaisser" : "Factures à payer");
        detail[c] = (detail[c] || 0) + fa.montant;
      });
      var debut = solde;
      solde = debut + entrees - sorties;
      mois.push({
        annee: d.getFullYear(), mois: d.getMonth(),
        debut: debut, entrees: entrees, sorties: sorties,
        variation: entrees - sorties, fin: solde, detail: detail,
      });
    }
    return mois;
  }

  function euros(n) {
    // toLocaleString insère des espaces fines insécables (U+202F) ou
    // insécables (U+00A0) comme séparateur de milliers. On les ramène à
    // une espace ordinaire pour que le texte reste comparable et testable.
    return Math.round(n).toLocaleString("fr-BE")
      .replace(/[\u202f\u00a0]/g, " ") + " \u20ac";
  }

  // ───────────────────────────────────────────────── rendu

  function rendre() {
    var mois = calculer();

    // Point bas : le mois où le solde de fin est le plus faible. C'est
    // l'information que le solde bancaire du jour ne donne jamais.
    var bas = mois[0];
    mois.forEach(function (m) { if (m.fin < bas.fin) bas = m; });
    var fin = mois[mois.length - 1];

    maj("kpi-depart", euros(etat.soldeDepart));
    maj("kpi-depart-note", MOIS_LONGS[mois[0].mois] + " " + mois[0].annee);
    maj("kpi-bas", euros(bas.fin));
    maj("kpi-bas-note", "fin " + MOIS_LONGS[bas.mois] + " " + bas.annee);
    maj("kpi-fin", euros(fin.fin));
    maj("kpi-fin-note", "fin " + MOIS_LONGS[fin.mois] + " " + fin.annee);

    var elBas = document.getElementById("kpi-bas");
    elBas.classList.toggle("kpi-alerte", bas.fin < etat.seuil);
    elBas.classList.toggle("kpi-ok", bas.fin >= etat.seuil);

    var verdict = document.getElementById("treso-verdict");
    if (bas.fin < 0) {
      verdict.className = "note treso-verdict treso-verdict-rouge";
      verdict.textContent = "Votre trésorerie passe en négatif fin " + MOIS_LONGS[bas.mois] +
        " (" + euros(bas.fin) + "). C'est le moment à préparer dès maintenant : décaler une dépense, " +
        "accélérer un encaissement, ou prévoir une avance.";
    } else if (bas.fin < etat.seuil) {
      verdict.className = "note treso-verdict treso-verdict-orange";
      verdict.textContent = "Votre point bas (" + euros(bas.fin) + " fin " + MOIS_LONGS[bas.mois] +
        ") passe sous votre seuil de sécurité de " + euros(etat.seuil) + ". Ça tient, mais sans marge d'imprévu.";
    } else {
      verdict.className = "note treso-verdict treso-verdict-vert";
      verdict.textContent = "Votre point bas (" + euros(bas.fin) + " fin " + MOIS_LONGS[bas.mois] +
        ") reste au-dessus de votre seuil de sécurité. Rien d'alarmant sur l'horizon choisi.";
    }

    dessinerCourbe(mois, bas);
    dessinerBarres(mois);
    remplirTableau(mois);
    rendreLignes();
    rendreFactures();
    sauver();
  }

  function maj(id, texte) {
    var el = document.getElementById(id);
    if (el) el.textContent = texte;
  }

  // ───────────────────────────────────────────────── graphiques
  // Deux visuels séparés plutôt qu'un seul à double échelle : superposer un
  // solde en euros et des flux mensuels sur un même axe donne un graphique
  // joli et illisible, où deux courbes qui se croisent ne veulent rien dire.

  function dessinerCourbe(mois, bas) {
    var L = 720, H = 260, gauche = 58, droite = 16, haut = 18, basM = 34;
    var w = L - gauche - droite, h = H - haut - basM;

    var vals = mois.map(function (m) { return m.fin; }).concat([etat.seuil, 0]);
    var vmax = Math.max.apply(null, vals);
    var vmin = Math.min.apply(null, vals);
    if (vmax === vmin) { vmax += 1000; vmin -= 1000; }
    var marge = (vmax - vmin) * 0.12;
    vmax += marge; vmin -= marge;

    function x(i) { return gauche + (mois.length === 1 ? w / 2 : (i * w) / (mois.length - 1)); }
    function y(v) { return haut + h - ((v - vmin) / (vmax - vmin)) * h; }

    var pts = mois.map(function (m, i) { return x(i) + " " + y(m.fin); });
    var ligne = "M " + pts.join(" L ");
    var aire = ligne + " L " + x(mois.length - 1) + " " + y(vmin) + " L " + x(0) + " " + y(vmin) + " Z";

    var s = [];
    s.push('<svg viewBox="0 0 ' + L + ' ' + H + '" role="img" aria-label="Courbe du solde de trésorerie prévisionnel. Les valeurs exactes figurent dans le plan de trésorerie ci-dessous.">');

    // Repères horizontaux
    for (var g = 0; g <= 3; g++) {
      var vy = haut + (g * h) / 3;
      s.push('<line x1="' + gauche + '" y1="' + vy + '" x2="' + (L - droite) + '" y2="' + vy +
             '" stroke="var(--line)" stroke-width="1"/>');
    }
    // Ligne du zéro, seulement si elle est dans le cadre
    if (vmin < 0 && vmax > 0) {
      s.push('<line x1="' + gauche + '" y1="' + y(0) + '" x2="' + (L - droite) + '" y2="' + y(0) +
             '" stroke="var(--ink-soft)" stroke-width="1.5"/>');
    }
    // Seuil de sécurité
    s.push('<line x1="' + gauche + '" y1="' + y(etat.seuil) + '" x2="' + (L - droite) + '" y2="' + y(etat.seuil) +
           '" stroke="var(--gold)" stroke-width="2" stroke-dasharray="7 5"/>');
    s.push('<text x="' + (gauche + 4) + '" y="' + (y(etat.seuil) - 6) +
           '" font-size="11" fill="var(--gold)" font-family="var(--font-body)">Seuil de sécurité</text>');

    s.push('<path d="' + aire + '" fill="var(--accent)" opacity=".12"/>');
    s.push('<path d="' + ligne + '" fill="none" stroke="var(--accent)" stroke-width="3" ' +
           'stroke-linecap="round" stroke-linejoin="round"/>');

    mois.forEach(function (m, i) {
      var estBas = (m === bas);
      s.push('<circle cx="' + x(i) + '" cy="' + y(m.fin) + '" r="' + (estBas ? 7 : 4) +
             '" fill="' + (estBas ? "var(--danger)" : "var(--card)") +
             '" stroke="' + (estBas ? "var(--danger)" : "var(--accent)") + '" stroke-width="2.5"/>');
      // Un libellé sur deux au-delà de 6 mois, sinon ils se chevauchent.
      if (mois.length <= 6 || i % 2 === 0) {
        s.push('<text x="' + x(i) + '" y="' + (H - 12) + '" text-anchor="middle" font-size="11" ' +
               'fill="var(--ink-soft)" font-family="var(--font-body)">' + MOIS_COURTS[m.mois] + '</text>');
      }
    });

    // Graduations verticales
    for (var k = 0; k <= 3; k++) {
      var vv = vmax - ((vmax - vmin) * k) / 3;
      s.push('<text x="' + (gauche - 8) + '" y="' + (haut + (k * h) / 3 + 4) + '" text-anchor="end" ' +
             'font-size="10" fill="var(--ink-soft)" font-family="var(--font-body)">' +
             Math.round(vv / 1000) + 'k</text>');
    }
    s.push("</svg>");
    document.getElementById("treso-courbe").innerHTML = s.join("");
  }

  function dessinerBarres(mois) {
    var L = 720, H = 150, gauche = 58, droite = 16, haut = 12, basM = 26;
    var w = L - gauche - droite, h = H - haut - basM;
    var mid = haut + h / 2;

    var pic = 1;
    mois.forEach(function (m) { pic = Math.max(pic, m.entrees, m.sorties); });
    var pas = w / mois.length;
    var larg = Math.min(18, pas * 0.32);

    var s = ['<svg viewBox="0 0 ' + L + ' ' + H + '" role="img" aria-label="Encaissements et décaissements par mois. Les valeurs exactes figurent dans le plan de trésorerie ci-dessous.">'];
    s.push('<line x1="' + gauche + '" y1="' + mid + '" x2="' + (L - droite) + '" y2="' + mid +
           '" stroke="var(--line)" stroke-width="1.5"/>');

    mois.forEach(function (m, i) {
      var cx = gauche + pas * i + pas / 2;
      var hIn = (m.entrees / pic) * (h / 2 - 6);
      var hOut = (m.sorties / pic) * (h / 2 - 6);
      s.push('<rect x="' + (cx - larg - 2) + '" y="' + (mid - hIn) + '" width="' + larg + '" height="' + hIn +
             '" rx="3" fill="#15803D" opacity=".85"/>');
      s.push('<rect x="' + (cx + 2) + '" y="' + mid + '" width="' + larg + '" height="' + hOut +
             '" rx="3" fill="var(--danger)" opacity=".8"/>');
      if (mois.length <= 6 || i % 2 === 0) {
        s.push('<text x="' + cx + '" y="' + (H - 8) + '" text-anchor="middle" font-size="10" ' +
               'fill="var(--ink-soft)" font-family="var(--font-body)">' + MOIS_COURTS[m.mois] + '</text>');
      }
    });
    s.push("</svg>");
    document.getElementById("treso-barres").innerHTML = s.join("");
  }

  // ───────────────────────────────────────────────── tableau

  function remplirTableau(mois) {
    var cats = { in: [], out: [] };
    etat.lignes.forEach(function (l) {
      if (cats[l.sens].indexOf(l.categorie) === -1) cats[l.sens].push(l.categorie);
    });
    // Les factures engagées créent leurs propres catégories. Sans ce second
    // passage, leur montant gonflait le total sans qu'aucune ligne du détail
    // n'explique d'où il venait.
    mois.forEach(function (m) {
      Object.keys(m.detail).forEach(function (k) {
        var i = k.indexOf("|");
        var sens = k.slice(0, i), cat = k.slice(i + 1);
        if (cats[sens] && cats[sens].indexOf(cat) === -1) cats[sens].push(cat);
      });
    });

    var h = ['<thead><tr><th scope="col">Catégorie</th>'];
    mois.forEach(function (m) {
      h.push('<th scope="col" class="treso-num">' + MOIS_COURTS[m.mois] + " " + String(m.annee).slice(2) + "</th>");
    });
    h.push("</tr></thead><tbody>");

    h.push(rangee("Solde de début", mois.map(function (m) { return m.debut; }), "treso-ligne-forte"));

    h.push(rangee("Encaissements", mois.map(function (m) { return m.entrees; }), "treso-ligne-in"));
    cats.in.forEach(function (c) {
      h.push(rangee(c, mois.map(function (m) { return m.detail["in|" + c] || 0; }), "treso-sous"));
    });

    h.push(rangee("Décaissements", mois.map(function (m) { return -m.sorties; }), "treso-ligne-out"));
    cats.out.forEach(function (c) {
      h.push(rangee(c, mois.map(function (m) { return -(m.detail["out|" + c] || 0); }), "treso-sous"));
    });

    h.push(rangee("Variation", mois.map(function (m) { return m.variation; }), "treso-ligne-forte"));
    h.push(rangee("Solde de fin", mois.map(function (m) { return m.fin; }), "treso-ligne-forte treso-ligne-fin"));
    h.push("</tbody>");

    document.getElementById("treso-tableau").innerHTML = h.join("");
  }

  function rangee(libelle, valeurs, classe) {
    var c = ['<tr class="' + classe + '"><th scope="row">' + echapper(libelle) + "</th>"];
    valeurs.forEach(function (v) {
      var signe = v < 0 ? "treso-neg" : (v > 0 ? "treso-pos" : "");
      c.push('<td class="treso-num ' + signe + '">' + (v === 0 ? "—" : euros(v)) + "</td>");
    });
    c.push("</tr>");
    return c.join("");
  }

  function echapper(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  // ───────────────────────────────────────────────── lignes saisies

  function rendreLignes() {
    ["in", "out"].forEach(function (sens) {
      var hote = document.getElementById(sens === "in" ? "lignes-in" : "lignes-out");
      var lignes = etat.lignes.filter(function (l) { return l.sens === sens; });
      if (!lignes.length) {
        hote.innerHTML = '<p class="treso-vide">Aucune ligne pour le moment.</p>';
        return;
      }
      hote.innerHTML = lignes.map(function (l) {
        return '<div class="treso-ligne" data-id="' + l.id + '">' +
          '<input type="text" value="' + echapper(l.categorie) + '" data-champ="categorie" aria-label="Libellé de la ligne">' +
          '<input type="number" value="' + l.montant + '" min="0" step="10" data-champ="montant" aria-label="Montant en euros">' +
          '<select data-champ="frequence" aria-label="Fréquence">' +
            opt("mensuel", "Chaque mois", l.frequence) +
            opt("trimestriel", "Chaque trimestre", l.frequence) +
            opt("annuel", "Une fois par an", l.frequence) +
            opt("ponctuel", "Une seule fois", l.frequence) +
          "</select>" +
          '<input type="number" value="' + (l.decalage || 0) + '" min="0" max="11" step="1" data-champ="decalage" ' +
            'aria-label="Décalage en mois" title="Décalage : 0 = dès le premier mois, 1 = le mois suivant, etc.">' +
          '<button type="button" class="treso-suppr" data-suppr="' + l.id + '" aria-label="Supprimer la ligne ' +
            echapper(l.categorie) + '">×</button>' +
        "</div>";
      }).join("");
    });
  }

  function opt(v, libelle, courant) {
    return '<option value="' + v + '"' + (v === courant ? " selected" : "") + ">" + libelle + "</option>";
  }


  // ───────────────────────────────────────────────── factures engagées

  function rendreFactures() {
    var parts = (etat.moisDepart || "").split("-");
    var an = parseInt(parts[0], 10), mo = (parseInt(parts[1], 10) || 1) - 1;

    ["in", "out"].forEach(function (sens) {
      var hote = document.getElementById(sens === "in" ? "factures-in" : "factures-out");
      var liste = etat.factures.filter(function (fa) { return fa.sens === sens; });
      if (!liste.length) {
        hote.innerHTML = '<p class="treso-vide">Aucune facture en attente.</p>';
      } else {
        // Les plus proches d'abord : c'est l'ordre dans lequel on s'en soucie.
        liste.sort(function (a, b) { return String(a.echeance).localeCompare(String(b.echeance)); });
        hote.innerHTML = liste.map(function (fa) {
          var idx = indexDuMois(fa.echeance, an, mo);
          var enRetard = !fa.regle && idx !== null && idx < 0;
          var horsHorizon = !fa.regle && idx !== null && idx >= etat.horizon;
          var alerte = "";
          if (enRetard) alerte = '<span class="treso-alerte">échéance dépassée — comptée sur le 1er mois</span>';
          else if (horsHorizon) alerte = '<span class="treso-hors">au-delà de l\'horizon choisi</span>';
          return '<div class="treso-facture' + (fa.regle ? " treso-facture-reglee" : "") + '" data-fid="' + fa.id + '">' +
            '<input type="text" value="' + echapper(fa.libelle) + '" data-fchamp="libelle" aria-label="Nom du client ou du fournisseur">' +
            '<input type="number" value="' + fa.montant + '" min="0" step="10" data-fchamp="montant" aria-label="Montant en euros">' +
            '<input type="date" value="' + echapper(fa.echeance || "") + '" data-fchamp="echeance" aria-label="Date d\'échéance">' +
            '<label class="treso-regle"><input type="checkbox" data-fchamp="regle"' + (fa.regle ? " checked" : "") +
              '> <span>Réglée</span></label>' +
            '<button type="button" class="treso-suppr" data-fsuppr="' + fa.id + '" aria-label="Supprimer la facture ' +
              echapper(fa.libelle) + '">×</button>' +
            (alerte ? '<p class="treso-facture-note">' + alerte + "</p>" : "") +
          "</div>";
        }).join("");
      }

      var total = liste.reduce(function (s, fa) { return s + (fa.regle ? 0 : fa.montant); }, 0);
      var nb = liste.filter(function (fa) { return !fa.regle; }).length;
      var resume = document.getElementById(sens === "in" ? "total-in" : "total-out");
      resume.textContent = nb === 0 ? "Rien en attente"
        : nb + (nb > 1 ? " factures" : " facture") + " — " + euros(total);
    });
  }

  // ───────────────────────────────────────────────── évènements

  racine.addEventListener("input", function (e) {
    var fchamp = e.target.getAttribute("data-fchamp");
    if (fchamp) {
      var bf = e.target.closest(".treso-facture");
      var fa = etat.factures.find(function (x) { return x.id === parseInt(bf.getAttribute("data-fid"), 10); });
      if (!fa) return;
      if (fchamp === "montant") fa.montant = Math.max(0, parseFloat(e.target.value) || 0);
      else if (fchamp === "regle") fa.regle = e.target.checked;
      else fa[fchamp] = e.target.value;
      rendreSansLignes();
      return;
    }
    var champ = e.target.getAttribute("data-champ");
    if (champ) {
      var bloc = e.target.closest(".treso-ligne");
      var l = etat.lignes.find(function (x) { return x.id === parseInt(bloc.getAttribute("data-id"), 10); });
      if (!l) return;
      l[champ] = (champ === "montant" || champ === "decalage")
        ? Math.max(0, parseFloat(e.target.value) || 0)
        : e.target.value;
      // On ne redessine pas les lignes pendant la frappe, sinon le champ perd
      // le focus à chaque caractère.
      rendreSansLignes();
      return;
    }
    var id = e.target.id;
    if (id === "p-solde") { etat.soldeDepart = parseFloat(e.target.value) || 0; rendre(); }
    if (id === "p-seuil") { etat.seuil = Math.max(0, parseFloat(e.target.value) || 0); rendre(); }
  });

  racine.addEventListener("change", function (e) {
    if (e.target.id === "p-horizon") { etat.horizon = parseInt(e.target.value, 10); rendre(); }
    if (e.target.id === "p-mois") { etat.moisDepart = e.target.value; rendre(); }
    if (e.target.getAttribute("data-champ") === "frequence") rendre();
    var fc = e.target.getAttribute("data-fchamp");
    // Une case cochée ou une date choisie changent l'état affiché de la
    // facture (grisée, alerte de retard) : il faut redessiner les listes.
    if (fc === "regle" || fc === "echeance") rendre();
  });

  racine.addEventListener("click", function (e) {
    var fsuppr = e.target.getAttribute("data-fsuppr");
    if (fsuppr) {
      etat.factures = etat.factures.filter(function (fa) { return fa.id !== parseInt(fsuppr, 10); });
      rendre();
      return;
    }
    var fajout = e.target.getAttribute("data-fajout");
    if (fajout) {
      var d = new Date();
      d.setMonth(d.getMonth() + 1);
      etat.factures.push({
        id: prochainId++, sens: fajout,
        libelle: fajout === "in" ? "Nouveau client" : "Nouveau fournisseur",
        montant: 0,
        echeance: d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()),
        regle: false,
      });
      rendre();
      var h = document.getElementById(fajout === "in" ? "factures-in" : "factures-out");
      var ch = h.querySelectorAll('input[data-fchamp="libelle"]');
      if (ch.length) { ch[ch.length - 1].focus(); ch[ch.length - 1].select(); }
      return;
    }
    var suppr = e.target.getAttribute("data-suppr");
    if (suppr) {
      etat.lignes = etat.lignes.filter(function (l) { return l.id !== parseInt(suppr, 10); });
      rendre();
      return;
    }
    var ajout = e.target.getAttribute("data-ajout");
    if (ajout) {
      etat.lignes.push({
        id: prochainId++, sens: ajout,
        categorie: ajout === "in" ? "Nouvelle entrée" : "Nouvelle sortie",
        montant: 0, frequence: "mensuel", decalage: 0,
      });
      rendre();
      var hote = document.getElementById(ajout === "in" ? "lignes-in" : "lignes-out");
      var champs = hote.querySelectorAll('input[data-champ="categorie"]');
      if (champs.length) { champs[champs.length - 1].focus(); champs[champs.length - 1].select(); }
    }
  });

  function rendreSansLignes() {
    var mois = calculer();
    var bas = mois[0];
    mois.forEach(function (m) { if (m.fin < bas.fin) bas = m; });
    var fin = mois[mois.length - 1];
    maj("kpi-bas", euros(bas.fin));
    maj("kpi-bas-note", "fin " + MOIS_LONGS[bas.mois] + " " + bas.annee);
    maj("kpi-fin", euros(fin.fin));
    maj("kpi-fin-note", "fin " + MOIS_LONGS[fin.mois] + " " + fin.annee);
    dessinerCourbe(mois, bas);
    dessinerBarres(mois);
    remplirTableau(mois);
    majTotauxFactures();
    sauver();
  }

  function majTotauxFactures() {
    ["in", "out"].forEach(function (sens) {
      var liste = etat.factures.filter(function (fa) { return fa.sens === sens && !fa.regle; });
      var total = liste.reduce(function (s, fa) { return s + fa.montant; }, 0);
      var el = document.getElementById(sens === "in" ? "total-in" : "total-out");
      if (el) el.textContent = liste.length === 0 ? "Rien en attente"
        : liste.length + (liste.length > 1 ? " factures" : " facture") + " — " + euros(total);
    });
  }

  // ───────────────────────────────────────────────── sauvegarde

  document.getElementById("treso-export").addEventListener("click", function () {
    telecharger(JSON.stringify(etat, null, 2), "pilotia-plan-tresorerie.json", "application/json");
  });

  document.getElementById("treso-csv").addEventListener("click", function () {
    var mois = calculer();
    var l = [];
    l.push("Plan de tresorerie - Pilotia");
    l.push("");
    var entete = ["Categorie"].concat(mois.map(function (m) { return MOIS_COURTS[m.mois] + " " + m.annee; }));
    l.push(entete.join(";"));
    function ajouter(nom, vals) { l.push([nom].concat(vals.map(function (v) { return Math.round(v); })).join(";")); }
    ajouter("Solde de debut", mois.map(function (m) { return m.debut; }));
    ajouter("Encaissements", mois.map(function (m) { return m.entrees; }));
    ajouter("Decaissements", mois.map(function (m) { return -m.sorties; }));
    ajouter("Variation", mois.map(function (m) { return m.variation; }));
    ajouter("Solde de fin", mois.map(function (m) { return m.fin; }));
    // BOM + point-virgule : ce qu'attend Excel en configuration francophone.
    telecharger("﻿" + l.join("\r\n") + "\r\n", "pilotia-plan-tresorerie.csv", "text/csv");
  });

  document.getElementById("treso-import").addEventListener("change", function (e) {
    var fichier = e.target.files && e.target.files[0];
    if (!fichier) return;
    var lecteur = new FileReader();
    lecteur.onload = function () {
      var msg = document.getElementById("treso-msg");
      try {
        var d = JSON.parse(lecteur.result);
        if (!d || d.version !== VERSION || !Array.isArray(d.lignes)) throw new Error("format");
        etat = d;
        prochainId = etat.lignes.reduce(function (m, l) { return Math.max(m, l.id); }, 0) + 1;
        rendre();
        msg.textContent = "Plan restauré.";
        msg.className = "form-msg-ok";
      } catch (err) {
        msg.textContent = "Ce fichier n'est pas un plan Pilotia valide.";
        msg.className = "form-msg-error";
      }
    };
    lecteur.readAsText(fichier);
    e.target.value = "";
  });

  document.getElementById("treso-reset").addEventListener("click", function () {
    if (!window.confirm("Effacer votre plan et repartir de l'exemple ? Cette action est définitive — pensez à exporter d'abord.")) return;
    try { localStorage.removeItem(CLE); } catch (e) {}
    etat = charger();
    prochainId = etat.lignes.reduce(function (m, l) { return Math.max(m, l.id); }, 0) + 1;
    synchroniserParametres();
    rendre();
  });

  function telecharger(contenu, nom, type) {
    var blob = new Blob([contenu], { type: type + ";charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = nom;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  }

  function synchroniserParametres() {
    document.getElementById("p-solde").value = etat.soldeDepart;
    document.getElementById("p-seuil").value = etat.seuil;
    document.getElementById("p-horizon").value = etat.horizon;
    document.getElementById("p-mois").value = etat.moisDepart;
  }

  synchroniserParametres();
  rendre();
})();
