/* Connexion à l'espace client (connexion.html ; conception, § 3.2 et 3.7).
   Trois étapes sur une seule page : l'adresse email, le code reçu, puis
   « Bienvenue » à la création seulement. Le titre de la page suit l'étape et
   reçoit le focus ; les erreurs sont annoncées. */
(function () {
  "use strict";

  var C = window.PilotiaCompte;
  var titre = document.getElementById("connexion-titre");
  if (!C || !titre) return;

  function el(id) { return document.getElementById(id); }

  var etapes = { email: el("etape-email"), code: el("etape-code"), bienvenue: el("etape-bienvenue") };
  var enConnexion = /[?&]mode=connexion(&|$)/.test(location.search);
  var TITRES = {
    email: enConnexion ? "Me connecter" : "Créer mon espace",
    code: "Entrez votre code",
    bienvenue: "Votre espace est presque prêt"
  };
  var RENVOI = "Renvoyer le code";
  var email = "";
  var code = "";
  var minuterie = null;

  function montrer(nom, focus) {
    Object.keys(etapes).forEach(function (k) { etapes[k].hidden = k !== nom; });
    titre.textContent = TITRES[nom];
    document.title = TITRES[nom] + " | Pilotia";
    if (focus !== false) titre.focus();
  }

  function erreur(id, texte) { el(id).textContent = texte || ""; }

  function occuper(form, oui) {
    form.querySelector('button[type="submit"]').disabled = oui;
    if (oui) form.setAttribute("aria-busy", "true"); else form.removeAttribute("aria-busy");
  }

  function dateCourte(iso) {
    var d = new Date(iso);
    return isNaN(d) ? "" : d.toLocaleDateString("fr-BE", { day: "numeric", month: "long" });
  }

  function horsLigne(id) {
    return function () { erreur(id, "Pas de réseau pour le moment. Réessayez dans un instant."); };
  }

  // « Renvoyer le code » devient possible une minute après chaque envoi.
  function armerRenvoi() {
    var b = el("code-renvoyer");
    b.textContent = RENVOI;
    b.disabled = true;
    clearTimeout(minuterie);
    minuterie = setTimeout(function () { b.disabled = false; }, 60000);
  }

  function demanderCode(saisie, piege) {
    return C.api("POST", "/api/compte?action=demander-code", { email: saisie, website: piege || "" });
  }

  function verifier(corps) {
    return C.api("POST", "/api/compte?action=verifier-code", corps);
  }

  // Connexion réussie : l'appareil garde la marque de l'espace, puis Mon
  // espace fait la première synchronisation.
  function connecte(r) {
    var e = C.espace();
    if (e && e.compte && e.compte !== r.compte) {
      var ok = window.confirm("Les données d'un autre espace sont sur cet appareil. Elles y seront effacées ; elles restent dans leur espace.");
      if (!ok) {
        C.api("POST", "/api/compte?action=deconnexion", {}).then(function () {}, function () {});
        montrer("email");
        erreur("email-erreur", "Connexion annulée : les données de l'autre espace restent sur cet appareil.");
        return;
      }
      C.viderAppareil();
      e = null;
    }
    e = e || { fiche: {}, calculs: {}, sync: {} };
    e.compte = r.compte;
    e.prenom = r.prenom || "";
    e.expire = false;
    C.garder(e);
    C.annoncer(r.cree ? "cree" : "connecte");
    location.replace("mon-espace.html");
  }

  function preparerBienvenue() {
    var liste = el("bienvenue-liste");
    liste.textContent = "";
    function ligne(texte) {
      var li = document.createElement("li");
      li.textContent = texte;
      liste.appendChild(li);
    }
    var d = C.lire("pilotia-diagnostic");
    var p = C.lire("pilotia-tresorerie");
    if (d && typeof d.total === "number") {
      ligne("Diagnostic express" + (d.date && dateCourte(d.date) ? ", fait le " + dateCourte(d.date) : ""));
    }
    if (p && p.modifie) ligne("Plan de trésorerie");
    el("bienvenue-import").hidden = !liste.children.length;
  }

  etapes.email.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var saisie = el("connexion-email").value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(saisie)) {
      erreur("email-erreur", "Entrez une adresse email valide, par exemple nom@entreprise.be.");
      return;
    }
    erreur("email-erreur");
    occuper(etapes.email, true);
    demanderCode(saisie, el("connexion-site").value).then(function (r) {
      occuper(etapes.email, false);
      if (r.statut !== 200) {
        erreur("email-erreur", r.json.erreur || "Impossible d'envoyer le code. Réessayez dans un instant.");
        return;
      }
      email = saisie;
      el("code-adresse").textContent = email;
      el("connexion-code").value = "";
      erreur("code-erreur");
      montrer("code");
      armerRenvoi();
    }, function () { occuper(etapes.email, false); horsLigne("email-erreur")(); });
  });

  el("code-modifier").addEventListener("click", function () {
    montrer("email");
    el("connexion-email").focus();
  });

  el("code-renvoyer").addEventListener("click", function () {
    var bouton = this;
    bouton.disabled = true;
    demanderCode(email).then(function (r) {
      erreur("code-erreur", r.statut === 200 ? "Un nouveau code vient de partir." : (r.json.erreur || ""));
      el("connexion-code").value = "";
      armerRenvoi();
    }, function () { bouton.disabled = false; horsLigne("code-erreur")(); });
  });

  // Le champ n'accepte que des chiffres ; le sixième valide de lui-même.
  el("connexion-code").addEventListener("input", function () {
    var v = this.value.replace(/\D/g, "").slice(0, 6);
    if (v !== this.value) this.value = v;
    if (v.length === 6) {
      if (etapes.code.requestSubmit) etapes.code.requestSubmit();
      else etapes.code.dispatchEvent(new Event("submit", { cancelable: true }));
    }
  });

  etapes.code.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (etapes.code.getAttribute("aria-busy")) return;
    var saisie = el("connexion-code").value.replace(/\D/g, "");
    if (saisie.length !== 6) {
      erreur("code-erreur", "Entrez les 6 chiffres reçus par email.");
      return;
    }
    erreur("code-erreur");
    occuper(etapes.code, true);
    verifier({ email: email, code: saisie }).then(function (r) {
      occuper(etapes.code, false);
      if (r.statut === 200 && r.json.nouveau) {
        code = saisie;
        preparerBienvenue();
        montrer("bienvenue");
        return;
      }
      if (r.statut === 200 && r.json.connecte) { connecte(r.json); return; }
      erreur("code-erreur", r.json.erreur || "Ce code ne correspond pas.");
      if (r.statut === 410 || r.statut === 429) {
        // Code périmé ou épuisé : on propose tout de suite d'en recevoir un autre.
        clearTimeout(minuterie);
        el("code-renvoyer").textContent = "Recevoir un nouveau code";
        el("code-renvoyer").disabled = false;
      }
    }, function () { occuper(etapes.code, false); horsLigne("code-erreur")(); });
  });

  etapes.bienvenue.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (!el("bienvenue-conditions").checked) {
      erreur("bienvenue-erreur", "Cochez la case pour accepter les conditions d'utilisation.");
      el("bienvenue-conditions").focus();
      return;
    }
    erreur("bienvenue-erreur");
    occuper(etapes.bienvenue, true);
    verifier({ email: email, code: code, prenom: el("bienvenue-prenom").value.trim(), conditions: true }).then(function (r) {
      occuper(etapes.bienvenue, false);
      if (r.statut === 200 && r.json.connecte) { connecte(r.json); return; }
      erreur("bienvenue-erreur", r.json.erreur || "Impossible de créer votre espace. Réessayez.");
      if (r.statut === 410) {
        montrer("email", false);
        erreur("email-erreur", r.json.erreur);
        el("connexion-email").focus();
      }
    }, function () { occuper(etapes.bienvenue, false); horsLigne("bienvenue-erreur")(); });
  });

  // Au chargement : espace fermé, déjà connecté, ou première étape.
  C.etat().then(function (etat) {
    if (!etat.ouvert) {
      titre.textContent = "Mon espace";
      el("connexion-ferme").hidden = false;
      return;
    }
    if (etat.connecte) { location.replace("mon-espace.html"); return; }
    montrer("email", false);
  });
})();
