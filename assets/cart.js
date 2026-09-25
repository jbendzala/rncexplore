/* ==========================================================================
   Košík bez servera. Obsah sa drží v prehliadači (localStorage), objednávka
   odchádza e-mailom. Položka si nesie vlastnú kópiu údajov, takže stránka
   košíka nepotrebuje načítať celý katalóg.
   ========================================================================== */
(function () {
  "use strict";
  var KEY = "rnc_cart_v1";
  var CFG = window.SITE_CONFIG || {};
  var LANG = window.LANG === "cs" ? "cs" : "sk";
  var CUR = LANG === "cs" ? "CZK" : "EUR";

  var T = {
    sk: { added: "Pridané do košíka", cart: "Košík", empty: "Košík je prázdny",
          emptyNote: "Vyberte produkty v katalógu a pridajte ich do košíka.",
          toCatalog: "Prejsť do katalógu", item: "Položka", variant: "Prevedenie",
          qty: "Počet", unit: "Cena za kus", sum: "Spolu", remove: "Odstrániť",
          total: "Celkom s DPH", goods: "Tovar", shipping: "Doprava",
          dlvCourier: "Doručenie kuriérom", dlvPickup: "Osobný odber v Bytči",
          shipFree: "v cene", free: "bez príplatku",
          vatNote: "Ceny tovaru sú vrátane 23 % DPH. Doprava je jednou sumou za celú objednávku, osobný odber bez príplatku.",
          contact: "Doručovacie a fakturačné údaje",
          order: "Objednávka zaväzujúca k platbe",
          sent: "Objednávka odoslaná. Obratom vám pošleme faktúru s QR kódom na zaplatenie.",
          sending: "Odosielam objednávku…",
          mailFallback: "Objednávku sa nepodarilo odoslať automaticky, preto sme otvorili váš e-mailový klient. Správu už len odošlite.",
          needsActivation: "Formulár ešte nie je aktivovaný. V schránke, kam sa objednávky doručujú, nájdete e-mail od formsubmit.co — kliknite v ňom na Activate Form. Objednávka sa zatiaľ odosiela e-mailovým klientom.",
          thanks: "Ďakujeme za objednávku",
          thanksNote: "Potvrdenie objednávky a faktúru s QR kódom vám pošleme e-mailom z adresy objednavky@rncexplore.com.",
          hint: "Ak sa e-mailový klient neotvorí, skopírujte objednávku a pošlite nám ju na ",
          terms: "Odoslaním objednávky potvrdzujete, že ste sa oboznámili s obchodnými podmienkami a že objednávka je spojená s povinnosťou platby.",
          need: "Vyplňte prosím povinné údaje označené hviezdičkou." },
    cs: { added: "Přidáno do košíku", cart: "Košík", empty: "Košík je prázdný",
          emptyNote: "Vyberte produkty v katalogu a přidejte je do košíku.",
          toCatalog: "Přejít do katalogu", item: "Položka", variant: "Provedení",
          qty: "Počet", unit: "Cena za kus", sum: "Celkem", remove: "Odstranit",
          total: "Celkem s DPH", goods: "Zboží", shipping: "Doprava",
          dlvCourier: "Doručení kurýrem", dlvPickup: "Osobní odběr v Bytči",
          shipFree: "v ceně", free: "bez příplatku",
          vatNote: "Ceny zboží jsou včetně 23 % DPH. Doprava je jednou částkou za celou objednávku, osobní odběr bez příplatku.",
          contact: "Doručovací a fakturační údaje",
          order: "Objednávka zavazující k platbě",
          sent: "Objednávka odeslána. Obratem vám pošleme fakturu s QR kódem k zaplacení.",
          sending: "Odesílám objednávku…",
          mailFallback: "Objednávku se nepodařilo odeslat automaticky, proto jsme otevřeli váš e-mailový klient. Zprávu už jen odešlete.",
          needsActivation: "Formulář ještě není aktivovaný. Ve schránce, kam se objednávky doručují, najdete e-mail od formsubmit.co — klikněte v něm na Activate Form. Objednávka se zatím odesílá e-mailovým klientem.",
          thanks: "Děkujeme za objednávku",
          thanksNote: "Potvrzení objednávky a fakturu s QR kódem vám pošleme e-mailem z adresy objednavky@rncexplore.com.",
          hint: "Pokud se e-mailový klient neotevře, zkopírujte objednávku a pošlete nám ji na ",
          terms: "Odesláním objednávky potvrzujete, že jste se seznámili s obchodními podmínkami a že objednávka je spojena s povinností platby.",
          need: "Vyplňte prosím povinné údaje označené hvězdičkou." }
  }[LANG];

  /* Kam službа objednávku doručí. Zákazník vidí vždy CFG.orderEmail,
     doručovacia adresa sa dá prepnúť v config.js cez deliverTo. */
  function deliveryEmail() { return CFG.deliverTo || CFG.orderEmail; }

  /* ---------- ceny ---------- */
  /* Doprava do ceny produktu nevstupuje, účtuje sa raz za objednávku až
     v košíku. Prepínač shippingInPrice zostáva, keby sa to malo zmeniť. */
  function shipNet() {
    return (CFG.shippingGross && CFG.shippingGross[CUR]) || 0;
  }
  function convert(usd) {
    var rate = (CFG.rates && CFG.rates[CUR]) || 1;
    var base = usd * (CFG.markup || 1) * rate;
    if (CFG.shippingInPrice) base += shipNet();
    var v = base * (1 + (CFG.vat || 0));
    if (CFG.rounding === "half") {
      /* nadol na celé a +0,50; v korunách sa halierniky nepoužívajú */
      return Math.floor(v) + (CUR === "CZK" ? 0 : 0.5);
    }
    if (CFG.rounding === "9") { v = Math.max(0, Math.round(v)); if (v >= 100) v = Math.floor(v / 10) * 10 + 9; }
    else if (CFG.rounding === "0") { v = Math.round(v); }
    return v;
  }
  function fmt(v) {
    /* celé sumy bez halierov, nezaokrúhlené (doprava, súčet) s nimi —
       aby sa zobrazená suma presne rovnala tej na faktúre */
    var dec = (v < 20 || Math.abs(v - Math.round(v)) > 0.005) ? 2 : 0;
    try {
      return new Intl.NumberFormat(LANG === "cs" ? "cs-CZ" : "sk-SK",
        { style: "currency", currency: CUR, minimumFractionDigits: dec, maximumFractionDigits: dec }).format(v);
    } catch (e) { return v.toFixed(dec) + (CUR === "CZK" ? " Kč" : " €"); }
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function el(id) { return document.getElementById(id); }

  /* ---------- stav ---------- */
  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function write(c) {
    try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {}
    badge();
  }
  function count() {
    return read().reduce(function (n, i) { return n + i.qty; }, 0);
  }
  function badge() {
    var n = count();
    [].forEach.call(document.querySelectorAll(".cart-n"), function (b) {
      b.textContent = n; b.hidden = n === 0;
    });
  }

  function add(item) {
    var c = read();
    var hit = c.filter(function (i) { return i.id === item.id && i.vi === item.vi; })[0];
    if (hit) hit.qty += item.qty; else c.push(item);
    write(c);
    toast(T.added);
  }

  var tEl;
  function toast(msg) {
    if (!tEl) {
      tEl = document.createElement("div"); tEl.className = "toast"; document.body.appendChild(tEl);
    }
    tEl.textContent = msg; tEl.classList.add("on");
    clearTimeout(tEl._t); tEl._t = setTimeout(function () { tEl.classList.remove("on"); }, 2200);
  }

  /* ---------- stránka košíka ---------- */
  /* Doprava je paušál za objednávku, nie za kus. Do košíka ju pripočítame
     s DPH, aby súčet zodpovedal tomu, čo zákazník naozaj zaplatí. */
  var pickup = false;                 /* zvolil zákazník osobný odber? */

  /* Paušál za doručenie, suma je už s DPH — jeden balík alebo desať,
     platí sa raz. */
  function shipCost() {
    return (CFG.shippingGross && CFG.shippingGross[CUR]) || 0;
  }

  /* Osobný odber je bez príplatku, zákazník si tovar vyzdvihne sám. */
  function shipping(c) {
    if (CFG.shippingInPrice) return 0;
    return pickup ? 0 : shipCost();
  }

  function totals(c) {
    return c.reduce(function (s, i) { return s + convert(i.usd) * i.qty; }, 0);
  }

  function renderCart() {
    var box = el("cartBox"); if (!box) return;
    var c = read();
    if (!c.length) {
      box.innerHTML = '<div class="cart-empty"><h3>' + esc(T.empty) + "</h3><p>" +
        esc(T.emptyNote) + '</p><p style="margin-top:18px"><a class="btn" href="produkty.html">' +
        esc(T.toCatalog) + "</a></p></div>";
      var f = el("cartForm"); if (f) f.hidden = true;
      return;
    }
    var rows = c.map(function (i, k) {
      var unit = convert(i.usd), sum = unit * i.qty;
      return '<tr data-k="' + k + '">' +
        '<td class="ci">' + (i.img ? '<img src="' + esc(i.img) + '?width=120" alt="">' : "") +
          '<span><b>' + esc(i[LANG]) + "</b>" +
          (i["v" + LANG] ? "<em>" + esc(i["v" + LANG]) + "</em>" : "") +
          (i.sku ? '<span class="ci-sku">' + esc(i.sku) + "</span>" : "") + "</span></td>" +
        '<td class="cq"><button type="button" data-d="-1" aria-label="−">−</button>' +
          "<span>" + i.qty + "</span>" +
          '<button type="button" data-d="1" aria-label="+">+</button></td>' +
        "<td>" + esc(fmt(unit)) + "</td>" +
        "<td><b>" + esc(fmt(sum)) + "</b></td>" +
        '<td><button type="button" class="ci-x" data-x="1" aria-label="' + esc(T.remove) + '">×</button></td>' +
        "</tr>";
    }).join("");
    box.innerHTML =
      '<div class="table-wrap"><table class="cart-t"><thead><tr>' +
      "<th>" + esc(T.item) + "</th><th>" + esc(T.qty) + "</th><th>" + esc(T.unit) +
      "</th><th>" + esc(T.sum) + "</th><th></th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
      (CFG.pickup
        ? '<div class="cart-ship"><label><input type="radio" name="dlv" value="courier"' +
          (pickup ? "" : " checked") + "><span>" + esc(T.dlvCourier) +
          (CFG.shippingInPrice ? "" : " — " + esc(fmt(shipCost()))) +
          "</span></label>" +
          '<label><input type="radio" name="dlv" value="pickup"' +
          (pickup ? " checked" : "") + "><span>" + esc(T.dlvPickup) +
          (CFG.shippingInPrice ? "" : " — " + esc(T.free)) +
          "</span></label></div>"
        : "") +
      '<div class="cart-sums">' +
        "<div><span>" + esc(T.goods) + "</span><span>" + esc(fmt(totals(c))) + "</span></div>" +
        (CFG.shippingInPrice
          ? "<div><span>" + esc(T.shipping) + "</span><span>" +
            esc(T.shipFree) + "</span></div>"
          : "<div><span>" + esc(T.shipping) + "</span><span>" +
            esc(pickup ? T.free : fmt(shipCost())) + "</span></div>") +
        '<div class="cart-sum"><span>' + esc(T.total) + "</span><b>" +
          esc(fmt(totals(c) + shipping(c))) + "</b></div>" +
      "</div>" +
      '<p class="note">' + esc(T.vatNote) + "</p>";

    box.querySelectorAll("input[name=dlv]").forEach(function (r) {
      r.onchange = function () { pickup = r.value === "pickup"; renderCart(); };
    });

    box.querySelectorAll("[data-d]").forEach(function (b) {
      b.onclick = function () {
        var k = +b.closest("tr").dataset.k, c2 = read();
        c2[k].qty = Math.max(1, c2[k].qty + (+b.dataset.d));
        write(c2); renderCart();
      };
    });
    box.querySelectorAll("[data-x]").forEach(function (b) {
      b.onclick = function () {
        var k = +b.closest("tr").dataset.k, c2 = read();
        c2.splice(k, 1); write(c2); renderCart();
      };
    });
  }

  /* ---------- objednávka e-mailom ---------- */
  function buildOrder() {
    var c = read();
    var g = function (id) {
      var n = el(id);
      if (!n) return "";
      /* pri výbere nás zaujíma text voľby, nie jej kód */
      if (n.tagName === "SELECT" && n.selectedIndex >= 0)
        return n.options[n.selectedIndex].textContent.trim();
      return (n.value || "").trim();
    };
    var L = LANG === "cs"
      ? { o: "OBJEDNÁVKA", z: "ZÁKAZNÍK", ad: "DORUČOVACÍ ADRESA", no: "POZNÁMKA",
          tot: "CELKEM S DPH", goods: "Zboží", ship: "Doprava",
          nm: "Jméno", em: "E-mail", ph: "Telefon", co: "Firma / IČO",
          src: "Odesláno z", pay: "Objednávka zavazující k platbě" }
      : { o: "OBJEDNÁVKA", z: "ZÁKAZNÍK", ad: "DORUČOVACIA ADRESA", no: "POZNÁMKA",
          tot: "SPOLU S DPH", goods: "Tovar", ship: "Doprava",
          nm: "Meno", em: "E-mail", ph: "Telefón", co: "Firma / IČO",
          src: "Odoslané z", pay: "Objednávka zaväzujúca k platbe" };
    var line = "──────────────────────────────";
    var out = [L.pay, "", L.o, line];
    c.forEach(function (i, k) {
      out.push((k + 1) + ". " + i[LANG]);
      if (i["v" + LANG]) out.push("   " + T.variant + ": " + i["v" + LANG]);
      if (i.sku) out.push("   " + (LANG === "cs" ? "Kód" : "Kód") + ": " + i.sku);
      out.push("   " + T.qty + ": " + i.qty + "   " + T.unit + ": " + fmt(convert(i.usd)) +
               "   " + T.sum + ": " + fmt(convert(i.usd) * i.qty));
    });
    out.push(line,
      L.goods + ": " + fmt(totals(c)),
      L.ship + ": " + (CFG.shippingInPrice
        ? T.shipFree
        : pickup ? T.free + " (" + T.dlvPickup + ")" : fmt(shipCost())),
      L.tot + ": " + fmt(totals(c) + shipping(c)), "",
      L.z, line,
      L.nm + ": " + g("cName"), L.em + ": " + g("cEmail"), L.ph + ": " + g("cPhone"));
    if (g("cCompany")) out.push(L.co + ": " + g("cCompany"));
    out.push("", L.ad, line, g("cStreet"), g("cZip") + " " + g("cCity"), g("cCountry"));
    if (g("cNote")) out.push("", L.no, line, g("cNote"));
    out.push("", line, L.src + ": " + location.origin + location.pathname);
    return { subject: L.pay + " — " + c.length + "× " +
             (LANG === "cs" ? "položka" : "položka") + ", " + fmt(totals(c) + shipping(c)),
             body: out.join("\n") };
  }

  var NEED = ["cName", "cEmail", "cPhone", "cStreet", "cCity", "cZip", "cCountry"];

  function fieldNodes() {
    return NEED.map(el).filter(Boolean);
  }

  function valid() {
    if (!window.RNCValid) {           /* keby site.js nedobehol */
      return fieldNodes().every(function (n) { return (n.value || "").trim(); });
    }
    return window.RNCValid.run(fieldNodes());
  }

  function mailtoFallback(o) {
    var href = "mailto:" + encodeURIComponent(CFG.orderEmail) +
      "?subject=" + encodeURIComponent(o.subject) + "&body=" + encodeURIComponent(o.body);
    if (href.length > 1900) href = href.slice(0, 1900);
    window.location.href = href;
  }

  /* Objednávku odošle služba, ktorá ju prepošle e-mailom.
     Stránka nemá server, preto sa volá priamo z prehliadača. */
  function send(o) {
    var how = (CFG.orderSend || "mailto").toLowerCase();
    var g = function (id) {
      var n = el(id);
      if (!n) return "";
      if (n.tagName === "SELECT" && n.selectedIndex >= 0)
        return n.options[n.selectedIndex].textContent.trim();
      return (n.value || "").trim();
    };

    /* Vlastný odosielač: e-mail odchádza z našej domény, kľúč drží Worker. */
    if (how === "api" && CFG.apiUrl) {
      return fetch(CFG.apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          kind: "order",
          lang: LANG,
          subject: o.subject,
          body: o.body,
          name: g("cName"),
          email: g("cEmail"),
          website: g("cWebsite")   /* pasca na roboty, človek ju nevyplní */
        })
      }).then(function (r) { return r.json().catch(function () { return {}; }); })
        .then(function (j) { if (!j || j.ok !== true) throw new Error("api"); });
    }
    if (how === "web3forms" && CFG.formKey) {
      return fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          access_key: CFG.formKey,
          subject: o.subject,
          from_name: g("cName") || "Objednávka",
          replyto: g("cEmail"),
          email: g("cEmail"),
          message: o.body
        })
      }).then(function (r) { return r.json(); })
        .then(function (j) { if (!j || j.success !== true) throw new Error("web3forms"); });
    }
    if (how === "formsubmit") {
      return fetch("https://formsubmit.co/ajax/" + encodeURIComponent(deliveryEmail()), {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: o.subject,
          _captcha: "false",
          _template: "table",
          name: g("cName"),
          email: g("cEmail"),
          phone: g("cPhone"),
          company: g("cCompany"),
          address: g("cStreet") + ", " + g("cZip") + " " + g("cCity") + ", " + g("cCountry"),
          note: g("cNote"),
          order: o.body
        })
      }).then(function (r) { return r.json(); })
        .then(function (j) {
          var ok = j && (j.success === true || String(j.success) === "true");
          if (ok) return;
          var msg = (j && j.message) || "";
          var e = new Error(msg || "formsubmit");
          /* prvá objednávka len vyžiada potvrdenie adresy */
          e.activation = /activat/i.test(msg);
          throw e;
        });
    }
    return Promise.reject(new Error("mailto"));
  }

  function done(msg, ok) {
    var box = el("cartMsg");
    if (box) { box.className = ok ? "msg ok" : "msg"; box.textContent = msg; }
  }

  function armLive() {
    if (window.RNCValid) window.RNCValid.live(fieldNodes());
  }

  function submit(e) {
    e.preventDefault();
    if (!read().length) return;
    if (!valid()) { done(T.need, false); return; }

    var o = buildOrder();
    var btn = el("cartOrder");
    var label = btn ? btn.textContent : "";
    if (btn) { btn.disabled = true; btn.textContent = T.sending; }
    done(T.sending, false);

    send(o).then(function () {
      write([]);                       /* košík je vybavený */
      var box = el("cartBox");
      if (box) box.innerHTML = '<div class="cart-empty"><h3>' + esc(T.thanks) +
        "</h3><p>" + esc(T.thanksNote) + "</p></div>";
      var f = el("cartForm"); if (f) f.hidden = true;
      done(T.sent, true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }).catch(function (err) {
      /* keď služba zlyhá, objednávka nesmie zmiznúť */
      if (btn) { btn.disabled = false; btn.textContent = label; }
      if (err && err.message) { try { console.warn("objednávka:", err.message); } catch (e) {} }
      done(err && err.activation ? T.needsActivation : T.mailFallback, false);
      mailtoFallback(o);
    });
  }

  /* ---------- štart ---------- */
  function start() {
    badge();
    renderCart();
    armLive();
    var f = el("cartForm");
    if (f) {
      f.addEventListener("submit", submit);
      var h = el("cartHint");
      if (h) h.innerHTML = esc(T.hint) + '<a href="mailto:' + esc(CFG.orderEmail) + '">' +
        esc(CFG.orderEmail) + "</a>";
      var tt = el("cartTerms"); if (tt) tt.textContent = T.terms;
      var ob = el("cartOrder"); if (ob) ob.textContent = T.order;
      var lh = el("cartContactH"); if (lh) lh.textContent = T.contact;
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();

  window.RNCCart = { add: add, count: count, render: renderCart };
})();
