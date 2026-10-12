/* Format app (brand/format-app-CONCEPTION.md) : panneau « Plus », barre
   d'onglets masquée pendant la saisie, sections repliables sur téléphone et
   défilement vers un résultat de calcul. Chargé après animations.js sur
   toutes les pages. Sans JavaScript, la barre d'onglets fonctionne et tout
   le contenu reste ouvert. */
(function () {
  "use strict";

  var racine = document.documentElement;
  var modeApp = window.matchMedia("(max-width: 1080px)");
  var modeTelephone = window.matchMedia("(max-width: 760px)");
  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ───── Panneau « Plus » : un <dialog> natif, qui garde le focus et se
     ferme à la touche Échap sans code supplémentaire. */
  var bouton = document.getElementById("navToggle");
  var panneau = document.getElementById("panneauPlus");
  if (bouton && panneau && typeof panneau.showModal === "function") {
    bouton.addEventListener("click", function () {
      panneau.showModal();
      bouton.setAttribute("aria-expanded", "true");
    });
    panneau.addEventListener("close", function () {
      bouton.setAttribute("aria-expanded", "false");
      bouton.focus();
    });
    panneau.querySelector(".plus-fermer").addEventListener("click", function () {
      panneau.close();
    });
    // Un toucher sur le voile, hors du panneau, le ferme.
    panneau.addEventListener("click", function (e) {
      if (e.target !== panneau) return;
      var r = panneau.getBoundingClientRect();
      if (e.clientY < r.top || e.clientY > r.bottom || e.clientX < r.left || e.clientX > r.right) {
        panneau.close();
      }
    });
    // Le panneau n'existe qu'en mode app : s'il est ouvert quand l'écran
    // s'élargit, on le referme.
    modeApp.addEventListener("change", function (e) {
      if (!e.matches && panneau.open) panneau.close();
    });
  }

  /* ───── Barre d'onglets masquée pendant la saisie : le clavier du
     téléphone occupe déjà le bas de l'écran. */
  var CHAMPS = "input:not([type=checkbox]):not([type=radio]):not([type=button])" +
    ":not([type=submit]):not([type=reset]):not([type=range]):not([type=file])" +
    ":not([type=color]), select, textarea";
  function estChamp(n) { return !!(n && n.matches && n.matches(CHAMPS)); }
  document.addEventListener("focusin", function (e) {
    if (modeApp.matches && estChamp(e.target)) racine.classList.add("saisie");
  });
  document.addEventListener("focusout", function () {
    // Le focus passe parfois d'un champ à l'autre : on attend la cible suivante.
    setTimeout(function () {
      if (!estChamp(document.activeElement)) racine.classList.remove("saisie");
    }, 60);
  });

  /* ───── Défilement vers un résultat de calcul (appelé par les calculateurs). */
  function versResultat(cible) {
    var el = typeof cible === "string" ? document.getElementById(cible) : cible;
    if (!el || !modeApp.matches) return;
    el.scrollIntoView({ block: "nearest", behavior: mouvementReduit.matches ? "auto" : "smooth" });
  }
  window.PilotiaApp = { versResultat: versResultat };

  /* ───── Sections repliables (760 px ou moins).
     - [data-repli] : le premier h2 devient un bouton, ce qui le suit le corps ;
     - [data-replis-h2] : chaque h2 enfant direct ouvre un groupe repliable ;
     - [data-replis] : « Tout ouvrir / Tout fermer » dès deux replis.
     Groupes, corps et boutons n'existent que sur téléphone : au-delà de
     760 px, la page retrouve exactement son HTML d'origine. Le corps est
     masqué par hidden="until-found" quand le navigateur le connaît : la
     recherche dans la page peut alors l'ouvrir. */
  if (!document.querySelector("[data-repli], [data-replis-h2]")) return;

  var CACHE = "onbeforematch" in document.body ? "until-found" : "";
  var CHEVRON = '<svg class="repli-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" ' +
    'focusable="false"><path d="M6 9l6 6 6-6"/></svg>';
  var replis = [];
  var compteur = 0;
  function tous(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }
  // Retire des classes sans laisser d'attribut class="" vide derrière soi.
  function retirer(el) {
    el.classList.remove.apply(el.classList, Array.prototype.slice.call(arguments, 1));
    if (!el.className) el.removeAttribute("class");
  }

  function grouper() {
    tous("[data-replis-h2]").forEach(function (conteneur) {
      Array.prototype.slice.call(conteneur.children).forEach(function (enfant) {
        if (enfant.tagName !== "H2") return;
        var groupe = document.createElement("div");
        groupe.className = "repli-groupe";
        groupe.setAttribute("data-repli", "");
        conteneur.insertBefore(groupe, enfant);
        var n = enfant;
        do {
          var suivant = n.nextSibling;
          groupe.appendChild(n);
          n = suivant;
        } while (n && n.nodeName !== "H2");
      });
    });
  }

  function degrouper() {
    tous(".repli-groupe").forEach(function (groupe) {
      while (groupe.firstChild) groupe.parentNode.insertBefore(groupe.firstChild, groupe);
      groupe.parentNode.removeChild(groupe);
    });
  }

  function ouvrir(r) {
    r.corps.removeAttribute("hidden");
    r.item.classList.add("repli-ouvert");
    r.bouton.setAttribute("aria-expanded", "true");
    majTout();
  }
  function fermer(r) {
    r.corps.setAttribute("hidden", CACHE);
    r.item.classList.remove("repli-ouvert");
    r.bouton.setAttribute("aria-expanded", "false");
    majTout();
  }
  function estFerme(r) { return r.corps.hasAttribute("hidden"); }

  function envelopper(item) {
    var titre = item.querySelector("h2");
    if (!titre) return null;
    var r = { item: item, titre: titre, surtitre: null, place: null };
    r.corps = document.createElement("div");
    r.corps.className = "repli-corps";
    r.corps.id = "repli-corps-" + (++compteur);
    titre.parentNode.insertBefore(r.corps, titre.nextSibling);
    while (r.corps.nextSibling) r.corps.appendChild(r.corps.nextSibling);
    // Le sur-titre passe en tête du corps : il s'affiche à l'ouverture.
    var avant = titre.previousElementSibling;
    if (avant && avant.classList.contains("eyebrow")) {
      r.surtitre = avant;
      r.place = avant.nextSibling;
      r.corps.insertBefore(avant, r.corps.firstChild);
    }
    r.bouton = document.createElement("button");
    r.bouton.type = "button";
    r.bouton.className = "repli-bouton";
    r.bouton.setAttribute("aria-controls", r.corps.id);
    var texte = document.createElement("span");
    texte.className = "repli-texte";
    while (titre.firstChild) texte.appendChild(titre.firstChild);
    r.bouton.appendChild(texte);
    r.bouton.insertAdjacentHTML("beforeend", CHEVRON);
    titre.appendChild(r.bouton);
    titre.classList.add("repli-titre");
    r.bouton.addEventListener("click", function () {
      if (estFerme(r)) ouvrir(r); else fermer(r);
    });
    r.corps.addEventListener("beforematch", function () { ouvrir(r); });
    // Une section sombre devient une carte claire comme les autres.
    if (item.classList.contains("section-sombre")) {
      item.classList.remove("section-sombre");
      item.setAttribute("data-sombre", "");
    }
    item.classList.add("repli-actif");
    fermer(r);
    return r;
  }

  function desenvelopper(r) {
    var texte = r.bouton.firstChild;
    while (texte.firstChild) r.titre.insertBefore(texte.firstChild, r.bouton);
    r.titre.removeChild(r.bouton);
    retirer(r.titre, "repli-titre");
    if (r.surtitre) r.titre.parentNode.insertBefore(r.surtitre, r.place);
    while (r.corps.firstChild) r.corps.parentNode.insertBefore(r.corps.firstChild, r.corps);
    r.corps.parentNode.removeChild(r.corps);
    if (r.item.hasAttribute("data-sombre")) {
      r.item.classList.add("section-sombre");
      r.item.removeAttribute("data-sombre");
    }
    retirer(r.item, "repli-actif", "repli-ouvert");
  }

  function majTout() {
    tous(".replis-tout").forEach(function (b) {
      var siens = b.replisConcernes;
      var toutOuvert = siens.every(function (r) { return !estFerme(r); });
      b.textContent = toutOuvert ? "Tout fermer" : "Tout ouvrir";
    });
  }

  function ajouterBoutonsTout() {
    tous("[data-replis]").forEach(function (conteneur) {
      var siens = replis.filter(function (r) { return conteneur.contains(r.item); });
      if (siens.length < 2) return;
      var outils = document.createElement("div");
      outils.className = "replis-outils";
      var b = document.createElement("button");
      b.type = "button";
      b.className = "replis-tout";
      b.replisConcernes = siens;
      outils.appendChild(b);
      siens[0].item.parentNode.insertBefore(outils, siens[0].item);
      b.addEventListener("click", function () {
        var toutOuvert = siens.every(function (r) { return !estFerme(r); });
        siens.forEach(function (r) { if (toutOuvert) fermer(r); else ouvrir(r); });
      });
    });
    majTout();
  }

  function ouvrirCibleDuLien() {
    if (!location.hash) return;
    var cible = null;
    try { cible = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) {}
    if (!cible) return;
    var touche = false;
    replis.forEach(function (r) {
      if (r.item.contains(cible) || r.item === cible) { ouvrir(r); touche = true; }
    });
    if (touche) cible.scrollIntoView({ block: "start" });
  }

  function activer() {
    if (replis.length) return;
    grouper();
    replis = tous("[data-repli]").map(envelopper).filter(Boolean);
    ajouterBoutonsTout();
    ouvrirCibleDuLien();
  }

  function desactiver() {
    replis.forEach(desenvelopper);
    replis = [];
    tous(".replis-outils").forEach(function (o) { o.parentNode.removeChild(o); });
    degrouper();
  }

  function appliquer() { if (modeTelephone.matches) activer(); else desactiver(); }

  appliquer();
  modeTelephone.addEventListener("change", appliquer);
  window.addEventListener("hashchange", ouvrirCibleDuLien);
  // À l'impression, tout s'ouvre ; ensuite, chaque section retrouve son état.
  var fermesAvantImpression = null;
  window.addEventListener("beforeprint", function () {
    fermesAvantImpression = replis.filter(estFerme);
    replis.forEach(function (r) { r.corps.removeAttribute("hidden"); });
  });
  window.addEventListener("afterprint", function () {
    (fermesAvantImpression || []).forEach(function (r) {
      if (replis.indexOf(r) >= 0) r.corps.setAttribute("hidden", CACHE);
    });
    fermesAvantImpression = null;
  });
})();
