# Katalóg solárnych panelov / Katalog solárních panelů

Statický dvojjazyčný katalóg (SK + CZ) so **566 produktmi**. Nie je to e-shop:
zákazník si prezerá sortiment a objednávku odosiela e-mailom priamo vám.

Bez databázy, bez servera, bez závislostí — funguje na GitHub Pages.

---

## 1. Nastavenie pred spustením

Otvorte **`config.js`** a upravte iba tento súbor:

| Položka | Význam |
|---|---|
| `company` | názov vašej firmy (v hlavičke a pätičke) |
| `orderEmail` | **e-mail, kam chodia objednávky** |
| `phone`, `web` | kontakt v pätičke |
| `markup` | vaša marža — `1.0` = bez marže, `1.25` = +25 % |
| `rates` | kurzy z USD (ceny v katalógu sú zdrojové v USD) |
| `rounding` | `"9"` = ceny končia na 9, `"0"` = celé čísla, `null` = presne |
| `showCompareAt` | zobraziť prečiarknutú pôvodnú cenu a zľavu v % |
| `showPrices` | `false` = všade „Cena na vyžiadanie“ |

> **Zástupné hodnoty na nahradenie:** `YOUR_COMPANY` a `objednavky@example.com`.

### Ceny

Zobrazená cena = `cena v USD × markup × kurz`. Slovenská verzia počíta v **EUR**,
česká v **CZK**. Kurzy si pravidelne aktualizujte v `config.js`.

Ak nechcete zdediť zľavové percentá výrobcu (`−55 %` a pod.), nastavte
`showCompareAt: false`.

---

## 2. Spustenie lokálne

```bash
python3 -m http.server 8000
```
Otvorte `http://localhost:8000/`. (Priame otvorenie súboru cez `file://`
nefunguje — prehliadač zablokuje načítanie dát.)

---

## 3. Nasadenie na GitHub Pages

```bash
git init
git add .
git commit -m "Katalóg solárnych panelov"
git branch -M main
git remote add origin https://github.com/POUZIVATEL/REPOZITAR.git
git push -u origin main
```

V repozitári: **Settings → Pages → Source: Deploy from a branch**,
branch `main`, folder `/ (root)`. Do minúty beží na
`https://POUZIVATEL.github.io/REPOZITAR/`.

### Vlastná doména

1. **Settings → Pages → Custom domain** — zadajte doménu a uložte
   (vytvorí sa súbor `CNAME`).
2. U registrátora domény nastavte DNS:
   - `www` → `CNAME` na `POUZIVATEL.github.io`
   - apex (`example.sk`) → `A` záznamy na
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. Po overení zapnite **Enforce HTTPS**.

---

## 4. Štruktúra

```
index.html          slovenská verzia
cz.html             česká verzia
config.js           ← jediný súbor na úpravu
data/products.js    dáta 566 produktov (SK + CZ názvy a popisy)
assets/styles.css   vzhľad
assets/app.js       filtrovanie, vyhľadávanie, detail, objednávka
.nojekyll           vypne spracovanie cez Jekyll
```

---

## 5. Ako funguje objednávka

Tlačidlo **Objednať / Objednat** otvorí formulár (kontakt, adresa, prevedenie,
počet kusov). Po odoslaní sa otvorí e-mailový klient zákazníka s pripravenou
správou na vašu adresu — obsahuje produkt, kód, prevedenie, počet, cenu
a všetky kontaktné údaje.

Pre prípad, že klient nemá nastavený e-mailový program, je vedľa tlačidlo
**Skopírovať údaje** — zákazník text vloží do webmailu.

> **Chcete objednávky bez e-mailového klienta?** Formulár sa dá napojiť na
> službu ako Formspree či Web3Forms — stačí vo `app.js` vo funkcii
> `submitOrder` poslať `buildOrder()` cez `fetch()` na ich endpoint.

---

## 6. Úprava produktov

`data/products.js` je generovaný súbor. Ručne sa dá upraviť ktorýkoľvek záznam:

```js
{ id:"...", cat:"hood", b:"Toyota", w:120, v:12, a:null, kg:10,
  usd:349, was:539, img:["https://…"], sku:"LS-…",
  n:{ sk:"názov SK", cs:"název CZ" },
  d:{ sk:"popis SK", cs:"popis CZ" },
  var:[{ sk:"Samotný panel", cs:"Samotný panel", p:349, sku:"…" }] }
```

Kategórie (`cat`): `hood`, `flexible`, `rooftent`, `tonneau`, `rv`,
`foldable`, `blanket`, `controller`, `inverter`, `accessory`.

Ak produkt pridáte alebo odoberiete, upravte aj počty v `window.CATALOG_META`
na začiatku súboru (`count` a `n` pri kategórii/značke).

---

## 7. Fotografie

Fotografie sa načítavajú z CDN výrobcu (nezaberajú miesto v repozitári).
Ak chcete byť nezávislí, stiahnite ich do priečinka `images/` a v
`data/products.js` prepíšte adresy v poli `img`.

---

## Poznámka k obsahu

Názvy, parametre a ceny vychádzajú z verejného sortimentu výrobcu Lensun.
Popisy produktov sú pôvodné, napísané pre tento katalóg. Pred zverejnením si
overte, že máte s výrobcom vysporiadaný vzťah predajcu a právo používať
jeho produktové fotografie.
