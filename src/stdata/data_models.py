import collections
import itertools
from typing import Any, Dict, List, Optional

import pydantic


def decode_attrib(field_name: str) -> str:
    return {"base_hp": "HP", "base_atk": "ATK", "base_def": "DEF", "eva": "EVA"}.get(
        field_name,
        field_name.replace("_", " ")
        .replace("pct", "%")
        .title()
        .replace("Hp", "HP")
        .replace("Atk", "ATK")
        .replace("Def", "DEF")
        .replace("Eva", "EVA")
        .replace("Shield DEF", "Shield Def")
        .replace("Req", "req"),
    )


class Skill(pydantic.BaseModel):
    name: str
    incompatibility: Optional[str]
    rarity: str
    gear_types: List[str] = pydantic.Field(default_factory=list)

    tier_1_hp: int
    tier_2_hp: int
    tier_3_hp: int
    tier_1_hp_pct: int
    tier_2_hp_pct: int
    tier_3_hp_pct: int

    tier_1_atk: int
    tier_2_atk: int
    tier_3_atk: int
    tier_1_weapon_atk: int
    tier_2_weapon_atk: int
    tier_3_weapon_atk: int

    tier_1_crit_chance: int
    tier_2_crit_chance: int
    tier_3_crit_chance: int
    tier_1_crit_damage: int
    tier_2_crit_damage: int
    tier_3_crit_damage: int

    tier_1_def: int
    tier_2_def: int
    tier_3_def: int
    tier_1_shield_def: int
    tier_2_shield_def: int
    tier_3_shield_def: int

    tier_1_eva: int
    tier_2_eva: int
    tier_3_eva: int

    tier_1_eq_bonus: int
    tier_2_eq_bonus: int
    tier_3_eq_bonus: int

    tier_2_element_req: int
    tier_3_element_req: int

    acrobat: bool
    archdruid: bool
    archmage: bool
    astramancer: bool
    barbarian: bool
    berserker: bool
    bishop: bool
    chieftain: bool
    cleric: bool
    conquistador: bool
    daimyo: bool
    dancer: bool
    druid: bool
    geomancer: bool
    grandmaster: bool
    jarl: bool
    knight: bool
    lord: bool
    mage: bool
    mercenary: bool
    monk: bool
    musketeer: bool
    ninja: bool
    pathfinder: bool
    ranger: bool
    samurai: bool
    sensei: bool
    soldier: bool
    sorcerer: bool
    spellblade: bool
    spellknight: bool
    thief: bool
    trickster: bool
    wanderer: bool
    warden: bool
    warlock: bool

    class Config:
        alias_generator = decode_attrib
        extra = "forbid"

    @pydantic.validator("gear_types", always=True, pre=True)
    def extract_gear_types(cls, v: List[str], values: Dict[str, Any]) -> List[str]:
        if values["name"].startswith("Wand"):
            return ["Wand"]
        if values["name"] == "Marksman":
            return ["Bow", "Crossbow", "Gun"]
        return v

    def get_hp(self) -> int:
        return self.tier_3_hp or self.tier_2_hp

    def get_hp_pct(self) -> int:
        return self.tier_3_hp_pct or self.tier_2_hp_pct

    def get_atk(self) -> int:
        return self.tier_3_atk or self.tier_2_atk

    def get_weapon_atk(self) -> int:
        return self.tier_3_weapon_atk or self.tier_2_weapon_atk

    def get_crit_chance(self) -> int:
        return self.tier_3_crit_chance or self.tier_2_crit_chance

    def get_crit_damage(self) -> int:
        return self.tier_3_crit_damage or self.tier_2_crit_damage

    def get_def(self) -> int:
        return self.tier_3_def or self.tier_2_def

    def get_shield_def(self) -> int:
        return self.tier_3_shield_def or self.tier_2_shield_def

    def get_eva(self) -> int:
        return self.tier_3_eva or self.tier_2_eva

    def get_eq_bonus(self) -> int:
        return self.tier_3_eq_bonus or self.tier_2_eq_bonus


class HeroClass(pydantic.BaseModel):
    name: str
    class_type: str
    base_hp: List[int]
    base_atk: List[int]
    base_def: List[int]
    slot_1: List[str]
    slot_2: List[str]
    slot_3: List[str]
    slot_4: List[str]
    slot_5: List[str]
    slot_6: List[str]

    @pydantic.validator("base_hp", "base_atk", "base_def", pre=True)
    def _base_stat(cls, v: Dict[str, int]) -> List[int]:
        stat_by_level = [0]
        for level in range(1, max(int(v_level) for v_level in v.keys()) + 1):
            stat_by_level.append(v[f"{level}"])
        return stat_by_level

    class Config:
        alias_generator = decode_attrib

    def item_type_combinations(self) -> List[List[str]]:
        unique_combinations = set()
        for combination in itertools.product(
            self.slot_1, self.slot_2, self.slot_3, self.slot_4, self.slot_5, self.slot_6
        ):
            normalized = tuple(sorted(collections.Counter(combination).items()))
            unique_combinations.add(normalized)
        return [
            [item_type for item_type, n in c for _ in range(n)]
            for c in unique_combinations
        ]


class Blueprint(pydantic.BaseModel):
    name: str
    base_atk: int
    base_hp: int
    base_def: int
    crit_chance: int
    eva: int
    type: str
    tier: int

    class Config:
        alias_generator = decode_attrib

    @pydantic.validator("crit_chance", pre=True)
    def handle_none(cls, v: Optional[int]) -> int:
        if not v:
            return 0
        return v

    @classmethod
    def get_by_name(cls, name: str) -> "Blueprint":
        return cls(name=name)
