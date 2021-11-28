import collections
import itertools
from typing import Dict, List, Optional

import pydantic


def decode_attrib(field_name: str) -> str:
    return {"base_hp": "HP", "base_atk": "ATK", "base_def": "DEF", "eva": "EVA"}.get(
        field_name, field_name.replace("_", " ").title()
    )


class Skill(pydantic.BaseModel):
    name: str


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

    @property
    def is_weapon(self) -> bool:
        return self.type in ["wand"]
