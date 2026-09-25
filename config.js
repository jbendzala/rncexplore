/* ==========================================================================
   NASTAVENIE / NASTAVENÍ  —  upravte tieto hodnoty a nič iné.
   Configure these values; nothing else needs editing.
   ========================================================================== */
window.SITE_CONFIG = {
  /* --- 1. VAŠA FIRMA / VAŠE FIRMA ---------------------------------------
     Nahraďte zástupné hodnoty svojimi údajmi.
     Replace these placeholders with your own details.                     */
  company: "Safiri s.r.o.",
  street: "Pšurnovice 221",
  city: "014 01 Bytča",
  ico: "55635113",
  dic: "2122040844",
  icDph: "SK2122040844",          // sme platiteľ DPH
  hours: "9:00 – 18:00",
  orderEmail: "objednavky@rncexplore.com", // sem chodia objednávky / sem chodí objednávky
  infoEmail: "info@rncexplore.com",     // všeobecné otázky a poradenstvo
  phone: "+421 905 698 410",
  web: "www.rncexplore.com",

  /* --- 2. CENY / CENY ----------------------------------------------------
     Ceny v katalógu sú v USD (zdroj výrobcu). Prepočítavajú sa takto:
       zobrazená cena = USD × markup × kurz
     markup = vaša marža (1.0 = bez marže, 1.25 = +25 %).
     Kurzy si podľa potreby aktualizujte.                                   */
  markup: 1.0,

  /* Násobiteľ dolárovej ceny Lensunu na maloobchodnú cenu BEZ DPH.
     EUR je zámerne 1.0 — dolárovú cenu berieme jedna k jednej ako eurá,
     nie je to kurz a neaktualizuje sa. CZK je prepočet tej eurovej ceny
     na koruny, ten sa aktualizuje podľa ECB.                             */
  rates: { EUR: 1.0, CZK: 25.131 },

  /* Sadzba DPH. Ceny na webe sa zobrazujú s DPH, ako to pri predaji
     spotrebiteľom vyžaduje zákon. 0.23 = 23 %.                           */
  vat: 0.23,

  /* Doprava S DPH, paušál za celú objednávku. Účtuje sa až v košíku pri
     výbere spôsobu doručenia, do ceny produktu sa nezapočítava.           */
  shippingGross: { EUR: 20, CZK: 500 },

  /* true  = doprava je už v cene produktu, košík neúčtuje nič navyše.
     false = ceny sú bez dopravy a košík ju pripočíta samostatne.          */
  shippingInPrice: false,

  /* Ponúkame osobný odber v Bytči? true = v košíku pribudne možnosť
     odberu za 0 €.                                                       */
  pickup: true,

  /* Zaokrúhlenie ceny s DPH:
       "half" -> nadol na celé a +0,50 (619,92 -> 619,50; 619,01 -> 619,50).
                 V korunách len nadol na celé, halierniky sa nepoužívajú.
       "9"    -> 249 € končí na 9 (249, 259…)
       "0"    -> na celé
       null   -> presne prepočítané                                       */
  rounding: "half",

  /* Zobraziť pôvodnú prečiarknutú cenu, ak ju výrobca uvádza?
     Necháme vypnuté. Lensun uvádza „pôvodnú" cenu pri úplne každom
     produkte a počíta ju vzorcom cena ÷ 0,65 — nie je to cena, za ktorú
     sa kedy predávalo. Oznámená zľava musí podľa zákona vychádzať
     z najnižšej ceny za posledných 30 dní, preto ju nezobrazujeme.
     Zapnite až vtedy, keď budete mať vlastnú cenovú históriu.           */
  showCompareAt: false,

  /* Zobraziť ceny vôbec? false = všade "Cena na vyžiadanie"               */
  showPrices: true,

  /* --- 3. ODOSIELANIE OBJEDNÁVOK ----------------------------------------
     Stránka nemá vlastný server, objednávku preto odošle cez službu,
     ktorá ju prepošle e-mailom na adresu orderEmail vyššie.

     "formsubmit" — netreba nič zriaďovať. Pri úplne prvej objednávke
                    príde na orderEmail e-mail od formsubmit.co s odkazom
                    na potvrdenie. Kým naň nekliknete, objednávky nechodia.
     "web3forms"  — na web3forms.com zadáte e-mail, obratom vám pošlú
                    prístupový kľúč. Vložte ho nižšie do formKey.
     "mailto"     — otvorí e-mailového klienta zákazníka (bez služby).
     "api"        — vlastný odosielač cez Cloudflare Worker a Brevo.
                    E-mail odchádza priamo z objednavky@rncexplore.com,
                    je podpísaný DKIM a neputuje do spamu. Adresu Workera
                    vložte nižšie do apiUrl.

     Ak odoslanie zlyhá, formulár sa vždy prepne na "mailto",
     aby objednávka nezostala visieť.                                     */
  orderSend: "formsubmit",
  formKey: "",

  /* Adresa Workera pre orderSend: "api". Po nasadení ju vypíše wrangler,
     napríklad "https://rncexplore-mail.vase-meno.workers.dev".           */
  apiUrl: "",

  /* Kam objednávku reálne doručiť. Nechajte prázdne = doručí sa na
     orderEmail. Vyplňte len vtedy, keď schránka orderEmail ešte
     nefunguje alebo sa k nej neviete dostať — na webe sa aj tak
     všade zobrazuje orderEmail, zákazník túto adresu nevidí.
     Príklad: "j.bendzala.j@gmail.com"                                    */
  deliverTo: "objednavky@rncexplore.com",
};
