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
  fill(".js-info", function (n) {
    var a = CFG.infoEmail || CFG.orderEmail || "";
    n.textContent = a;
    if (n.tagName === "A") n.href = "mailto:" + a;
  });
  fill(".js-web", function (n) { n.textContent = CFG.web || ""; });
  fill(".js-street", function (n) { n.textContent = CFG.street || ""; });
  fill(".js-city", function (n) { n.textContent = CFG.city || ""; });
  fill(".js-address", function (n) {
    n.textContent = [CFG.street, CFG.city].filter(Boolean).join(", ");
  });
  fill(".js-ico", function (n) { n.textContent = CFG.ico || ""; });
  fill(".js-dic", function (n) { n.textContent = CFG.dic || ""; });
  fill(".js-icdph", function (n) { n.textContent = CFG.icDph || ""; });
  fill(".js-hours", function (n) { n.textContent = CFG.hours || ""; });
  fill(".js-year", function (n) { n.textContent = new Date().getFullYear(); });
  fill(".js-rights", function (n) {
    /* názov firmy končí bodkou v „s.r.o.“, druhú už nepridávame */
    var co = (CFG.company || "").replace(/\.$/, "");
    n.textContent = "© " + new Date().getFullYear() + " " + co + ". " + T.rights;
  });
  fill("[data-t-theme]", function (n) { n.title = T.theme; n.setAttribute("aria-label", T.theme); });

  /* ==========================================================================
     Spoločná kontrola formulárov. Používa ju košík, dopytové formuláre aj
     objednávkové okno, aby sa pravidlá aj hlášky nepísali trikrát.
     Druh kontroly sa odvodí z typu poľa (email, tel), alebo sa dá určiť
     atribútom data-check.
     ========================================================================== */
  var VT = {
    sk: { req: "Toto pole je povinné.",
          email: "Zadajte e-mail v tvare meno@domena.sk.",
          phone: "Zadajte telefónne číslo, aspoň 9 číslic.",
          zip: "PSČ má päť číslic, napríklad 014 01.",
          short: "Zadajte aspoň dva znaky." },
    cs: { req: "Toto pole je povinné.",
          email: "Zadejte e-mail ve tvaru jmeno@domena.cz.",
          phone: "Zadejte telefonní číslo, alespoň 9 číslic.",
          zip: "PSČ má pět číslic, například 014 01.",
          short: "Zadejte alespoň dva znaky." }
  }[LANG];

  function digits(v) { return (v || "").replace(/\D/g, ""); }

  function checkOne(node) {
    var v = (node.value || "").trim();
    var kind = node.getAttribute("data-check") ||
               (node.type === "email" ? "email" : node.type === "tel" ? "phone" : "");
    if (!v) return node.required ? VT.req : "";
    if (kind === "email" && !/^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/.test(v)) return VT.email;
    if (kind === "phone" && digits(v).length < 9) return VT.phone;
    if (kind === "zip" && digits(v).length !== 5) return VT.zip;
    if (kind === "name" && v.length < 2) return VT.short;
    return "";
  }

  /* Hlášku vypíšeme pod pole a zviažeme ju s ním pre čítačky obrazovky. */
  function mark(node, msg) {
    var box = node.closest("label") || node.parentNode;
    var e = box.querySelector(".err");
    node.classList.toggle("bad", !!msg);
    node.setAttribute("aria-invalid", msg ? "true" : "false");
    if (!msg) { if (e) e.remove(); node.removeAttribute("aria-describedby"); return; }
    if (!e) {
      e = document.createElement("span");
      e.className = "err";
      e.id = (node.id || "f" + Math.random().toString(36).slice(2)) + "-err";
      box.appendChild(e);
    }
    e.textContent = msg;
    node.setAttribute("aria-describedby", e.id);
  }

  window.RNCValid = {
    /* nodes — polia na kontrolu. Vráti true, keď je všetko v poriadku,
       inak označí chyby a presunie kurzor na prvé chybné pole. */
    run: function (nodes) {
      var first = null;
      nodes.forEach(function (n) {
        if (!n) return;
        var msg = checkOne(n);
        mark(n, msg);
        if (msg && !first) first = n;
      });
      if (first) first.focus();
      return !first;
    },
    /* kontrola počas písania odstráni hlášku hneď, ako je pole v poriadku */
    live: function (nodes) {
      nodes.forEach(function (n) {
        if (!n || n.dataset.liveOn) return;
        n.dataset.liveOn = "1";
        var h = function () { if (n.classList.contains("bad")) mark(n, checkOne(n)); };
        n.addEventListener("input", h);
        n.addEventListener("blur", function () { if ((n.value || "").trim()) mark(n, checkOne(n)); });
      });
    }
  };

  /* --- oznam o ukladaní v prehliadači ---
     Nežiadame súhlas: košík a režim zobrazenia sú nevyhnutné na fungovanie
     stránky, ktoré si návštevník vyžiadal. Lištu preto stačí raz zavrieť. --- */
  var cbar = el("cookieBar");
  if (cbar) {
    var CKEY = "rnc_notice_v1", seen = null;
    try { seen = localStorage.getItem(CKEY); } catch (e) { seen = "1"; }
    if (!seen) {
      cbar.hidden = false;
      /* trieda až po vykreslení, nech lišta prichádza plynulo */
      requestAnimationFrame(function () { cbar.classList.add("on"); });
      var ok = el("cookieOk");
      if (ok) ok.addEventListener("click", function () {
        cbar.classList.remove("on");
        try { localStorage.setItem(CKEY, "1"); } catch (e) {}
        setTimeout(function () { cbar.hidden = true; }, 250);
      });
    }
  }

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
