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
        if not self.blueprint.base_atk:
            return 0
        element_atk = {None: 0, 9: 10}[self.ench_elem]
        soul_atk = {None: 0, EnchSoul.MUNDRA: 50}.get(self.ench_soul, 48)
        return int(
            (self.blueprint.base_atk + element_atk + soul_atk)
            * QUALITY_MULTIPLIER[self.quality]
        )

    def get_def(self) -> int:
        if not self.blueprint.base_def:
            return 0
        element_def = {None: 0, 9: 10}[self.ench_elem]
        soul_def = {None: 0, EnchSoul.MUNDRA: 33}.get(self.ench_soul, 10)
        return int(
            (self.blueprint.base_def + element_def + soul_def)
            * QUALITY_MULTIPLIER[self.quality]
        )


class Hero(pydantic.BaseModel):
    hero_class: data_models.HeroClass
    items: List[Item]
    skill_names: List[str]
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
        return (
            self.hero_class.base_atk[self.level]
            + self.seed_atk
            + sum(i.get_atk() for i in self.items)
        )

    @property
    def stat_def(self) -> int:
        return (
            self.hero_class.base_def[self.level]
            + self.seed_def
            + sum(i.get_def() for i in self.items)
        )

    @property
    def stat_threat(self) -> int:
        ...

    @property
    def stat_crit_chance(self) -> int:
        ...

    @property
    def stat_crit_mult(self) -> int:
        ...

    @property
    def stat_eva(self) -> int:
        ...

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
