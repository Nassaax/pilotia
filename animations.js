/* Pilotia — animations légères (scroll reveal), sans dépendance.
   Basé sur les recommandations ui-ux-pro-max : opacity 0→1, y:12px, ~350ms ease-out,
   déclenché à l'entrée dans le viewport, désactivé sous prefers-reduced-motion.
   L'état initial "caché" est posé par le script synchrone dans <head> (classe .js sur
   <html>, voir style.css) — pas ici — pour éviter un flash de contenu visible puis
   soudain masqué le temps que ce script (chargé en defer) s'exécute. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduceMotion || !("IntersectionObserver" in window)) {
    return; // le contenu est visible par défaut : rien à faire, aucune régression sans JS
  }

  var selectors = [
    ".card", ".path-card", ".step", ".faq details",
    "section .section-title"
  ];
  var els = document.querySelectorAll(selectors.join(","));
  if (!els.length) return;

  function delayFor(el) {
    var parent = el.parentElement;
    if (!parent) return 0;
    var siblings = Array.prototype.filter.call(parent.children, function (c) {
      return c === el || (c.matches && selectors.some(function (s) { return c.matches(s); }));
    });
    var index = siblings.indexOf(el);
    return Math.min(index, 5) * 70; // 70ms de stagger, plafonné pour rester perceptible
  }

  els.forEach(function (el) {
    el.style.transitionDelay = delayFor(el) + "ms";
  });

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );

  els.forEach(function (el) { observer.observe(el); });
})();

/* Menu mobile (hamburger) + menu déroulant "Découvrir" — navigation de base,
   ne dépend pas de prefers-reduced-motion (ce n'est pas une animation décorative). */
(function () {
  "use strict";

  var toggle = document.getElementById("navToggle");
  var navLinks = document.getElementById("navLinks");

  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      var open = navLinks.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var dropdowns = document.querySelectorAll(".dropdown");

  dropdowns.forEach(function (dropdown) {
    var trigger = dropdown.querySelector(".dropdown-trigger");
    if (!trigger) return;

    trigger.addEventListener("click", function () {
      var open = dropdown.classList.toggle("is-open");
      trigger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  document.addEventListener("click", function (e) {
    dropdowns.forEach(function (dropdown) {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("is-open");
        var trigger = dropdown.querySelector(".dropdown-trigger");
        if (trigger) trigger.setAttribute("aria-expanded", "false");
      }
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    dropdowns.forEach(function (dropdown) {
      dropdown.classList.remove("is-open");
      var trigger = dropdown.querySelector(".dropdown-trigger");
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    });
    if (navLinks && navLinks.classList.contains("is-open")) {
      navLinks.classList.remove("is-open");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    }
  });
})();

/* Téléchargements protégés par email (ressources.html, outils.html) — capture
   l'email via /api/subscribe (Brevo) puis déclenche le téléchargement réel
   du fichier. Un email déjà connu n'est jamais bloqué (upsert côté serveur). */
(function () {
  "use strict";

  var forms = document.querySelectorAll(".gated-download");
  if (!forms.length) return;

  forms.forEach(function (form) {
    var msg = form.querySelector(".gated-download-msg");
    var input = form.querySelector('input[type="email"]');
    var button = form.querySelector("button");
    var defaultLabel = button.textContent;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = input.value.trim();
      if (!email) return;

      button.disabled = true;
      button.textContent = "Envoi...";
      msg.textContent = "";

      fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, resource: form.getAttribute("data-resource") }),
      })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (data) {
            return { ok: r.ok, data: data };
          });
        })
        .then(function (result) {
          if (result.ok && result.data && result.data.ok) {
            var a = document.createElement("a");
            a.href = form.getAttribute("data-file");
            a.download = "";
            document.body.appendChild(a);
            a.click();
            a.remove();
            msg.textContent = "Merci ! Le téléchargement démarre.";
            input.value = "";
          } else {
            msg.textContent = (result.data && result.data.error) || "Une erreur est survenue, réessayez.";
          }
        })
        .catch(function () {
          msg.textContent = "Une erreur est survenue, réessayez.";
        })
        .finally(function () {
          button.disabled = false;
          button.textContent = defaultLabel;
        });
    });
  });
})();

/* Compteur animé sur les chiffres clés (statistiques.html) — désactivé sous
   prefers-reduced-motion : le chiffre final s'affiche directement, sans étape intermédiaire. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var nums = document.querySelectorAll(".stat-number[data-count]");
  if (!nums.length) return;

  if (reduceMotion || !("IntersectionObserver" in window)) {
    return; // le texte statique déjà présent dans le HTML reste affiché tel quel
  }

  function format(value, decimals) {
    return value.toLocaleString("fr-BE", {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  }

  function animate(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var decimals = el.getAttribute("data-count-decimals") ? parseInt(el.getAttribute("data-count-decimals"), 10) : 0;
    var prefix = el.getAttribute("data-count-prefix") || "";
    var suffix = el.getAttribute("data-count-suffix") || "";
    var duration = 1200;
    var start = null;

    function step(timestamp) {
      if (start === null) start = timestamp;
      var progress = Math.min((timestamp - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      var current = target * eased;
      el.textContent = prefix + format(current, decimals) + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = prefix + format(target, decimals) + suffix;
      }
    }

    requestAnimationFrame(step);
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animate(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );

  nums.forEach(function (el) { observer.observe(el); });
})();

/* Formulaire de contact (contact.html) — envoie le message via /api/contact
   (email transactionnel Brevo). Le consentement est requis côté client ET
   revérifié côté serveur : une validation uniquement front-end ne prouve rien. */
(function () {
  "use strict";

  var form = document.getElementById("contact-form");
  if (!form) return;

  var msg = document.getElementById("contact-msg");
  var button = document.getElementById("contact-submit");
  var defaultLabel = button.textContent;

  function show(text, isError) {
    msg.textContent = text;
    msg.className = isError ? "form-msg-error" : "form-msg-ok";
  }

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : "";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    var payload = {
      nom: val("nom"),
      email: val("email"),
      entreprise: val("entreprise"),
      profil: val("profil"),
      message: val("message"),
      consent: document.getElementById("consent").checked,
      website: val("website"),
    };

    // On renvoie le focus sur le premier champ fautif : sans cela, un utilisateur
    // au lecteur d'écran entend le message d'erreur sans savoir où corriger.
    if (!payload.nom) { show("Merci d'indiquer votre nom.", true); document.getElementById("nom").focus(); return; }
    if (!payload.email) { show("Merci d'indiquer votre email.", true); document.getElementById("email").focus(); return; }
    if (!payload.message) { show("Merci de décrire votre situation en quelques mots.", true); document.getElementById("message").focus(); return; }
    if (!payload.consent) { show("Merci d'accepter le traitement de votre message pour pouvoir l'envoyer.", true); document.getElementById("consent").focus(); return; }

    button.disabled = true;
    button.textContent = "Envoi en cours...";
    show("", false);

    fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (data) {
          return { ok: r.ok, data: data };
        });
      })
      .then(function (result) {
        if (result.ok && result.data && result.data.ok) {
          form.reset();
          show("Merci ! Votre message est parti, on vous répond sous 24 à 48 heures ouvrables.", false);
        } else {
          show((result.data && result.data.error) || "Une erreur est survenue, réessayez.", true);
        }
      })
      .catch(function () {
        show("Impossible d'envoyer le message pour le moment. Réessayez dans quelques minutes.", true);
      })
      .finally(function () {
        button.disabled = false;
        button.textContent = defaultLabel;
      });
  });
})();

/* Motion design du site (voir style.css, « Motion design sur le site ») :
   titres mot par mot, frise de la méthode, compteurs des calculateurs.
   Rien de tout cela ne tourne sous prefers-reduced-motion : les titres restent
   entiers, la frise pleine, les résultats s'affichent directement. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion || !("IntersectionObserver" in window)) return;

  /* Titres mot par mot. Le texte complet reste dans une copie sr-only ; les
     mots animés sont masqués aux lecteurs d'écran, qui liraient sinon un
     titre haché. Un élément enfant (<sup>, <span>…) reste un seul mot. */
  document.querySelectorAll("section .section-title").forEach(function (titre) {
    var visuel = document.createElement("span");
    visuel.setAttribute("aria-hidden", "true");
    var i = 0;
    function mot(contenu) {
      var s = document.createElement("span");
      s.className = "mot";
      s.style.setProperty("--i", Math.min(i++, 14));
      s.appendChild(contenu);
      visuel.appendChild(s);
    }
    Array.prototype.slice.call(titre.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/( +)/).forEach(function (bout) {
          if (!bout) return;
          if (/^ +$/.test(bout)) visuel.appendChild(document.createTextNode(" "));
          else mot(document.createTextNode(bout));
        });
      } else if (n.nodeName === "BR") {
        visuel.appendChild(n.cloneNode(true));
      } else if (n.nodeType === 1) {
        mot(n.cloneNode(true));
      }
    });
    var lu = document.createElement("span");
    lu.className = "sr-only";
    lu.textContent = titre.textContent.replace(/\s+/g, " ").trim();
    titre.textContent = "";
    titre.appendChild(lu);
    titre.appendChild(visuel);
    titre.classList.add("mots");
  });

  /* Frise de la méthode : le filet entre deux étapes se remplit à mesure que
     la ligne de lecture (60 % de la hauteur de l'écran) le parcourt. */
  document.querySelectorAll(".etapes").forEach(function (frise) {
    var etapes = frise.querySelectorAll(".step");
    var attente = false;
    function maj() {
      attente = false;
      var lecture = window.innerHeight * 0.6;
      etapes.forEach(function (etape, k) {
        var num = etape.querySelector(".step-num");
        var r = num.getBoundingClientRect();
        num.classList.toggle("atteinte", r.top + r.height / 2 <= lecture);
        if (k === etapes.length - 1) return;
        var debut = r.bottom;
        var fin = etapes[k + 1].querySelector(".step-num").getBoundingClientRect().top;
        var t = (lecture - debut) / Math.max(1, fin - debut);
        etape.style.setProperty("--trace", Math.max(0, Math.min(1, t)).toFixed(3));
      });
    }
    function demander() { if (!attente) { attente = true; requestAnimationFrame(maj); } }
    window.addEventListener("scroll", demander, { passive: true });
    window.addEventListener("resize", demander);
    maj();
  });

  /* Compteurs des calculateurs (éléments data-compteur). Le résultat défile
     jusqu'à sa valeur la première fois qu'il apparaît, puis à chaque
     changement isolé (un choix dans une liste, un bouton). Pendant la frappe,
     quand les changements se suivent à moins de 600 ms, la valeur s'affiche
     directement : un calculateur doit rester calme pendant la saisie. */
  var cibles = document.querySelectorAll("[data-compteur]");
  if (!cibles.length) return;

  var NOMBRE = /[−-]?\d{1,3}(?:[   ]\d{3})+(?:,\d+)?|[−-]?\d+(?:,\d+)?/;

  function noeudNombre(el) {
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false), n;
    while ((n = w.nextNode())) if (NOMBRE.test(n.nodeValue)) return n;
    return null;
  }
  function lire(txt) {
    var m = txt.match(NOMBRE);
    if (!m) return null;
    var brut = m[0], sep = (brut.match(/[   ]/) || [" "])[0];
    var dec = brut.indexOf(",") >= 0 ? brut.split(",")[1].length : 0;
    var val = parseFloat(brut.replace(/[   ]/g, "").replace(",", ".").replace("−", "-"));
    var moins = brut.charAt(0) === "−" ? "−" : "-";
    return { val: val, dec: dec, sep: sep, moins: moins, avant: txt.slice(0, m.index), apres: txt.slice(m.index + brut.length) };
  }
  function ecrire(f, v) {
    var abs = Math.abs(v).toFixed(f.dec).split(".");
    var ent = abs[0].replace(/\B(?=(\d{3})+(?!\d))/g, f.sep);
    var neg = v < 0 && Number(Math.abs(v).toFixed(f.dec)) !== 0;
    return f.avant + (neg ? f.moins : "") + ent + (f.dec ? "," + abs[1] : "") + f.apres;
  }

  var obs;
  function animer(el, de) {
    var n = noeudNombre(el);
    if (!n) return;
    var f = lire(n.nodeValue), t0 = null;
    if (!f || f.val === de) return;
    cancelAnimationFrame(el._anim);
    function pas(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min(1, (ts - t0) / 550), e = 1 - Math.pow(1 - p, 3);
      n.nodeValue = ecrire(f, p < 1 ? de + (f.val - de) * e : f.val);
      obs.takeRecords(); // nos propres écritures ne relancent pas d'animation
      if (p < 1) el._anim = requestAnimationFrame(pas);
    }
    el._anim = requestAnimationFrame(pas);
  }

  obs = new MutationObserver(function (records) {
    var vus = [];
    records.forEach(function (r) {
      var el = r.target.nodeType === 1 && r.target.hasAttribute("data-compteur") ? r.target : r.target.parentElement && r.target.parentElement.closest("[data-compteur]");
      if (el && vus.indexOf(el) < 0) vus.push(el);
    });
    var maintenant = performance.now();
    vus.forEach(function (el) {
      var n = noeudNombre(el), f = n && lire(n.nodeValue);
      var precedent = el._val;
      el._val = f ? f.val : null;
      var rafale = maintenant - (el._dernier || -1e9) < 600;
      el._dernier = maintenant;
      cancelAnimationFrame(el._anim);
      if (!el._vu || rafale || precedent == null || !f) return;
      animer(el, precedent);
    });
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      el._vu = true;
      io.unobserve(el);
      animer(el, 0);
    });
  }, { threshold: 0.6 });

  cibles.forEach(function (el) {
    var n = noeudNombre(el), f = n && lire(n.nodeValue);
    el._val = f ? f.val : null;
    obs.observe(el, { childList: true, characterData: true, subtree: true });
    io.observe(el);
  });
})();
