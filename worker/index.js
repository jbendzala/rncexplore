/* ==========================================================================
   Odosielanie objednávok a dopytov z rncexplore.com.

   Web je statický, preto nemá kde bezpečne držať prístupový kľúč k poštovej
   službe. Tento Worker ho drží namiesto neho: stránka pošle formulár sem,
   Worker zavolá Brevo a e-mail odíde z našej vlastnej domény.

   Vďaka tomu:
     * odosielateľom je objednavky@rncexplore.com, nie cudzia adresa,
     * správa je podpísaná DKIM a prejde SPF, takže nepadá do spamu,
     * kľúč zostáva na serveri, z prehliadača sa k nemu nedá dostať.

   Nastavenie je vo wrangler.toml, tajomstvá cez `wrangler secret put`.
   ========================================================================== */

const CORS = (origin) => ({
  "Access-Control-Allow-Origin": origin,
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
  Vary: "Origin",
});

function json(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...CORS(origin) },
  });
}

/** Do e-mailu nesmie preliezť riadok navyše — ten by sa dal zneužiť. */
function clean(v, max) {
  return String(v == null ? "" : v).replace(/[\r\n]+/g, " ").trim().slice(0, max || 200);
}

function validEmail(v) {
  return /^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/.test(v);
}

async function brevo(env, payload) {
  const r = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: {
      "api-key": env.BREVO_API_KEY,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    const text = await r.text();
    throw new Error("brevo " + r.status + ": " + text.slice(0, 300));
  }
  return r.json();
}

/* Potvrdenie pre zákazníka. Zámerne jednoduché — faktúru posielame zvlášť. */
function confirmBody(lang, name, orderText) {
  const sk = lang !== "cs";
  const hi = sk ? `Dobrý deň, ${name},` : `Dobrý den, ${name},`;
  const got = sk
    ? "ďakujeme za objednávku. Prijali sme ju a obratom vám pošleme faktúru s QR kódom na zaplatenie."
    : "děkujeme za objednávku. Přijali jsme ji a obratem vám pošleme fakturu s QR kódem k zaplacení.";
  const ship = sk
    ? "Tovar expedujeme po pripísaní platby."
    : "Zboží expedujeme po připsání platby.";
  const rec = sk ? "Rekapitulácia objednávky" : "Rekapitulace objednávky";
  const bye = sk ? "Safiri s.r.o. · www.rncexplore.com" : "Safiri s.r.o. · www.rncexplore.com";
  return `${hi}\n\n${got}\n${ship}\n\n${rec}\n${orderText}\n\n${bye}`;
}

export default {
  async fetch(request, env) {
    const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
    const origin = request.headers.get("Origin") || "";
    const ok = allowed.includes(origin);
    const cors = ok ? origin : allowed[0] || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS(cors) });
    }
    if (request.method !== "POST") {
      return json({ ok: false, error: "method" }, 405, cors);
    }
    if (!ok) {
      return json({ ok: false, error: "origin" }, 403, cors);
    }

    let d;
    try {
      d = await request.json();
    } catch (e) {
      return json({ ok: false, error: "json" }, 400, cors);
    }

    /* Skryté pole, ktoré človek nevyplní. Roboty áno — a tie odmietneme. */
    if (clean(d.website)) {
      return json({ ok: true }, 200, cors);
    }

    const name = clean(d.name, 120);
    const email = clean(d.email, 160);
    const lang = d.lang === "cs" ? "cs" : "sk";
    const subject = clean(d.subject, 200) || "Správa z webu";
    const body = String(d.body == null ? "" : d.body).slice(0, 20000);
    const kind = d.kind === "inquiry" ? "inquiry" : "order";

    if (!name || !validEmail(email) || !body.trim()) {
      return json({ ok: false, error: "fields" }, 400, cors);
    }

    const from = { name: env.FROM_NAME || "Safiri s.r.o.", email: env.FROM_EMAIL };
    const to = kind === "inquiry" ? env.INFO_EMAIL : env.ORDER_EMAIL;

    try {
      /* 1. nám — s odpoveďou rovno na zákazníka */
      await brevo(env, {
        sender: from,
        to: [{ email: to }],
        replyTo: { email, name },
        subject,
        textContent: body,
      });

      /* 2. zákazníkovi — potvrdenie z našej adresy.
         Keby zlyhalo, objednávku už máme, takže ju nezhadzujeme. */
      let copy = true;
      try {
        await brevo(env, {
          sender: from,
          to: [{ email, name }],
          replyTo: { email: to },
          subject: (lang === "cs" ? "Potvrzení objednávky — " : "Potvrdenie objednávky — ")
            + (env.FROM_NAME || "Safiri s.r.o."),
          textContent: confirmBody(lang, name, body),
        });
      } catch (e) {
        copy = false;
      }

      return json({ ok: true, copy }, 200, cors);
    } catch (e) {
      return json({ ok: false, error: "send" }, 502, cors);
    }
  },
};
