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
