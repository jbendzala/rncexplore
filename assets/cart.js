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
          total: "Celkom", vatNote: "Ceny sú vrátane DPH. Dopravu doúčtujeme podľa hmotnosti zásielky.",
          contact: "Doručovacie a fakturačné údaje",
          order: "Objednávka zaväzujúca k platbe",
          sent: "Objednávka odoslaná. Obratom vám pošleme faktúru s QR kódom na zaplatenie.",
          sending: "Odosielam objednávku…",
          mailFallback: "Objednávku sa nepodarilo odoslať automaticky, preto sme otvorili váš e-mailový klient. Správu už len odošlite.",
          needsActivation: "Formulár ešte nie je aktivovaný. V schránke objednavky@rncexplore.com nájdete e-mail od formsubmit.co — kliknite na odkaz Activate Form. Objednávka sa zatiaľ odosiela e-mailovým klientom.",
          thanks: "Ďakujeme za objednávku",
          thanksNote: "Kópiu sme poslali aj na váš e-mail. Faktúru s QR kódom vám pošleme obratom.",
          hint: "Ak sa e-mailový klient neotvorí, skopírujte objednávku a pošlite nám ju na ",
          terms: "Odoslaním objednávky potvrdzujete, že ste sa oboznámili s obchodnými podmienkami a že objednávka je spojená s povinnosťou platby.",
          need: "Vyplňte prosím povinné údaje označené hviezdičkou." },
    cs: { added: "Přidáno do košíku", cart: "Košík", empty: "Košík je prázdný",
          emptyNote: "Vyberte produkty v katalogu a přidejte je do košíku.",
          toCatalog: "Přejít do katalogu", item: "Položka", variant: "Provedení",
          qty: "Počet", unit: "Cena za kus", sum: "Celkem", remove: "Odstranit",
          total: "Celkem", vatNote: "Ceny jsou včetně DPH. Dopravu doúčtujeme podle hmotnosti zásilky.",
          contact: "Doručovací a fakturační údaje",
          order: "Objednávka zavazující k platbě",
          sent: "Objednávka odeslána. Obratem vám pošleme fakturu s QR kódem k zaplacení.",
          sending: "Odesílám objednávku…",
          mailFallback: "Objednávku se nepodařilo odeslat automaticky, proto jsme otevřeli váš e-mailový klient. Zprávu už jen odešlete.",
          needsActivation: "Formulář ještě není aktivovaný. Ve schránce objednavky@rncexplore.com najdete e-mail od formsubmit.co — klikněte na odkaz Activate Form. Objednávka se zatím odesílá e-mailovým klientem.",
          thanks: "Děkujeme za objednávku",
          thanksNote: "Kopii jsme poslali i na váš e-mail. Fakturu s QR kódem vám pošleme obratem.",
          hint: "Pokud se e-mailový klient neotevře, zkopírujte objednávku a pošlete nám ji na ",
          terms: "Odesláním objednávky potvrzujete, že jste se seznámili s obchodními podmínkami a že objednávka je spojena s povinností platby.",
          need: "Vyplňte prosím povinné údaje označené hvězdičkou." }
  }[LANG];

  /* ---------- ceny ---------- */
  function convert(usd) {
    var rate = (CFG.rates && CFG.rates[CUR]) || 1;
    var v = usd * (CFG.markup || 1) * rate;
    if (CFG.rounding === "9") { v = Math.max(0, Math.round(v)); if (v >= 100) v = Math.floor(v / 10) * 10 + 9; }
    else if (CFG.rounding === "0") { v = Math.round(v); }
    return v;
  }
  function fmt(v) {
    var dec = v < 20 ? 2 : 0;
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
      '<div class="cart-sum"><span>' + esc(T.total) + "</span><b>" + esc(fmt(totals(c))) + "</b></div>" +
      '<p class="note">' + esc(T.vatNote) + "</p>";

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
    var g = function (id) { var n = el(id); return n ? (n.value || "").trim() : ""; };
    var L = LANG === "cs"
      ? { o: "OBJEDNÁVKA", z: "ZÁKAZNÍK", ad: "DORUČOVACÍ ADRESA", no: "POZNÁMKA",
          tot: "CELKEM", nm: "Jméno", em: "E-mail", ph: "Telefon", co: "Firma / IČO",
          src: "Odesláno z", pay: "Objednávka zavazující k platbě" }
      : { o: "OBJEDNÁVKA", z: "ZÁKAZNÍK", ad: "DORUČOVACIA ADRESA", no: "POZNÁMKA",
          tot: "SPOLU", nm: "Meno", em: "E-mail", ph: "Telefón", co: "Firma / IČO",
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
    out.push(line, L.tot + ": " + fmt(totals(c)), "",
      L.z, line,
      L.nm + ": " + g("cName"), L.em + ": " + g("cEmail"), L.ph + ": " + g("cPhone"));
    if (g("cCompany")) out.push(L.co + ": " + g("cCompany"));
    out.push("", L.ad, line, g("cStreet"), g("cZip") + " " + g("cCity"), g("cCountry"));
    if (g("cNote")) out.push("", L.no, line, g("cNote"));
    out.push("", line, L.src + ": " + location.origin + location.pathname);
    return { subject: L.pay + " — " + c.length + "× " +
             (LANG === "cs" ? "položka" : "položka") + ", " + fmt(totals(c)),
             body: out.join("\n") };
  }

  function valid() {
    var need = ["cName", "cEmail", "cPhone", "cStreet", "cCity", "cZip"];
    var ok = true;
    need.forEach(function (id) {
      var n = el(id); if (!n) return;
      var bad = !n.value.trim();
      n.classList.toggle("bad", bad);
      if (bad) ok = false;
    });
    return ok;
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
    var g = function (id) { var n = el(id); return n ? (n.value || "").trim() : ""; };
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
      return fetch("https://formsubmit.co/ajax/" + encodeURIComponent(CFG.orderEmail), {
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
