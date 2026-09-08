/* ==========================================================================
   Spoločné správanie všetkých stránok: hlavička, navigácia, pätička, režim.
   Katalóg samotný rieši assets/app.js (načítaný len na stránke produktov).
   ========================================================================== */
(function () {
  "use strict";
  var CFG  = window.SITE_CONFIG || {};
  var LANG = window.LANG === "cs" ? "cs" : "sk";

  var T = {
    sk: { menu: "Menu", close: "Zavrieť", theme: "Svetlý / tmavý režim",
          utilA: "Solárne panely pre vozidlá, karavany a outdoor",
          rights: "Všetky práva vyhradené.",
          ftrNav: "Navigácia", ftrContact: "Kontakt", ftrInfo: "Informácie",
          toTop: "Hore" },
    cs: { menu: "Menu", close: "Zavřít", theme: "Světlý / tmavý režim",
          utilA: "Solární panely pro vozidla, karavany a outdoor",
          rights: "Všechna práva vyhrazena.",
          ftrNav: "Navigace", ftrContact: "Kontakt", ftrInfo: "Informace",
          toTop: "Nahoru" }
  }[LANG];

  function el(id) { return document.getElementById(id); }
  function fill(sel, fn) {
    [].forEach.call(document.querySelectorAll(sel), fn);
  }

  /* --- údaje firmy z config.js --- */
  fill(".js-company", function (n) { n.textContent = CFG.company || ""; });
  /* logo nesie názov firmy ako prístupný popis */
  fill(".js-logo", function (n) { n.setAttribute("aria-label", CFG.company || ""); });
  fill(".js-phone", function (n) {
    n.textContent = CFG.phone || "";
    if (n.tagName === "A") n.href = "tel:" + String(CFG.phone || "").replace(/\s+/g, "");
  });
  fill(".js-mail", function (n) {
    n.textContent = CFG.orderEmail || "";
    if (n.tagName === "A") n.href = "mailto:" + (CFG.orderEmail || "");
  });
  fill(".js-web", function (n) { n.textContent = CFG.web || ""; });
  fill(".js-street", function (n) { n.textContent = CFG.street || ""; });
  fill(".js-city", function (n) { n.textContent = CFG.city || ""; });
  fill(".js-address", function (n) {
    n.textContent = [CFG.street, CFG.city].filter(Boolean).join(", ");
  });
  fill(".js-ico", function (n) { n.textContent = CFG.ico || ""; });
  fill(".js-dic", function (n) { n.textContent = CFG.dic || ""; });
  fill(".js-hours", function (n) { n.textContent = CFG.hours || ""; });
  fill(".js-year", function (n) { n.textContent = new Date().getFullYear(); });
  fill(".js-rights", function (n) {
    n.textContent = "© " + new Date().getFullYear() + " " + (CFG.company || "") + ". " + T.rights;
  });
  fill("[data-t-theme]", function (n) { n.title = T.theme; n.setAttribute("aria-label", T.theme); });

  /* --- filter rubrík na blogu ---
     Odkaz typu blog.html?rubrika=technika otvorí prehľad rovno vo filtri. --- */
  var bCats = el("blogCats"), bPosts = el("blogPosts");
  if (bCats && bPosts) {
    var chips = [].slice.call(bCats.querySelectorAll(".chip"));
    var cards = [].slice.call(bPosts.querySelectorAll(".post"));
    var apply = function (cat) {
      chips.forEach(function (c) {
        c.setAttribute("aria-pressed", String(c.getAttribute("data-cat") === cat));
      });
      cards.forEach(function (c) {
        c.hidden = !!cat && c.getAttribute("data-cat") !== cat;
      });
    };
    bCats.addEventListener("click", function (e) {
      var c = e.target.closest(".chip");
      if (!c) return;
      var cat = c.getAttribute("data-cat");
      apply(cat);
      var u = new URL(location.href);
      if (cat) u.searchParams.set("rubrika", cat); else u.searchParams.delete("rubrika");
      history.replaceState(null, "", u);
    });
    var want = new URLSearchParams(location.search).get("rubrika") || "";
    if (want && chips.some(function (c) { return c.getAttribute("data-cat") === want; }))
      apply(want);
  }

  /* --- mobilná navigácia --- */
  var burger = el("burger"), nav = el("nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    });
    /* zatvor po kliknutí na odkaz */
    nav.addEventListener("click", function (e) {
      if (!e.target.closest("a")) return;
      nav.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    });
  }

  /* --- rozbaľovacie menu produktov (klik aj klávesnica) --- */
  fill(".has-sub > button", function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      var li = b.parentNode, open = li.classList.toggle("open");
      b.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (e) {
    if (e.target.closest(".has-sub")) return;
    fill(".has-sub.open", function (li) {
      li.classList.remove("open");
      var b = li.querySelector("button"); if (b) b.setAttribute("aria-expanded", "false");
    });
  });

  /* --- svetlý / tmavý režim --- */
  var saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  var tb = el("themeBtn");
  if (tb) tb.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme");
    if (!cur) cur = matchMedia("(prefers-color-scheme:dark)").matches ? "dark" : "light";
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) {}
  });

  /* --- FAQ rozbaľovanie --- */
  fill(".faq-q", function (q) {
    q.addEventListener("click", function () {
      var open = q.parentNode.classList.toggle("open");
      q.setAttribute("aria-expanded", String(open));
    });
  });
})();
