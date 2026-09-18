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
