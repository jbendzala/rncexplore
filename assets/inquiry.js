/* ==========================================================================
   Jednoduchý dopytový formulár bez servera. Rovnakou cestou ako objednávka:
   údaje prepošle formulárová služba na náš e-mail, pri výpadku sa otvorí
   e-mailový klient. Formulár sa označí triedou "inq-form", polia atribútom
   data-label; povinné majú "required".
   ========================================================================== */
(function () {
  "use strict";
  var CFG = window.SITE_CONFIG || {};
  var LANG = window.LANG === "cs" ? "cs" : "sk";

  var T = {
    sk: { sending: "Odosielam…",
          sent: "Ďakujeme, správu sme dostali. Ozveme sa vám obratom.",
          need: "Vyplňte prosím povinné údaje označené hviezdičkou.",
          mailFallback: "Správu sa nepodarilo odoslať automaticky, preto sme otvorili váš e-mailový klient. Správu už len odošlite.",
          needsActivation: "Formulár ešte nie je aktivovaný. V schránke, kam sa správy doručujú, nájdete e-mail od formsubmit.co — kliknite v ňom na Activate Form. Správa sa zatiaľ odosiela e-mailovým klientom.",
          src: "Odoslané z" },
    cs: { sending: "Odesílám…",
          sent: "Děkujeme, zprávu jsme dostali. Ozveme se vám obratem.",
          need: "Vyplňte prosím povinné údaje označené hvězdičkou.",
          mailFallback: "Zprávu se nepodařilo odeslat automaticky, proto jsme otevřeli váš e-mailový klient. Zprávu už jen odešlete.",
          needsActivation: "Formulář ještě není aktivovaný. Ve schránce, kam se zprávy doručují, najdete e-mail od formsubmit.co — klikněte v něm na Activate Form. Zpráva se zatím odesílá e-mailovým klientem.",
          src: "Odesláno z" }
  }[LANG];

  /* Formulár si cieľovú schránku určí atribútom data-to:
     "info" = všeobecné otázky, inak objednávky. */
  function deliveryEmail(form) {
    if (form && form.getAttribute("data-to") === "info")
      return CFG.infoEmail || CFG.orderEmail;
    return CFG.deliverTo || CFG.orderEmail;
  }

  function fields(form) {
    return Array.prototype.slice.call(form.querySelectorAll("[data-label]"));
  }

  function valid(form) {
    if (!window.RNCValid) {
      return fields(form).every(function (n) {
        return !n.required || (n.value || "").trim();
      });
    }
    return window.RNCValid.run(fields(form));
  }

  function build(form) {
    var line = "─".repeat(30);
    var out = [form.getAttribute("data-subject") || "", line];
    fields(form).forEach(function (n) {
      var v = (n.value || "").trim();
      if (v) out.push(n.getAttribute("data-label") + ": " + v);
    });
    out.push("", line, T.src + ": " + location.origin + location.pathname);
    return { subject: form.getAttribute("data-subject") || "Dopyt",
             body: out.join("\n") };
  }

  function pick(form, kind) {
    var n = form.querySelector("[data-role=" + kind + "]");
    return n ? (n.value || "").trim() : "";
  }

  function send(form, o) {
    var how = (CFG.orderSend || "mailto").toLowerCase();
    if (how === "web3forms" && CFG.formKey) {
      return fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ access_key: CFG.formKey, subject: o.subject,
          from_name: pick(form, "name") || o.subject, replyto: pick(form, "email"),
          email: pick(form, "email"), message: o.body })
      }).then(function (r) { return r.json(); })
        .then(function (j) { if (!j || j.success !== true) throw new Error("web3forms"); });
    }
    if (how === "formsubmit") {
      var payload = { _subject: o.subject, _captcha: "false", _template: "table",
                      email: pick(form, "email"), message: o.body };
      fields(form).forEach(function (n) {
        var v = (n.tagName === "SELECT" && n.selectedIndex >= 0)
          ? n.options[n.selectedIndex].textContent.trim()
          : (n.value || "").trim();
        if (v) payload[n.getAttribute("data-label")] = v;
      });
      var post = function (to) {
        return fetch("https://formsubmit.co/ajax/" + encodeURIComponent(to), {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload)
        }).then(function (r) { return r.json(); })
          .then(function (j) {
            if (j && (j.success === true || String(j.success) === "true")) return;
            var msg = (j && j.message) || "";
            var e = new Error(msg || "formsubmit");
            e.activation = /activat/i.test(msg);
            throw e;
          });
      };
      var want = deliveryEmail(form);
      var backup = CFG.deliverTo || CFG.orderEmail;
      /* Kým nová adresa nie je u formulárovej služby potvrdená, správu
         radšej pošleme na overenú schránku, než by sme ju stratili. */
      return post(want).catch(function (err) {
        if (err && err.activation && backup && backup !== want) return post(backup);
        throw err;
      });
    }
    return Promise.reject(new Error("mailto"));
  }

  function mailtoFallback(o, form) {
    var href = "mailto:" + encodeURIComponent(deliveryEmail(form)) +
      "?subject=" + encodeURIComponent(o.subject) + "&body=" + encodeURIComponent(o.body);
    if (href.length > 1900) href = href.slice(0, 1900);
    window.location.href = href;
  }

  function init(form) {
    if (window.RNCValid) window.RNCValid.live(fields(form));
    var box = form.querySelector(".msg");
    var btn = form.querySelector("button[type=submit]");
    var label = btn ? btn.textContent : "";
    function say(msg, ok) {
      if (!box) return;
      box.className = ok ? "msg ok" : "msg";
      box.textContent = msg;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!valid(form)) { say(T.need, false); return; }
      var o = build(form);
      if (btn) { btn.disabled = true; btn.textContent = T.sending; }
      say(T.sending, false);
      send(form, o).then(function () {
        form.reset();
        say(T.sent, true);
      }).catch(function (err) {
        say(err && err.activation ? T.needsActivation : T.mailFallback, false);
        mailtoFallback(o, form);
      }).then(function () {
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
    });
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll("form.inq-form"), init);
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
