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
})();
