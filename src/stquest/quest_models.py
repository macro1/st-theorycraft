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
    ench_elem: str
    ench_soul: Optional[EnchSoul]

    def get_hp(self) -> int:
        return int(self.blueprint.base_hp * QUALITY_MULTIPLIER[self.quality])

    def get_atk(self) -> int:
        return int(self.blueprint.base_atk * QUALITY_MULTIPLIER[self.quality])

    def get_def(self) -> int:
        return int(self.blueprint.base_def * QUALITY_MULTIPLIER[self.quality])


class Hero(pydantic.BaseModel):
    hero_class: data_models.HeroClass
    items: List[Item]
    skill_names: List[str]
    level: int = 40

    @property
    def stat_hp(self) -> int:
        return self.hero_class.base_hp[self.level] + sum(i.get_hp() for i in self.items)

    @property
    def stat_atk(self) -> int:
        return self.hero_class.base_atk[self.level] + sum(
            i.get_atk() for i in self.items
        )

    @property
    def stat_def(self) -> int:
        return self.hero_class.base_def[self.level] + sum(
            i.get_def() for i in self.items
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
