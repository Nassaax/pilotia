/* Pilotis — animations légères (scroll reveal), sans dépendance.
   Basé sur les recommandations ui-ux-pro-max : opacity 0→1, y:12px, ~350ms ease-out,
   déclenché à l'entrée dans le viewport, désactivé sous prefers-reduced-motion. */
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
    el.classList.add("reveal");
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
