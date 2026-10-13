/* Espace client, côté navigateur (brand/espace-client-CONCEPTION.md, § 3.7,
   4.1 et 4.3). Chargé sur Mon espace, la connexion, la fiche, le diagnostic,
   le rapport, le plan de trésorerie et les six calculateurs.

   Sans la clé « pilotia-espace » sur l'appareil, ce script ne fait aucune
   requête ; seules Mon espace et la connexion demandent si l'espace est
   ouvert. Les blocs suivants du fichier ajoutent la synchronisation. */
(function () {
  "use strict";

  var CLE = "pilotia-espace";
  var CLES_APPAREIL = ["pilotia-diagnostic", "pilotia-tresorerie", "pilotia-tresorerie-resume", CLE];

  // Le stockage local peut être plein ou interdit (navigation privée) : on
  // ne le laisse jamais casser la page.
  function lire(cle) {
    try {
      var brut = localStorage.getItem(cle);
      return brut ? JSON.parse(brut) : null;
    } catch (e) { return null; }
  }

  function ecrire(cle, valeur) {
    try { localStorage.setItem(cle, JSON.stringify(valeur)); return true; } catch (e) { return false; }
  }

  function retirer(cle) {
    try { localStorage.removeItem(cle); } catch (e) {}
  }

  function espace() { return lire(CLE); }

  function garder(e) { return ecrire(CLE, e); }

  // Un message à montrer une fois sur Mon espace, après un changement de page.
  function annoncer(code) {
    try { sessionStorage.setItem("pilotia-message", code); } catch (e) {}
  }

  function message() {
    try {
      var m = sessionStorage.getItem("pilotia-message");
      sessionStorage.removeItem("pilotia-message");
      return m;
    } catch (e) { return null; }
  }

  // Efface toutes les données Pilotia de l'appareil (déconnexion,
  // suppression, connexion fermée à distance).
  function viderAppareil(code) {
    CLES_APPAREIL.forEach(retirer);
    if (code) annoncer(code);
  }

  // Appel aux fonctions /api : rend toujours { statut, json }. Une panne de
  // réseau rejette la promesse.
  function api(methode, adresse, corps, options) {
    var init = { method: methode, credentials: "same-origin", headers: {} };
    if (corps !== undefined) {
      init.headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(corps);
    }
    if (options && options.keepalive) init.keepalive = true;
    return fetch(adresse, init).then(function (r) {
      return r.json().then(
        function (json) { return { statut: r.status, json: json || {} }; },
        function () { return { statut: r.status, json: {} }; });
    });
  }

  // L'espace est-il ouvert, et sommes-nous connectés ? Une seule demande par
  // page ; en cas de panne, l'espace est considéré comme fermé.
  var etatPromesse = null;
  function etat() {
    if (!etatPromesse) {
      etatPromesse = api("GET", "/api/compte?action=etat").then(
        function (r) { return r.statut === 200 && typeof r.json.ouvert === "boolean" ? r.json : { ouvert: false }; },
        function () { return { ouvert: false }; });
    }
    return etatPromesse;
  }

  window.PilotiaCompte = {
    CLE: CLE, lire: lire, ecrire: ecrire, retirer: retirer, espace: espace, garder: garder,
    annoncer: annoncer, message: message, viderAppareil: viderAppareil, api: api, etat: etat
  };
})();

/* ─── Synchronisation entre l'appareil et l'espace (conception, § 3.7 et 4.3).
   Pour chaque élément (fiche, diagnostic, plan, calculs), l'appareil garde la
   version de l'espace sur laquelle il s'appuie et l'empreinte de son contenu à
   ce moment-là. Un contenu qui ne correspond plus à cette empreinte est une
   modification à envoyer ; une version plus récente dans l'espace est à
   reprendre. Si les deux ont changé, le plus récent l'emporte, sauf pour le
   plan, où la personne choisit. */
(function () {
  "use strict";

  var C = window.PilotiaCompte;
  if (!C) return;

  var ELEMENTS = ["fiche", "diagnostic", "plan", "calculs"];
  // Pages rechargées quand l'espace apporte une version plus récente de ce
  // qu'elles affichent.
  var RECHARGER = { "plan-tresorerie.html": "plan", "rapport-diagnostic.html": "diagnostic" };
  var page = location.pathname.split("/").pop() || "index.html";
  var envois = {};
  var enAttente = {}; // éléments qui ne partent pas avant la page suivante
  var ferme = false; // interrupteur refermé : rien ne part avant la prochaine lecture
  var finPret;
  var pret = new Promise(function (ok) { finPret = ok; });

  // Texte d'une valeur aux clés triées : la base ne garde pas l'ordre des
  // clés, qui ne doit pas faire croire à une différence.
  function canonique(v) {
    if (Array.isArray(v)) return "[" + v.map(canonique).join(",") + "]";
    if (v && typeof v === "object") {
      return "{" + Object.keys(v).sort().map(function (k) {
        return JSON.stringify(k) + ":" + canonique(v[k]);
      }).join(",") + "}";
    }
    return v === undefined ? "null" : JSON.stringify(v);
  }

  // Empreinte courte d'un texte (cyrb53, domaine public).
  function empreinte(texte) {
    var h1 = 0xdeadbeef, h2 = 0x41c6ce57;
    for (var i = 0; i < texte.length; i++) {
      var ch = texte.charCodeAt(i);
      h1 = Math.imul(h1 ^ ch, 2654435761);
      h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
    return (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(36);
  }

  // Pour le plan, seul son état compte : son résumé est réécrit à chaque affichage.
  function signature(cle, valeur) {
    if (valeur === null || valeur === undefined) return "vide";
    return empreinte(canonique(cle === "plan" ? valeur.etat : valeur));
  }

  // La copie de l'appareil. Un plan jamais modifié (celui d'exemple) compte
  // comme absent.
  function local(cle, e) {
    if (cle === "diagnostic") return C.lire("pilotia-diagnostic");
    if (cle === "plan") {
      var etat = C.lire("pilotia-tresorerie");
      return etat && etat.modifie ? { etat: etat, resume: C.lire("pilotia-tresorerie-resume") } : null;
    }
    var v = e[cle];
    return v && typeof v === "object" && Object.keys(v).length ? v : null;
  }

  function appliquer(cle, valeur, e) {
    if (cle === "diagnostic") {
      if (valeur) C.ecrire("pilotia-diagnostic", valeur); else C.retirer("pilotia-diagnostic");
    } else if (cle === "plan") {
      if (valeur) {
        C.ecrire("pilotia-tresorerie", valeur.etat);
        if (valeur.resume) C.ecrire("pilotia-tresorerie-resume", valeur.resume);
        else C.retirer("pilotia-tresorerie-resume");
      } else {
        C.retirer("pilotia-tresorerie");
        C.retirer("pilotia-tresorerie-resume");
      }
    } else {
      e[cle] = valeur || {};
      if (cle === "fiche") e.prenom = (valeur && valeur.prenom) || "";
    }
  }

  function meta(e, cle) {
    e.sync = e.sync || {};
    return e.sync[cle] || { version: 0, empreinte: "vide" };
  }

  // L'appareil s'appuie désormais sur cette version de l'espace.
  function noter(e, cle, version, valeur) {
    e.sync = e.sync || {};
    e.sync[cle] = { version: version, empreinte: signature(cle, valeur) };
    if (e.erreurs) delete e.erreurs[cle];
  }

  // Prévient la page (Mon espace, calculateurs, plan) de ce qui a changé.
  function avertir(changes) {
    var ev;
    try { ev = new CustomEvent("pilotia-espace", { detail: { changes: changes } }); } catch (x) { return; }
    document.dispatchEvent(ev);
  }

  // Recharge la page une seule fois, même si l'espace change encore.
  function recharger() {
    try {
      var avant = Number(sessionStorage.getItem("pilotia-recharge")) || 0;
      if (Date.now() - avant < 10000) return false;
      sessionStorage.setItem("pilotia-recharge", String(Date.now()));
    } catch (x) { return false; }
    location.reload();
    return true;
  }

  // Connexion refusée : expirée, l'appareil garde tout et attend la
  // reconnexion ; fermée à distance ou espace supprimé, il efface tout.
  function refuser(raison) {
    if (raison === "fermee") {
      C.viderAppareil("fermee");
      avertir(["fermee"]);
      return;
    }
    var e = C.espace();
    if (e && !e.expire) {
      e.expire = true;
      C.garder(e);
    }
    avertir(["expire"]);
  }

  // Feuille de choix (maquette E3) sur une <dialog> modale : Échap annule,
  // le focus va au premier bouton.
  function feuille(options) {
    var d = document.createElement("dialog");
    d.className = "feuille" + (options.danger ? " feuille-danger" : "");
    d.setAttribute("aria-labelledby", "feuille-titre");
    var titre = document.createElement("h2");
    titre.id = "feuille-titre";
    titre.textContent = options.titre;
    d.appendChild(titre);
    (options.textes || []).forEach(function (texte) {
      var p = document.createElement("p");
      p.textContent = texte;
      d.appendChild(p);
    });
    options.boutons.forEach(function (b) {
      var bouton = document.createElement("button");
      bouton.type = "button";
      bouton.className = "btn " + (b.classe || "btn-secondary");
      bouton.textContent = b.libelle;
      bouton.addEventListener("click", function () {
        d.close();
        d.remove();
        if (b.action) b.action();
      });
      d.appendChild(bouton);
    });
    if (options.note) {
      var note = document.createElement("p");
      note.className = "feuille-note";
      note.textContent = options.note;
      d.appendChild(note);
    }
    d.addEventListener("cancel", function () {
      d.remove();
      if (options.annuler) options.annuler();
    });
    document.body.appendChild(d);
    d.showModal();
    d.querySelector("button").focus();
    return d;
  }

  // Feuille « Deux versions du plan » (§ 3.7). Échap ne tranche pas : le plan
  // reste en attente sur cet appareil, et la question revient à la prochaine
  // page ouverte.
  function demanderPlan(s) {
    if (enAttente.plan) return;
    enAttente.plan = true;
    var quand = new Date(s.maj);
    var heure = quand.getHours() + " h " + ("0" + quand.getMinutes()).slice(-2);
    var date = quand.toLocaleDateString("fr-BE", { day: "numeric", month: "long" });
    feuille({
      titre: "Votre plan a aussi changé sur un autre appareil",
      textes: ["Il a été modifié dans votre espace le " + date + " à " + heure +
        ", pendant que vous le modifiiez ici. Lequel garder ?"],
      boutons: [
        {
          libelle: "Garder celui de cet appareil", classe: "btn-primary",
          action: function () {
            var e = C.espace();
            delete enAttente.plan;
            if (!e) return;
            var m = meta(e, "plan");
            e.sync.plan = { version: s.version, empreinte: m.empreinte };
            C.garder(e);
            envoyer("plan");
          }
        },
        {
          libelle: "Reprendre celui de mon espace",
          action: function () {
            var e = C.espace();
            delete enAttente.plan;
            if (!e) return;
            appliquer("plan", s.valeur, e);
            noter(e, "plan", s.version, s.valeur);
            C.garder(e);
            avertir(["plan"]);
            if (page === "plan-tresorerie.html") location.reload();
          }
        }
      ],
      note: "La version écartée est remplacée. Pour garder les deux, exportez d'abord celle-ci (bouton en bas du plan)."
    });
  }

  // Les deux côtés ont changé depuis la dernière synchronisation.
  function resoudre(cle, l, s) {
    if (!s) return { action: "envoyer", base: 0 }; // effacé ailleurs, modifié ici : on le garde
    if (!l) return { action: "appliquer" }; // effacé ici, modifié ailleurs : rien ne se perd
    if (signature(cle, l) === signature(cle, s.valeur)) return { action: "noter" };
    if (cle === "diagnostic") {
      return Date.parse(l.date) > Date.parse(s.valeur.date) ? { action: "envoyer", base: s.version } : { action: "appliquer" };
    }
    if (cle === "calculs") {
      var fusion = {};
      [s.valeur, l].forEach(function (source) {
        Object.keys(source).forEach(function (outil) {
          if (!fusion[outil] || Date.parse(source[outil].maj) > Date.parse(fusion[outil].maj)) fusion[outil] = source[outil];
        });
      });
      return { action: "fusionner", valeur: fusion };
    }
    if (cle === "plan") return { action: "demander" };
    return { action: "appliquer" }; // la fiche : l'espace fait foi
  }

  function envoyer(cle, options) {
    if (envois[cle]) return envois[cle];
    var e = C.espace();
    if (ferme || enAttente[cle] || !e || e.expire) return Promise.resolve();
    var l = local(cle, e);
    var m = meta(e, cle);
    var sig = signature(cle, l);
    if (sig === m.empreinte || sig === m.refuse) return Promise.resolve();
    var envoi = C.api("PUT", "/api/donnees?cle=" + cle, { valeur: l, version: m.version }, options).then(function (r) {
      delete envois[cle];
      var e2 = C.espace();
      if (!e2) return;
      if (r.statut === 200) {
        // Ce qui est parti devient la référence ; une modification faite entre-temps
        // partira au prochain passage.
        if (cle === "fiche") appliquer("fiche", r.json.valeur, e2);
        noter(e2, cle, r.json.version, cle === "fiche" ? r.json.valeur : l);
        C.garder(e2);
        avertir(["enregistre"]);
      } else if (r.statut === 401) {
        refuser(r.json.raison);
      } else if (r.statut === 404) {
        ferme = true;
      } else if (r.statut === 409) {
        synchroniser();
      } else if (r.statut === 413) {
        // Trop volumineux : Mon espace le signale, et ce contenu ne repart pas.
        var m2 = meta(e2, cle);
        m2.refuse = sig;
        e2.sync[cle] = m2;
        e2.erreurs = e2.erreurs || {};
        e2.erreurs[cle] = "trop-grand";
        C.garder(e2);
        avertir(["erreur"]);
      }
    }, function () { delete envois[cle]; }); // pas de réseau : on réessaiera
    envois[cle] = envoi;
    return envoi;
  }

  function envoyerTout(options) {
    return Promise.all(ELEMENTS.map(function (cle) { return envoyer(cle, options); }));
  }

  function synchroniser() {
    var e = C.espace();
    if (!e || e.expire) return Promise.resolve();
    return C.api("GET", "/api/donnees").then(function (r) {
      ferme = r.statut === 404;
      if (r.statut === 401) { refuser(r.json.raison); return; }
      if (r.statut !== 200) return;
      var serveur = r.json.elements || {};
      e = C.espace();
      if (!e) return;
      var changes = [];
      ELEMENTS.forEach(function (cle) {
        var m = meta(e, cle);
        var s = serveur[cle] || null;
        var l = local(cle, e);
        var version = s ? s.version : 0;
        if (version === m.version) return; // rien de neuf dans l'espace
        if (signature(cle, l) === m.empreinte) {
          appliquer(cle, s && s.valeur, e);
          noter(e, cle, version, s && s.valeur);
          changes.push(cle);
          return;
        }
        var choix = resoudre(cle, l, s);
        if (choix.action === "appliquer") {
          appliquer(cle, s.valeur, e);
          noter(e, cle, version, s.valeur);
          changes.push(cle);
        } else if (choix.action === "noter") {
          noter(e, cle, version, s.valeur);
        } else if (choix.action === "fusionner") {
          appliquer(cle, choix.valeur, e);
          noter(e, cle, version, s.valeur);
          changes.push(cle);
        } else if (choix.action === "envoyer") {
          e.sync[cle] = { version: choix.base, empreinte: m.empreinte };
        } else if (choix.action === "demander") {
          demanderPlan(s);
        }
      });
      var garde = C.garder(e);
      if (changes.length) avertir(changes);
      var affiche = RECHARGER[page];
      if (affiche && changes.indexOf(affiche) !== -1) {
        if (garde && recharger()) return;
        // Sans rechargement (déjà rechargée il y a moins de 10 secondes, ou
        // stockage plein), l'écran garde l'ancienne version : rien de ce qu'on
        // y fait ne part avant la page suivante, qui le comparera à l'espace.
        enAttente[affiche] = true;
      }
      return envoyerTout();
    }, function () {});
  }

  C.pret = function () { return pret; };
  C.synchroniser = synchroniser;
  C.feuille = feuille;

  if (!C.espace()) {
    finPret();
    return;
  }
  synchroniser().then(finPret, finPret);
  setInterval(function () { if (document.visibilityState === "visible") envoyerTout(); }, 3000);
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible") synchroniser();
    else envoyerTout({ keepalive: true });
  });
  window.addEventListener("pagehide", function () { envoyerTout({ keepalive: true }); });
})();
