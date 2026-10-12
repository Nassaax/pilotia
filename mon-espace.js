/* Mon espace (mon-espace.html) : affiche ce que les outils ont enregistré
   sur cet appareil. Rien n'est envoyé : tout se lit dans le stockage local.
   Sans JavaScript ou sans résultat, la page montre ses trois points de départ. */
(function () {
  "use strict";

  var CLE_DIAG = "pilotia-diagnostic";
  var CLE_PLAN = "pilotia-tresorerie";
  var CLE_RESUME = "pilotia-tresorerie-resume";
  // Ordre de priorité en cas d'égalité (conception, § 4.2).
  var THEMES = ["Trésorerie & résilience", "Finances", "Personnel & organisation", "Présence digitale"];
  var CHEVRON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
    '<path d="m9 6 6 6-6 6"/></svg>';

  function lire(cle) {
    try {
      var brut = localStorage.getItem(cle);
      return brut ? JSON.parse(brut) : null;
    } catch (e) { return null; }
  }

  function themeLePlusFaible(themes) {
    var choix = null, min = Infinity;
    THEMES.forEach(function (t) {
      if (themes && typeof themes[t] === "number" && themes[t] < min) { min = themes[t]; choix = t; }
    });
    return choix;
  }

  function outilPour(theme, aUnPlan) {
    var sous = theme + " : votre thème le plus faible";
    if (theme === "Finances") return { href: "calculateur-marge.html", titre: "Calculer votre marge", sous: sous };
    if (theme === "Personnel & organisation") return { href: "calculateur-cout-salarie.html", titre: "Calculer le coût réel d'un salarié", sous: sous };
    if (theme === "Présence digitale") return { href: "generateur-calendrier-contenu.html", titre: "Générer votre calendrier de contenu", sous: sous };
    if (theme === "Trésorerie & résilience") {
      return aUnPlan
        ? { href: "calculateur-delai-encaissement.html", titre: "Mesurer votre délai d'encaissement", sous: sous }
        : { href: "plan-tresorerie.html", titre: "Créer votre plan de trésorerie", sous: sous };
    }
    return null;
  }

  function el(tag, classe, texte) {
    var e = document.createElement(tag);
    if (classe) e.className = classe;
    if (texte !== undefined) e.textContent = texte;
    return e;
  }

  function dateCourte(iso) {
    var d = new Date(iso);
    return isNaN(d) ? "" : d.toLocaleDateString("fr-BE", { day: "numeric", month: "long" });
  }

  function euros(n) {
    return Math.round(n).toLocaleString("fr-BE").replace(/[  ]/g, " ") + " €";
  }

  function afficherDiagnostic(d) {
    var carte = document.getElementById("carte-diagnostic");
    if (!d || typeof d.total !== "number") { carte.hidden = true; return false; }
    document.getElementById("diag-total").textContent = d.total;
    document.getElementById("diag-libelle").textContent = d.pill || "";
    var date = d.date ? dateCourte(d.date) : "";
    document.getElementById("diag-date").textContent = date ? "Fait le " + date : "";
    var liste = document.getElementById("diag-themes");
    liste.textContent = "";
    Object.keys(d.themes || {}).forEach(function (t) {
      var score = d.themes[t];
      var li = el("li");
      li.appendChild(el("span", "theme-nom", t));
      li.appendChild(el("span", "theme-score", score + "/4"));
      var jauge = el("span", "jauge");
      var barre = el("span");
      barre.style.width = Math.max(0, Math.min(100, score / 4 * 100)) + "%";
      jauge.appendChild(barre);
      li.appendChild(jauge);
      liste.appendChild(li);
    });
    carte.hidden = false;
    return true;
  }

  function afficherPlan(r) {
    var carte = document.getElementById("carte-tresorerie");
    if (!r || typeof r.montant !== "number") { carte.hidden = true; return false; }
    document.getElementById("plan-montant").textContent = euros(r.montant);
    document.getElementById("plan-mois").textContent = "fin " + r.mois + (r.annee ? " " + r.annee : "");
    var date = r.maj ? dateCourte(r.maj) : "";
    document.getElementById("plan-date").textContent = date ? "Mis à jour le " + date : "";
    carte.hidden = false;
    return true;
  }

  function ligne(item) {
    var li = el("li");
    var a = el("a", "ligne-app");
    a.href = item.href;
    var txt = el("span", "ligne-texte");
    txt.appendChild(el("span", "ligne-titre", item.titre));
    txt.appendChild(el("span", "ligne-sous", item.sous));
    a.appendChild(txt);
    a.insertAdjacentHTML("beforeend", CHEVRON);
    li.appendChild(a);
    return li;
  }

  function afficherProchainPas(d, aUnPlan) {
    var liste = document.getElementById("prochain-pas");
    liste.textContent = "";
    var premier = d
      ? outilPour(themeLePlusFaible(d.themes), aUnPlan)
      : { href: "diagnostic.html", titre: "Faire le diagnostic express", sous: "8 questions, 3 minutes" };
    if (premier) liste.appendChild(ligne(premier));
    liste.appendChild(ligne({ href: "contact.html", titre: "Parler de votre situation", sous: "Appel gratuit de 15 minutes" }));
  }

  function afficher() {
    var d = lire(CLE_DIAG);
    var aDiag = afficherDiagnostic(d);
    var aPlan = afficherPlan(lire(CLE_RESUME));
    var vide = !aDiag && !aPlan;
    document.getElementById("espace-vide").hidden = !vide;
    document.getElementById("espace-resultats").hidden = vide;
    if (!vide) afficherProchainPas(aDiag ? d : null, aPlan);
  }

  document.getElementById("espace-effacer").addEventListener("click", function () {
    if (!window.confirm("Effacer de cet appareil votre diagnostic et votre plan de trésorerie ? Cette action est définitive.")) return;
    [CLE_DIAG, CLE_PLAN, CLE_RESUME].forEach(function (c) {
      try { localStorage.removeItem(c); } catch (e) {}
    });
    afficher();
    document.getElementById("espace-titre").focus();
  });

  window.PilotiaMonEspace = { themeLePlusFaible: themeLePlusFaible, outilPour: outilPour };
  afficher();
})();
