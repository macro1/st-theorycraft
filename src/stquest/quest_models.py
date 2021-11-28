import collections
import enum
from typing import List, Optional

import pydantic

from stdata import data_models


class EnchSoul(enum.Enum):
    ARMADILLO = enum.auto()
    LIZARD = enum.auto()
    SHARK = enum.auto()
    DINOSAUR = enum.auto()
    MUNDRA = enum.auto()

    CAT = "cat"
    LION = "lion"


class Quality(enum.Enum):
    NORMAL = "normal"
    SUPERIOR = "superior"
    FLAWLESS = "flawless"
    EPIC = "epic"
    LEGENDARY = "legendary"


QUALITY_MULTIPLIER = {
    Quality.NORMAL: 1.0,
    Quality.SUPERIOR: 1.25,
    Quality.FLAWLESS: 2.0,
    Quality.EPIC: 3.0,
    Quality.LEGENDARY: 5.0,
}


class Item(pydantic.BaseModel):
    blueprint: data_models.Blueprint
    quality: Quality
    ench_elem: Optional[int]
    ench_soul: Optional[EnchSoul]

    def get_hp(self) -> int:
        if not self.blueprint.base_hp:
            return 0
        element_hp = {None: 0, 9: 10}[self.ench_elem]
        soul_hp = {None: 0, EnchSoul.MUNDRA: 10}.get(self.ench_soul, 10)
        return int(
            (self.blueprint.base_hp + element_hp + soul_hp)
            * QUALITY_MULTIPLIER[self.quality]
        )

    def get_atk(self) -> int:
        eq_atk = int(self.blueprint.base_atk * QUALITY_MULTIPLIER[self.quality])
        element_atk = min([{None: 0, 9: 48}[self.ench_elem], eq_atk])
        soul_atk = min([{None: 0, EnchSoul.MUNDRA: 50}.get(self.ench_soul, 48), eq_atk])
        return eq_atk + element_atk + soul_atk

    def get_def(self) -> int:
        if not self.blueprint.base_def:
            return 0
        element_def = {None: 0, 9: 10}[self.ench_elem]
        soul_def = {None: 0, EnchSoul.MUNDRA: 33}.get(self.ench_soul, 10)
        return int(
            (self.blueprint.base_def + element_def + soul_def)
            * QUALITY_MULTIPLIER[self.quality]
        )

    def get_eva(self) -> int:
        return {
            None: 0,
            EnchSoul.CAT: 2,
            EnchSoul.LION: 1,
        }.get(self.ench_soul, 0) + self.blueprint.eva


class Hero(pydantic.BaseModel):
    hero_class: data_models.HeroClass
    items: List[Item]
    skills: List[data_models.Skill]
    level: int = 40
    seed_hp: int = 0
    seed_atk: int = 0
    seed_def: int = 0

    @property
    def stat_hp(self) -> int:
        return (
            self.hero_class.base_hp[self.level]
            + self.seed_hp
            + sum(i.get_hp() for i in self.items)
        )

    @property
    def stat_atk(self) -> int:
        """ATK = (Base ATK + Seed ATK
        + (Weapon ATK + Enchants) * (1 + Weapon Skill + Gear Skill)
        + (Gear ATK + Enchants) * (1 + Gear Skill) )
        * (1 + ATK Modifiers)"""
        atk = self.hero_class.base_atk[self.level]  # Base ATK
        atk += self.seed_atk * 4  # Seed ATK

        for i in self.items:
            # Weapon, Enchants, Weapon and Gear Skill
            weapon_skill = sum(
                s.get_weapon_atk()
                for s in self.skills
                if i.blueprint.type in s.gear_types
            )
            eq_bonus = sum(s.get_eq_bonus() for s in self.skills)
            item_atk = int(i.get_atk() * (1.0 + (weapon_skill + eq_bonus) / 100.0))

            atk += item_atk

        soul_counts = collections.Counter(i.ench_soul for i in self.items)
        # ATK Modifiers
        damage_bonus = (
            sum(s.get_atk() for s in self.skills) + 5 * soul_counts[EnchSoul.LION]
        )
        atk = int(atk * (1.0 + (damage_bonus / 100.0)))

        return atk

    @property
    def stat_def(self) -> int:
        return (
            self.hero_class.base_def[self.level]
            + self.seed_def
            + sum(i.get_def() for i in self.items)
        )

    @property
    def stat_threat(self) -> int:
        return {"Red": 90, "Green": 40, "Blue": 10}[self.hero_class.class_type]

    @property
    def stat_crit_chance(self) -> int:
        return {"Red": 5, "Green": 20, "Blue": 5}[self.hero_class.class_type]

    @property
    def stat_crit_mult(self) -> int:
        return 200

    @property
    def stat_eva(self) -> int:
        return {"Red": 0, "Green": 30, "Blue": 0}[self.hero_class.class_type] + sum(
            i.get_eva() for i in self.items
        )

    @property
    def num_armadillo(self) -> int:
        ...

    @property
    def num_lizard(self) -> int:
        ...

    @property
    def num_shark(self) -> int:
        ...

    @property
    def num_dinosaur(self) -> int:
        ...

    @property
    def num_mundra(self) -> int:
        ...

    @property
    def stat_atk_pct_non_weapon(self) -> int:
        ...

    @property
    def stat_def_pct_non_weapon(self) -> int:
        ...
