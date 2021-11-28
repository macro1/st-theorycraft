from stquest import hero_quest_import


def test_get_hero_for_string() -> None:
    hero_string = (
        "Yes|Green Type|Trickster|"
        "Bow|Light Armor|Rogue Hat|Gloves|Amulet|Ring|"
        "Pinata Hunter - T11|Cat Burglar Outfit - T11|Cat Burglar Hood - T11|Raptor Wings - T11|Forlorn Acorn - T11|Bunbun Band - T10|"
        "Legendary|Legendary|Legendary|Legendary|Legendary|Legendary|"
        "15 / Tier 9|15 / Tier 9|15 / Tier 9|15 / Tier 9|15 / Tier 9|15 / Tier 9|"
        "||||||"
        "Backstab (+60% ATK & +10% Crit Chance)|Blurred Movement (+25% EVA)|Extra Conditioning (+50% DEF & +15% EVA)||"
        "40|40|40|40|"
    )
    hero = hero_quest_import.get_hero_for_string(hero_string)
    test_hero_string = hero_quest_import.get_string_for_hero(hero)
    assert test_hero_string.split("|") == hero_string.split("|")
