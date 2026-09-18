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
    ".hero .eyebrow", ".hero h1", ".hero .lead", ".hero .btn-row",
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

/* Bascule thème clair/sombre — préférence mémorisée dans localStorage, indépendante
   de prefers-color-scheme une fois que la personne a fait un choix explicite. L'état
   initial (avant ce script, chargé en defer) est déjà posé par le script synchrone
   dans <head> pour éviter un flash du mauvais thème au chargement. */
(function () {
  "use strict";

  var STORAGE_KEY = "pilotia-theme";
  var toggle = document.getElementById("themeToggle");
  if (!toggle) return;

  function currentTheme() {
    var explicit = document.documentElement.getAttribute("data-theme");
    if (explicit === "dark" || explicit === "light") return explicit;
    var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    return prefersDark ? "dark" : "light";
  }

  function syncToggleA11y(theme) {
    toggle.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    toggle.setAttribute("aria-label", theme === "dark" ? "Passer en mode clair" : "Passer en mode sombre");
  }

  // Au chargement : seulement synchroniser aria-pressed/aria-label sur le thème
  // effectif (explicite ou système). On n'écrit PAS dans localStorage ici — tant
  // que la personne n'a pas cliqué, le site continue de suivre prefers-color-scheme
  // même si celui-ci change entre deux visites.
  syncToggleA11y(currentTheme());

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    syncToggleA11y(theme);
    try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) {}
  }

  toggle.addEventListener("click", function () {
    applyTheme(currentTheme() === "dark" ? "light" : "dark");
    toggle.classList.remove("is-bouncing");
    void toggle.offsetWidth; // relance l'animation si l'utilisateur clique plusieurs fois de suite
    toggle.classList.add("is-bouncing");
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
