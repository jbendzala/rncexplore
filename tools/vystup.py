# -*- coding: utf-8 -*-
"""Kam exporty zapisujú.

Predtým si každý skript písal do ~/Documents vlastnou cestou a výsledkom
bolo dvadsať súborov vedľa seba, kde nebolo vidieť, čo sa nahráva do
Shoptetu, čo sa vkladá ručne a čo je len pre nás. Cesta je preto na
jednom mieste a rozdelená podľa toho, čo sa so súborom robí.

Keď sa niečo presunie v Finderi, ale nie tu, ďalší beh exportu to vysype
naspäť — preto to patrí sem a nie do príkazu mv.
"""
import os

ZAKLAD = os.path.expanduser("~/Documents/rncexplore-podklady")

# Čo sa nahráva do Shoptetu importom.
IMPORT = os.path.join(ZAKLAD, "shoptet-import")
# Čo sa do Shoptetu vkladá ručne — články a stránky sa importovať nedajú.
VLOZIT = os.path.join(ZAKLAD, "shoptet-na-vlozenie")
# Naše vlastné exporty: cenníky, podklady pre partnerov, pre Lensun.
NASE = os.path.join(ZAKLAD, "nase-exporty")
# Návrhy, poznámky, dokumenty.
DOKUMENTY = os.path.join(ZAKLAD, "dokumenty")


def kam(skupina, *cesta):
    """Vráti cestu a založí priečinok, aby to nemusel riešiť každý export."""
    p = os.path.join(skupina, *cesta)
    os.makedirs(os.path.dirname(p) if os.path.splitext(p)[1] else p,
                exist_ok=True)
    return p
