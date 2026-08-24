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

Repozitár: `github.com/jbendzala/rncexplore` · doména: `rncexplore.com`
(DNS spravuje **Websupport.sk**, registrátor Gransy)

### Krok 1 — repozitár musí byť verejný

GitHub Pages z **privátneho** repozitára funguje len s plateným plánom
(GitHub Pro). Náš repozitár je teraz privátny, takže najprv:

**Settings → General → Danger Zone → Change visibility → Make public**

Zverejní sa tým celý kód vrátane `config.js` (e-mail a telefón) — tie sú
aj tak viditeľné na samotnom webe. Ceny a marža v `config.js` budú tiež
verejné; ak to nechcete, zvoľte radšej GitHub Pro.

### Krok 2 — zapnúť Pages

**Settings → Pages → Build and deployment**
- Source: `Deploy from a branch`
- Branch: `main`, priečinok `/ (root)` → **Save**

Do minúty beží na `https://jbendzala.github.io/rncexplore/`.
Overte, že web funguje, až potom pokračujte doménou.

### Krok 3 — doména v GitHube

**Settings → Pages → Custom domain** → zadajte `www.rncexplore.com` → **Save**

GitHub tým vytvorí v repozitári súbor `CNAME` (nový commit priamo na
GitHube). Pred ďalším pushom si preto stiahnite zmeny:

```bash
git pull origin main
```

### Krok 4 — DNS na Websupport

V administrácii Websupport: **Domény → rncexplore.com → DNS záznamy**.

> **Najprv zmažte** existujúce záznamy `A` pre `@` aj `www`, ktoré teraz
> smerujú na `37.9.175.132`. Ak ich necháte, prevádzka sa bude striedavo
> posielať na starý server a web bude fungovať len občas.
> Pri `www` nemôže súčasne existovať `A` aj `CNAME`.

Potom pridajte:

| Typ | Názov | Hodnota | TTL |
|---|---|---|---|
| CNAME | `www` | `jbendzala.github.io.` | 3600 |
| A | `@` | `185.199.108.153` | 3600 |
| A | `@` | `185.199.109.153` | 3600 |
| A | `@` | `185.199.110.153` | 3600 |
| A | `@` | `185.199.111.153` | 3600 |

Štyri `A` záznamy pre `@` zabezpečia, že `rncexplore.com` bez `www`
presmeruje na `www.rncexplore.com`. Voliteľne pridajte aj IPv6 (`AAAA`
pre `@`): `2606:50c0:8000::153`, `2606:50c0:8001::153`,
`2606:50c0:8002::153`, `2606:50c0:8003::153`.

### Krok 5 — HTTPS

Keď sa DNS rozšíri (spravidla 10–60 minút, výnimočne až 24 h), vráťte sa
do **Settings → Pages** a zapnite **Enforce HTTPS**. Certifikát vystaví
GitHub automaticky. Kým sa nevystaví, políčko je neaktívne — počkajte.

### Overenie

```bash
dig +short www.rncexplore.com     # má vrátiť jbendzala.github.io
dig +short rncexplore.com         # má vrátiť štyri 185.199.x.153
curl -sI https://www.rncexplore.com | head -3
```

### Aktualizácia webu

Odteraz stačí:

```bash
git add -A && git commit -m "popis zmeny" && git push
```

Pages nasadí zmenu do minúty.

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
