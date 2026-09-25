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

import { DurableObject } from "cloudflare:workers";

/* Strop na odosielanie. Nativný rate-limit binding Cloudflare na tomto
   účte nič nevynucoval (38 žiadostí za sebou prešlo), preto počítame sami.
   Durable Object je na to určený: pre daný kľúč beží vždy jedna instancia,
   takže počítadlo nemá ako pretiecť dvoma cestami naraz.

   Dva stropy, každý na iné riziko:
     * na IP    — cudzí skript neposiela dávky,
     * na deň   — aj keby striedal IP, denná kvóta Breva prežije.            */
export class Throttle extends DurableObject {
  /** Kĺzavé okno pre jednu IP. */
  async hit(windowMs, max) {
    const now = Date.now();
    const hits = ((await this.ctx.storage.get("hits")) || [])
      .filter((t) => now - t < windowMs);
    if (hits.length >= max) return false;
    hits.push(now);
    await this.ctx.storage.put("hits", hits);
    return true;
  }

  /** Počet odoslaní za dnešný deň, spoločný pre celý web. */
  async day(max) {
    const today = new Date().toISOString().slice(0, 10);
    const rec = (await this.ctx.storage.get("day")) || { d: "", n: 0 };
    if (rec.d !== today) { rec.d = today; rec.n = 0; }
    if (rec.n >= max) return false;
    rec.n += 1;
    await this.ctx.storage.put("day", rec);
    return true;
  }
}

const PER_IP = { window: 60000, max: 5 };
const PER_DAY = 200;      /* Brevo dáva 300/deň, nechávame si rezervu */

/* Keď počítadlo zlyhá, radšej pustíme — objednávka je cennejšia než
   dokonalý strop. */

/** Strop na IP. Kontroluje sa hneď, ešte pred čítaním tela žiadosti. */
async function ipAllowed(env, ip) {
  if (!env.THROTTLE) return true;
  try {
    const o = env.THROTTLE.get(env.THROTTLE.idFromName("ip:" + ip));
    return await o.hit(PER_IP.window, PER_IP.max);
  } catch (e) {
    return true;
  }
}

/** Denný strop. Zvyšuje sa až tesne pred odoslaním — inak by nám roboty
    zachytené na pasci vyčerpali kvótu, hoci sa za ne nič neposiela. */
async function dayAllowed(env) {
  if (!env.THROTTLE) return true;
  try {
    const o = env.THROTTLE.get(env.THROTTLE.idFromName("global"));
    return await o.day(PER_DAY);
  } catch (e) {
    return true;
  }
}

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

/* Potvrdenie pre zákazníka. Zámerne jednoduché — faktúru posielame zvlášť.
   Dopyt nie je objednávka, preto má vlastné znenie: nič sme neprijali na
   zaplatenie a faktúra nepríde. */
function confirmBody(kind, lang, name, orderText) {
  const sk = lang !== "cs";
  const hi = sk ? `Dobrý deň, ${name},` : `Dobrý den, ${name},`;
  const bye = "Safiri s.r.o. · www.rncexplore.com";

  if (kind === "inquiry") {
    const got = sk
      ? "ďakujeme za správu. Prijali sme ju a ozveme sa vám najneskôr nasledujúci pracovný deň."
      : "děkujeme za zprávu. Přijali jsme ji a ozveme se vám nejpozději následující pracovní den.";
    const rec = sk ? "Kópia vašej správy" : "Kopie vaší zprávy";
    return `${hi}\n\n${got}\n\n${rec}\n${orderText}\n\n${bye}`;
  }

  const got = sk
    ? "ďakujeme za objednávku. Prijali sme ju a obratom vám pošleme faktúru s QR kódom na zaplatenie."
    : "děkujeme za objednávku. Přijali jsme ji a obratem vám pošleme fakturu s QR kódem k zaplacení.";
  const ship = sk
    ? "Tovar expedujeme po pripísaní platby."
    : "Zboží expedujeme po připsání platby.";
  const rec = sk ? "Rekapitulácia objednávky" : "Rekapitulace objednávky";
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

    /* Zoznam adries nestačí: Origin si klient vypíše aký chce. Strop na
       IP drží prípadné zneužitie v mieri a chráni denný limit Breva. */
    const ip = request.headers.get("CF-Connecting-IP") || "neznama";
    if (!(await ipAllowed(env, ip))) {
      return json({ ok: false, error: "rate" }, 429, cors);
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
    const body = String(d.body == null ? "" : d.body).slice(0, 8000);
    const kind = d.kind === "inquiry" ? "inquiry" : "order";

    if (!name || !validEmail(email) || !body.trim()) {
      return json({ ok: false, error: "fields" }, 400, cors);
    }

    if (!(await dayAllowed(env))) {
      return json({ ok: false, error: "rate" }, 429, cors);
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
          subject: (kind === "inquiry"
            ? (lang === "cs" ? "Přijali jsme vaši zprávu — " : "Prijali sme vašu správu — ")
            : (lang === "cs" ? "Potvrzení objednávky — " : "Potvrdenie objednávky — "))
            + (env.FROM_NAME || "Safiri s.r.o."),
          textContent: confirmBody(kind, lang, name, body),
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
