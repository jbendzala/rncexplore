/* ==========================================================================
   Katalóg solárnych panelov — logika (SK/CZ)
   Jazyk stránky určuje <html lang> resp. window.LANG ("sk" | "cs").
   ========================================================================== */
(function () {
  "use strict";

  var CFG  = window.SITE_CONFIG || {};
  var LANG = window.LANG === "cs" ? "cs" : "sk";
  var CUR  = LANG === "cs" ? "CZK" : "EUR";
  var META = window.CATALOG_META || { cats: [], brands: [], count: 0 };
  var ALL  = window.PRODUCTS || [];
  var PAGE = 48;

  /* ---------- preklady rozhrania ---------- */
  var T = {
    sk: {
      eyebrow: "Katalóg produktov",
      taglineHtml: "Solárna energia<br>pre <em>vozidlá</em> a karavany",
      catsTitle: "Kategórie",
      catsHint: "Kliknutím filtrujete katalóg",
      utilA: "Katalóg pre nezáväzný dopyt",
      ftrLangH: "Jazyk",
      tagline: "Solárne panely pre vozidlá, karavany a outdoor",
      heroLead: "Prezrite si celý sortiment. Vyberte produkt, vyplňte kontaktné údaje a my sa vám ozveme s cenovou ponukou a termínom dodania.",
      products: "produktov v katalógu", categories: "kategórií", brands: "značiek vozidiel",
      search: "Hľadať produkt, značku alebo model…",
      allCats: "Všetky kategórie", allBrands: "Všetky značky",
      sortDefault: "Predvolené poradie", sortWattUp: "Výkon: od najnižšieho", sortWattDown: "Výkon: od najvyššieho",
      sortPriceUp: "Cena: od najnižšej", sortPriceDown: "Cena: od najvyššej", sortName: "Názov A–Z",
      found: function (n) { return n + " " + plural(n, ["produkt", "produkty", "produktov"]); },
      reset: "Zrušiť filtre", loadMore: "Zobraziť ďalšie",
      noneTitle: "Nič sme nenašli", noneText: "Skúste iné hľadané slovo alebo zrušte filtre.",
      detail: "Detail", order: "Objednať", askPrice: "Cena na vyžiadanie", from: "od",
      close: "Zavrieť", noImg: "Bez fotografie",
      specs: "Parametre", power: "Výkon", voltage: "Napätie", current: "Prúd",
      weight: "Hmotnosť", code: "Kód produktu", category: "Kategória", brand: "Značka",
      variant: "Prevedenie", qty: "Počet kusov",
      orderTitle: "Nezáväzná objednávka",
      orderLead: "Vyplňte údaje a odošlite. Otvorí sa váš e-mailový klient s pripravenou správou — stačí ju odoslať.",
      name: "Meno a priezvisko", email: "E-mail", phone: "Telefón", company: "Firma / IČO",
      street: "Ulica a číslo", city: "Mesto", zip: "PSČ", country: "Krajina",
      msg: "Poznámka", msgPh: "Termín dodania, spôsob montáže, otázky…",
      optional: "nepovinné", send: "Odoslať objednávku", copy: "Skopírovať údaje",
      copied: "Údaje skopírované do schránky — vložte ich do e-mailu.",
      mailHint: "Ak sa e-mailový klient neotvorí, použite tlačidlo „Skopírovať údaje“ a pošlite nám ich na ",
      sentOk: "Otvorili sme váš e-mailový klient. Objednávka bude odoslaná až po jej potvrdení v e-maile.",
      subject: "Objednávka z katalógu", theme: "Svetlý / tmavý režim",
      priceNote: "Ceny sú orientačné vrátane DPH. Záväznú ponuku dostanete e-mailom.",
      contact: "Kontakt", info: "Informácie",
      infoText: "Katalóg slúži na prezeranie sortimentu. Objednávky vybavujeme individuálne e-mailom.",
      rights: "Všetky práva vyhradené.",
      langNote: "Katalóg produktov"
    },
    cs: {
      eyebrow: "Katalog produktů",
      taglineHtml: "Solární energie<br>pro <em>vozidla</em> a karavany",
      catsTitle: "Kategorie",
      catsHint: "Kliknutím filtrujete katalog",
      utilA: "Katalog pro nezávaznou poptávku",
      ftrLangH: "Jazyk",
      tagline: "Solární panely pro vozidla, karavany a outdoor",
      heroLead: "Prohlédněte si celý sortiment. Vyberte produkt, vyplňte kontaktní údaje a my se vám ozveme s cenovou nabídkou a termínem dodání.",
      products: "produktů v katalogu", categories: "kategorií", brands: "značek vozidel",
      search: "Hledat produkt, značku nebo model…",
      allCats: "Všechny kategorie", allBrands: "Všechny značky",
      sortDefault: "Výchozí pořadí", sortWattUp: "Výkon: od nejnižšího", sortWattDown: "Výkon: od nejvyššího",
      sortPriceUp: "Cena: od nejnižší", sortPriceDown: "Cena: od nejvyšší", sortName: "Název A–Z",
      found: function (n) { return n + " " + plural(n, ["produkt", "produkty", "produktů"]); },
      reset: "Zrušit filtry", loadMore: "Zobrazit další",
      noneTitle: "Nic jsme nenašli", noneText: "Zkuste jiné hledané slovo nebo zrušte filtry.",
      detail: "Detail", order: "Objednat", askPrice: "Cena na vyžádání", from: "od",
      close: "Zavřít", noImg: "Bez fotografie",
      specs: "Parametry", power: "Výkon", voltage: "Napětí", current: "Proud",
      weight: "Hmotnost", code: "Kód produktu", category: "Kategorie", brand: "Značka",
      variant: "Provedení", qty: "Počet kusů",
      orderTitle: "Nezávazná objednávka",
      orderLead: "Vyplňte údaje a odešlete. Otevře se váš e-mailový klient s připravenou zprávou — stačí ji odeslat.",
      name: "Jméno a příjmení", email: "E-mail", phone: "Telefon", company: "Firma / IČO",
      street: "Ulice a číslo", city: "Město", zip: "PSČ", country: "Země",
      msg: "Poznámka", msgPh: "Termín dodání, způsob montáže, dotazy…",
      optional: "nepovinné", send: "Odeslat objednávku", copy: "Zkopírovat údaje",
      copied: "Údaje zkopírovány do schránky — vložte je do e-mailu.",
      mailHint: "Pokud se e-mailový klient neotevře, použijte tlačítko „Zkopírovat údaje“ a pošlete nám je na ",
      sentOk: "Otevřeli jsme váš e-mailový klient. Objednávka bude odeslána až po jejím potvrzení v e-mailu.",
      subject: "Objednávka z katalogu", theme: "Světlý / tmavý režim",
      priceNote: "Ceny jsou orientační včetně DPH. Závaznou nabídku dostanete e-mailem.",
      contact: "Kontakt", info: "Informace",
      infoText: "Katalog slouží k prohlížení sortimentu. Objednávky vyřizujeme individuálně e-mailem.",
      rights: "Všechna práva vyhrazena.",
      langNote: "Katalog produktů"
    }
  }[LANG];

  /* slovenské/české skloňovanie počtu */
  function plural(n, f) { return n === 1 ? f[0] : (n >= 2 && n <= 4 ? f[1] : f[2]); }

  /* ---------- ceny ---------- */
  function convert(usd) {
    var rate = (CFG.rates && CFG.rates[CUR]) || 1;
    var v = usd * (CFG.markup || 1) * rate;
    if (CFG.rounding === "9") {
      v = Math.max(0, Math.round(v));
      /* zakončenie na 9 má zmysel až pri vyšších sumách */
      if (v >= 100) v = Math.floor(v / 10) * 10 + 9;
    } else if (CFG.rounding === "0") {
      v = Math.round(v);
    }
    return v;
  }
  function money(usd) { return fmt(convert(usd)); }
  /* naformátuje už prepočítanú sumu (aby 2 × 369 € bolo presne 738 €) */
  function fmt(v) {
    var dec = v < 20 ? 2 : 0;
    try {
      return new Intl.NumberFormat(LANG === "cs" ? "cs-CZ" : "sk-SK",
        { style: "currency", currency: CUR, minimumFractionDigits: dec, maximumFractionDigits: dec }).format(v);
    } catch (e) {
      return v.toFixed(dec) + " " + (CUR === "CZK" ? "Kč" : "€");
    }
  }

  /* ---------- pomôcky ---------- */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function el(id) { return document.getElementById(id); }
  function catName(k) {
    for (var i = 0; i < META.cats.length; i++) if (META.cats[i].k === k) return META.cats[i][LANG];
    return k;
  }
  /* Shopify CDN vie doručiť zmenšenú verziu — vložené dátové URI necháme tak */
  function imgUrl(src, w) {
    if (!src || src.indexOf("data:") === 0) return src;
    return src + (src.indexOf("?") === -1 ? "?" : "&") + "width=" + w;
  }
  function nameOf(p) { return p.n[LANG] || p.n.sk; }
  function descOf(p) { return p.d[LANG] || p.d.sk; }
  function varName(v) { return v[LANG] || v.sk; }

  /* diakritika-necitlivé hľadanie */
  function fold(s) {
    return String(s).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }
  ALL.forEach(function (p) {
    p._s = fold([nameOf(p), p.b || "", p.sku, catName(p.cat), p.w ? p.w + "w" : ""].join(" "));
  });

  /* ---------- stav ---------- */
  var S = { q: "", cat: "", brand: "", sort: "", shown: PAGE };

  function filtered() {
    var q = fold(S.q.trim());
    var terms = q ? q.split(/\s+/) : [];
    var out = ALL.filter(function (p) {
      if (S.cat && p.cat !== S.cat) return false;
      if (S.brand && p.b !== S.brand) return false;
      for (var i = 0; i < terms.length; i++) if (p._s.indexOf(terms[i]) === -1) return false;
      return true;
    });
    var s = S.sort;
    if (s === "w-") out.sort(function (a, b) { return (a.w || 0) - (b.w || 0); });
    else if (s === "w+") out.sort(function (a, b) { return (b.w || 0) - (a.w || 0); });
    else if (s === "p-") out.sort(function (a, b) { return a.usd - b.usd; });
    else if (s === "p+") out.sort(function (a, b) { return b.usd - a.usd; });
    else if (s === "n") out.sort(function (a, b) { return nameOf(a).localeCompare(nameOf(b), LANG); });
    return out;
  }

  /* ---------- vykreslenie kariet ---------- */
  function cardHTML(p) {
    var img = p.img && p.img[0];
    var off = p.was && CFG.showCompareAt ? Math.round((1 - p.usd / p.was) * 100) : 0;
    var specs = [];
    if (p.w) specs.push(p.w + " W");
    if (p.v) specs.push(p.v + " V");
    if (p.a) specs.push(p.a + " A");
    if (p.kg) specs.push(p.kg + " kg");

    return '<article class="card" data-id="' + esc(p.id) + '">' +
      '<div class="card-img" data-act="detail">' +
        (img ? '<img loading="lazy" decoding="async" src="' + esc(imgUrl(img, 600)) +
               '" alt="' + esc(nameOf(p)) + '">'
             : '<div class="ph">' + esc(T.noImg) + "</div>") +
        (off > 5 ? '<span class="badge">−' + off + "%</span>" : "") +
      "</div>" +
      '<div class="card-b">' +
        '<div class="card-cat">' + esc(catName(p.cat)) + "</div>" +
        '<h3 class="card-t" data-act="detail">' + esc(nameOf(p)) + "</h3>" +
        (specs.length ? '<div class="specs">' + specs.map(function (s) {
          return '<span class="spec">' + esc(s) + "</span>"; }).join("") + "</div>" : "") +
        '<div class="card-f">' + priceHTML(p) +
          '<button class="btn" data-act="order">' + esc(T.order) + "</button>" +
        "</div>" +
      "</div></article>";
  }

  function priceHTML(p) {
    if (CFG.showPrices === false) return '<div class="price"><span class="ask">' + esc(T.askPrice) + "</span></div>";
    var many = p.var && p.var.length > 1;
    var alt = CUR === "EUR" ? null : null;
    return '<div class="price">' +
      (p.was && CFG.showCompareAt ? "<s>" + esc(money(p.was)) + "</s>" : "") +
      "<b>" + (many ? esc(T.from) + " " : "") + esc(money(p.usd)) + "</b>" +
      "</div>";
  }

  function render(reset) {
    var list = filtered();
    if (reset) S.shown = PAGE;
    var grid = el("grid");
    var slice = list.slice(0, S.shown);

    grid.innerHTML = slice.length ? slice.map(cardHTML).join("")
      : '<div class="empty" style="grid-column:1/-1"><h3>' + esc(T.noneTitle) + "</h3><p>" +
        esc(T.noneText) + '</p><button class="btn ghost" id="reset2" style="margin-top:14px">' +
        esc(T.reset) + "</button></div>";

    el("count").textContent = T.found(list.length);
    el("more").innerHTML = list.length > S.shown
      ? '<button class="btn ghost" id="loadMore">' + esc(T.loadMore) + " (" +
        (list.length - S.shown) + ")</button>" : "";

    var r2 = el("reset2"); if (r2) r2.onclick = resetFilters;
    var lm = el("loadMore");
    if (lm) lm.onclick = function () { S.shown += PAGE; render(false); };
  }

  function resetFilters() {
    S.q = ""; S.cat = ""; S.brand = ""; S.sort = "";
    el("q").value = ""; el("brand").value = ""; el("sort").value = "";
    syncChips(); render(true);
  }
  function syncChips() {
    [].forEach.call(document.querySelectorAll(".chip"), function (c) {
      c.setAttribute("aria-pressed", String(c.dataset.cat === S.cat));
    });
    [].forEach.call(document.querySelectorAll(".tile"), function (t) {
      t.setAttribute("aria-pressed", String(t.dataset.cat === S.cat));
    });
  }

  /* dlaždice kategórií nad filtrom */
  function renderTiles() {
    el("tiles").innerHTML = META.cats.map(function (c) {
      return '<button type="button" class="tile" data-cat="' + esc(c.k) +
        '" aria-pressed="' + (S.cat === c.k) + '">' +
        '<span class="tile-t">' + esc(c[LANG]) + "</span>" +
        '<span class="tile-n">' + c.n + "</span></button>";
    }).join("");
  }

  /* ---------- detail produktu ---------- */
  var current = null;
  function openDetail(p) {
    current = p;
    var imgs = p.img && p.img.length ? p.img : [];
    var rows = [];
    if (p.w)  rows.push([T.power, p.w + " W"]);
    if (p.v)  rows.push([T.voltage, p.v + " V"]);
    if (p.a)  rows.push([T.current, p.a + " A"]);
    if (p.kg) rows.push([T.weight, p.kg + " kg"]);
    rows.push([T.category, catName(p.cat)]);
    if (p.b) rows.push([T.brand, p.b]);
    if (p.sku) rows.push([T.code, p.sku]);

    el("detailBody").innerHTML =
      '<div class="p-detail"><div class="p-media">' +
        '<div class="p-main">' + (imgs.length
          ? '<img id="pMain" src="' + esc(imgUrl(imgs[0], 1200)) + '" alt="' + esc(nameOf(p)) + '">'
          : '<div class="ph" style="display:grid;place-items:center;height:100%;color:var(--fg-3)">' + esc(T.noImg) + "</div>") +
        "</div>" +
        (imgs.length > 1 ? '<div class="p-thumbs">' + imgs.map(function (s, i) {
          return '<button data-src="' + esc(imgUrl(s, 1200)) + '" aria-current="' + (i === 0) +
                 '"><img src="' + esc(imgUrl(s, 160)) + '" alt=""></button>'; }).join("") + "</div>" : "") +
      "</div>" +
      '<div class="p-info">' +
        '<div class="card-cat">' + esc(catName(p.cat)) + "</div>" +
        "<h2>" + esc(nameOf(p)) + "</h2>" +
        '<p class="p-desc">' + esc(descOf(p)) + "</p>" +
        (CFG.showPrices === false
          ? '<div class="p-price"><b>' + esc(T.askPrice) + "</b></div>"
          : '<div class="p-price">' + (p.was && CFG.showCompareAt ? "<s>" + esc(money(p.was)) + "</s>" : "") +
            "<b>" + ((p.var && p.var.length > 1) ? esc(T.from) + " " : "") + esc(money(p.usd)) + "</b></div>") +
        '<table class="tbl">' + rows.map(function (r) {
          return "<tr><th>" + esc(r[0]) + "</th><td>" + esc(r[1]) + "</td></tr>"; }).join("") + "</table>" +
        '<button class="btn wide" id="toOrder">' + esc(T.order) + "</button>" +
        (CFG.showPrices === false ? "" : '<p class="note">' + esc(T.priceNote) + "</p>") +
      "</div></div>";

    [].forEach.call(document.querySelectorAll(".p-thumbs button"), function (b) {
      b.onclick = function () {
        el("pMain").src = b.dataset.src;
        [].forEach.call(document.querySelectorAll(".p-thumbs button"), function (x) {
          x.setAttribute("aria-current", String(x === b)); });
      };
    });
    el("toOrder").onclick = function () { closeModal("detailOv"); openOrder(p); };
    show("detailOv");
  }

  /* ---------- objednávkový formulár ---------- */
  function openOrder(p) {
    current = p;
    var vs = p.var && p.var.length ? p.var : [{ sk: "", cs: "", p: p.usd, sku: p.sku }];
    el("ofProd").innerHTML =
      (p.img && p.img[0] ? '<img src="' + esc(imgUrl(p.img[0], 160)) + '" alt="">' : "") +
      "<div><strong>" + esc(nameOf(p)) + "</strong><span>" +
      esc(p.sku || catName(p.cat)) + "</span></div>";

    var sel = el("ofVariant");
    sel.innerHTML = vs.map(function (v, i) {
      var label = varName(v) || nameOf(p);
      if (CFG.showPrices !== false) label += " — " + money(v.p);
      return '<option value="' + i + '">' + esc(label) + "</option>";
    }).join("");
    el("ofVariantWrap").style.display = vs.length > 1 ? "" : "none";
    el("ofMsgBox").innerHTML = esc(T.mailHint) + '<a href="mailto:' + esc(CFG.orderEmail) + '">' +
      esc(CFG.orderEmail) + "</a>";
    el("ofMsgBox").className = "msg";
    show("orderOv");
    setTimeout(function () { el("ofName").focus(); }, 60);
  }

  function buildOrder() {
    var p = current;
    var vs = p.var && p.var.length ? p.var : [{ sk: "", cs: "", p: p.usd, sku: p.sku }];
    var v = vs[parseInt(el("ofVariant").value, 10) || 0];
    var qty = Math.max(1, parseInt(el("ofQty").value, 10) || 1);
    var g = function (id) { return (el(id).value || "").trim(); };

    var L = LANG === "cs"
      ? { p: "PRODUKT", n: "Název", c: "Kód", var: "Provedení", q: "Počet kusů", pr: "Cena za kus",
          tot: "Celkem", z: "ZÁKAZNÍK", nm: "Jméno", em: "E-mail", ph: "Telefon", co: "Firma / IČO",
          ad: "ADRESA DORUČENÍ", no: "POZNÁMKA", src: "Odesláno z katalogu", ask: "na vyžádání" }
      : { p: "PRODUKT", n: "Názov", c: "Kód", var: "Prevedenie", q: "Počet kusov", pr: "Cena za kus",
          tot: "Spolu", z: "ZÁKAZNÍK", nm: "Meno", em: "E-mail", ph: "Telefón", co: "Firma / IČO",
          ad: "ADRESA DORUČENIA", no: "POZNÁMKA", src: "Odoslané z katalógu", ask: "na vyžiadanie" };

    var unit  = convert(v.p);
    var price = CFG.showPrices === false ? L.ask : fmt(unit);
    var total = CFG.showPrices === false ? L.ask : fmt(unit * qty);

    var lines = [
      L.p, "──────────────────────────────",
      L.n + ": " + nameOf(p),
      L.c + ": " + (v.sku || p.sku || "—"),
    ];
    if (vs.length > 1) lines.push(L.var + ": " + (varName(v) || "—"));
    lines.push(L.q + ": " + qty, L.pr + ": " + price, L.tot + ": " + total, "",
      L.z, "──────────────────────────────",
      L.nm + ": " + g("ofName"),
      L.em + ": " + g("ofEmail"),
      L.ph + ": " + g("ofPhone"));
    if (g("ofCompany")) lines.push(L.co + ": " + g("ofCompany"));
    lines.push("", L.ad, "──────────────────────────────",
      g("ofStreet"), g("ofZip") + " " + g("ofCity"), g("ofCountry"));
    if (g("ofNote")) lines.push("", L.no, "──────────────────────────────", g("ofNote"));
    lines.push("", "──────────────────────────────",
      L.src + ": " + location.origin + location.pathname);

    return {
      subject: T.subject + " — " + nameOf(p) + (qty > 1 ? " (" + qty + " ks)" : ""),
      body: lines.join("\n")
    };
  }

  function submitOrder(e) {
    e.preventDefault();
    var o = buildOrder();
    var href = "mailto:" + encodeURIComponent(CFG.orderEmail) +
      "?subject=" + encodeURIComponent(o.subject) + "&body=" + encodeURIComponent(o.body);
    if (href.length > 1800) href = href.slice(0, 1800);   // limit dĺžky mailto
    window.location.href = href;
    var box = el("ofMsgBox");
    box.className = "msg ok";
    box.textContent = T.sentOk;
  }

  function copyOrder() {
    var o = buildOrder();
    var text = o.subject + "\n\n" + o.body;
    var done = function () {
      var box = el("ofMsgBox"); box.className = "msg ok"; box.textContent = T.copied;
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text, done); });
    } else fallbackCopy(text, done);
  }
  function fallbackCopy(text, done) {
    var ta = document.createElement("textarea");
    ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  /* ---------- modálne okná ---------- */
  var lastFocus = null;
  function show(id) {
    lastFocus = document.activeElement;
    el(id).hidden = false;
    document.body.style.overflow = "hidden";
  }
  function closeModal(id) {
    el(id).hidden = true;
    if (!document.querySelector(".ov:not([hidden])")) document.body.style.overflow = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  /* ---------- štart ---------- */
  /* --- výber odporúčaných produktov na domovskú stránku --- */
  function renderFeatured() {
    var box = el("featured"); if (!box) return;
    var n = parseInt(box.dataset.count, 10) || 8;
    /* po jednom z hlavných druhov tovaru, nech je výber pestrý a reprezentatívny */
    var order = ["hood", "flexible", "rooftent", "foldable", "blanket",
                 "tonneau", "rv", "controller"];
    var disc = function (p) { return p.was ? 1 - p.usd / p.was : 0; };
    var pick = [], used = {};
    order.forEach(function (cat) {
      var best = ALL.filter(function (p) {
        return p.cat === cat && p.img.length && !used[p.id] && (p.w || p.a);
      }).sort(function (a, b) { return disc(b) - disc(a); })[0];
      if (best) { pick.push(best); used[best.id] = 1; }
    });
    /* ak by niektorá kategória chýbala, doplníme najvýhodnejšími panelmi */
    if (pick.length < n) {
      ALL.filter(function (p) { return p.img.length && p.w && !used[p.id]; })
         .sort(function (a, b) { return disc(b) - disc(a); })
         .slice(0, n - pick.length)
         .forEach(function (p) { pick.push(p); used[p.id] = 1; });
    }
    box.innerHTML = pick.slice(0, n).map(cardHTML).join("");
    box.addEventListener("click", function (e) {
      var t = e.target.closest("[data-act]"); if (!t) return;
      var id = t.closest(".card").dataset.id;
      var p = ALL.filter(function (x) { return x.id === id; })[0];
      if (!p) return;
      if (t.dataset.act === "order") openOrder(p); else openDetail(p);
    });
  }

  /* --- mozaika kategórií na domovskej stránke --- */
  var LS = "https://lensunsolar.com/cdn/shop/files/";
  var CAT_PHOTO = {
    hood:     LS + "LensunSolar-Hood-Solar-Panel-for-Toyota-4Runner.jpg?width=1200",
    flexible: LS + "LensunSolar-Flexible-Solar-Panel-Installed-on-the-Car-Roof.jpg?width=800",
    blanket:  LS + "LensunSolar-400W-Solar-Blanket.jpg?width=800",
    foldable: LS + "Lensun-200W-Foldable-Solar-Panel.jpg?width=800",
    rooftent: "https://cdn.shopify.com/s/files/1/0595/2156/4737/files/" +
              "lensun-400w-200w-flexible-solar-panel-roof-tent.jpg?width=800"
  };
  /* ak kategória nemá vlastnú fotografiu, vezmeme prvý produkt z nej */
  function catPhoto(k) {
    if (CAT_PHOTO[k]) return CAT_PHOTO[k];
    var p = ALL.filter(function (x) { return x.cat === k && x.img.length; })[0];
    return p ? imgUrl(p.img[0], 800) : "";
  }

  function renderMosaic() {
    var box = el("mosaic"); if (!box) return;
    var href = box.dataset.href || "produkty.html";
    box.innerHTML = META.cats.map(function (c) {
      var src = catPhoto(c.k);
      return '<a class="mos" href="' + esc(href) + "?cat=" + esc(c.k) + '">' +
        (src ? '<img loading="lazy" decoding="async" src="' + esc(src) +
               '" alt="' + esc(c[LANG]) + '">' : "") +
        '<span class="mos-t"><b>' + esc(c[LANG]) + "</b><span>" + c.n + "</span></span></a>";
    }).join("");
  }

  /* --- mriežka značiek vozidiel s logami --- */
  var BRAND_LOGO = {
    "Toyota":        "https://lensunsolar.com/cdn/shop/files/Toyota_535x.jpg",
    "Ford":          "https://lensunsolar.com/cdn/shop/files/Ford_535x.jpg",
    "Land Rover":    "https://lensunsolar.com/cdn/shop/files/LandRover_535x.jpg",
    "Mercedes-Benz": "https://lensunsolar.com/cdn/shop/files/Mercedes_Benz_535x.png",
    "Jeep":          "https://lensunsolar.com/cdn/shop/files/Jeep_535x.jpg"
  };
  /* logá uložené u nás — doplňte sem ďalšie súbory z priečinka assets/ */
  var BRAND_LOGO_LOCAL = {
    "Isuzu":      "Isuzu-logo.png",
    "Dacia":      "Dacia-logo.png",
    "Suzuki":     "Suzuki-Logo.wine.png",
    "Fiat":       "Fiat_logo.svg.webp",
    "Volkswagen": "Volkswagen_logo.png",
    "Ineos":      "INEOS_logo.svg.webp"
  };
  /* cesta k priečinku assets/ sa líši pre /cz/, odvodíme ju zo štýlov */
  function assetBase() {
    var l = document.querySelector('link[rel="stylesheet"][href*="assets/styles.css"]');
    return l ? l.getAttribute("href").replace(/styles\.css.*$/, "") : "assets/";
  }
  function brandLogo(name) {
    if (BRAND_LOGO_LOCAL[name]) return assetBase() + BRAND_LOGO_LOCAL[name];
    return BRAND_LOGO[name] || "";
  }

  function renderBrandGrid() {
    var box = el("brandGrid"); if (!box) return;
    var href = box.dataset.href || "produkty.html";
    box.innerHTML = META.brands.map(function (b) {
      var logo = brandLogo(b.k);
      /* vzdialené logá majú v obrázku veľa bieleho okraja, vlastné sú orezané
         na doraz — preto im dávame odlišnú maximálnu veľkosť */
      var cls = BRAND_LOGO_LOCAL[b.k] ? "logo-tight" : "logo-padded";
      var inner = logo
        ? '<img class="' + cls + '" loading="lazy" decoding="async" src="' + esc(logo) + '" alt="' + esc(b.k) + '">'
        /* pre značky bez loga použijeme čistý nápis v rovnakej dlaždici */
        : '<span class="brand-word">' + esc(b.k) + "</span>";
      return '<a class="brand-cell" href="' + esc(href) + "?brand=" +
        encodeURIComponent(b.k) + '" title="' + esc(b.k) + '">' +
        inner + '<span class="brand-n">' + b.n + "</span></a>";
    }).join("");
  }

  /* --- dlaždice kategórií (aj mimo katalógu, ako rozcestník) --- */
  function renderTilesInto(box, asLinks) {
    box.innerHTML = META.cats.map(function (c) {
      if (asLinks) {
        return '<a class="tile" href="' + esc(box.dataset.href || "produkty.html") + "?cat=" + esc(c.k) + '">' +
          '<span class="tile-t">' + esc(c[LANG]) + "</span>" +
          '<span class="tile-n">' + c.n + "</span></a>";
      }
      return '<button type="button" class="tile" data-cat="' + esc(c.k) +
        '" aria-pressed="' + (S.cat === c.k) + '">' +
        '<span class="tile-t">' + esc(c[LANG]) + "</span>" +
        '<span class="tile-n">' + c.n + "</span></button>";
    }).join("");
  }

  function init() {
    /* rozcestníky na domovskej stránke */
    var linkTiles = el("catTiles");
    if (linkTiles) renderTilesInto(linkTiles, true);
    renderMosaic();
    renderBrandGrid();

    /* objednávkový formulár je na každej stránke, kde je katalóg alebo výber */
    if (el("orderForm")) initOrderForm();

    /* odporúčané produkty */
    renderFeatured();

    /* štatistiky v hero pruhu (domovská stránka aj katalóg) */
    if (el("statA")) {
      el("statA").innerHTML = "<b>" + META.count + "</b><span>" + esc(T.products) + "</span>";
      el("statB").innerHTML = "<b>" + META.cats.length + "</b><span>" + esc(T.categories) + "</span>";
      el("statC").innerHTML = "<b>" + META.brands.length + "</b><span>" + esc(T.brands) + "</span>";
    }

    /* ďalej už len plný katalóg */
    if (!el("grid")) return;

    el("q").placeholder = T.search;
    el("resetBtn").textContent = T.reset;
    if (el("tiles")) renderTilesInto(el("tiles"), false);

    el("chips").innerHTML = '<button class="chip" data-cat="" aria-pressed="true">' +
      esc(T.allCats) + "<b>" + META.count + "</b></button>" +
      META.cats.map(function (c) {
        return '<button class="chip" data-cat="' + esc(c.k) + '" aria-pressed="false">' +
          esc(c[LANG]) + "<b>" + c.n + "</b></button>"; }).join("");

    el("brand").innerHTML = '<option value="">' + esc(T.allBrands) + "</option>" +
      META.brands.map(function (b) {
        return '<option value="' + esc(b.k) + '">' + esc(b.k) + " (" + b.n + ")</option>"; }).join("");

    el("sort").innerHTML = [["", T.sortDefault], ["p-", T.sortPriceUp], ["p+", T.sortPriceDown],
      ["w+", T.sortWattDown], ["w-", T.sortWattUp], ["n", T.sortName]]
      .map(function (o) { return '<option value="' + o[0] + '">' + esc(o[1]) + "</option>"; }).join("");

    /* kategória z adresy: produkty.html?cat=hood */
    var qs = /[?&]cat=([a-z]+)/.exec(location.search);
    if (qs && META.cats.some(function (c) { return c.k === qs[1]; })) S.cat = qs[1];
    var qq = /[?&]q=([^&]*)/.exec(location.search);
    if (qq) { S.q = decodeURIComponent(qq[1].replace(/\+/g, " ")); el("q").value = S.q; }
    var qb = /[?&]brand=([^&]*)/.exec(location.search);
    if (qb) {
      var want = decodeURIComponent(qb[1].replace(/\+/g, " "));
      if (META.brands.some(function (b) { return b.k === want; })) {
        S.brand = want; el("brand").value = want;
      }
    }
    syncChips();

    var deb;
    el("q").addEventListener("input", function (e) {
      clearTimeout(deb); var v = e.target.value;
      deb = setTimeout(function () { S.q = v; render(true); }, 160);
    });
    el("chips").addEventListener("click", function (e) {
      var c = e.target.closest(".chip"); if (!c) return;
      S.cat = c.dataset.cat; syncChips(); render(true);
      window.scrollTo({ top: el("catalog").offsetTop - 90, behavior: "smooth" });
    });
    if (el("tiles")) el("tiles").addEventListener("click", function (e) {
      var t = e.target.closest(".tile"); if (!t) return;
      S.cat = (S.cat === t.dataset.cat) ? "" : t.dataset.cat;
      syncChips(); render(true);
      window.scrollTo({ top: el("catalog").offsetTop - 90, behavior: "smooth" });
    });
    el("brand").addEventListener("change", function (e) { S.brand = e.target.value; render(true); });
    el("sort").addEventListener("change", function (e) { S.sort = e.target.value; render(true); });
    el("resetBtn").addEventListener("click", resetFilters);

    el("grid").addEventListener("click", function (e) {
      var t = e.target.closest("[data-act]"); if (!t) return;
      var p = ALL.filter(function (x) { return x.id === t.closest(".card").dataset.id; })[0];
      if (!p) return;
      if (t.dataset.act === "order") openOrder(p); else openDetail(p);
    });

    render(true);
  }

  /* --- objednávkový formulár (spoločný pre katalóg aj domovskú stránku) --- */
  function initOrderForm() {
    var F = [["ofName", T.name, 1], ["ofEmail", T.email, 1], ["ofPhone", T.phone, 1],
             ["ofCompany", T.company, 0], ["ofStreet", T.street, 1], ["ofCity", T.city, 1],
             ["ofZip", T.zip, 1], ["ofCountry", T.country, 0]];
    F.forEach(function (f) {
      var lb = el(f[0]).closest("label");
      lb.querySelector("span").innerHTML = esc(f[1]) +
        (f[2] ? ' <em class="req">*</em>' : ' <em class="opt">(' + esc(T.optional) + ")</em>");
      if (f[2]) el(f[0]).required = true;
    });
    el("ofCountry").value = LANG === "cs" ? "Česká republika" : "Slovensko";
    el("lbVariant").textContent = T.variant;
    el("lbQty").textContent = T.qty;
    el("lbNote").textContent = T.msg;
    el("ofNote").placeholder = T.msgPh;
    el("orderTitle").textContent = T.orderTitle;
    el("orderLead").textContent = T.orderLead;
    el("btnSend").textContent = T.send;
    el("btnCopy").textContent = T.copy;

    [].forEach.call(document.querySelectorAll("[data-close]"), function (b) {
      b.addEventListener("click", function () { closeModal(b.dataset.close); });
    });
    [].forEach.call(document.querySelectorAll(".ov"), function (o) {
      o.addEventListener("click", function (e) { if (e.target === o) closeModal(o.id); });
    });
    if (!window.__escBound) {
      window.__escBound = true;
      document.addEventListener("keydown", function (e) {
        if (e.key !== "Escape") return;
        var open = document.querySelector(".ov:not([hidden])");
        if (open) closeModal(open.id);
      });
    }
    el("orderForm").addEventListener("submit", submitOrder);
    el("btnCopy").addEventListener("click", copyOrder);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
