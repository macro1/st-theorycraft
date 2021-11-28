import collections
import itertools
import json
import pathlib
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from . import data_models

stats = [
    "base_atk",
    "base_hp",
    "base_def",
    "crit_chance",
    "eva",
]


def get_class(hero_class_name: str) -> data_models.HeroClass:
    hero_class_name = hero_class_name.lower()
    with open(pathlib.Path("data") / "classes.json") as infile:
        hero_classes = json.load(infile)
    try:
        [hero_class] = (c for c in hero_classes if c["Name"].lower() == hero_class_name)
    except ValueError:
        raise Exception(f"Unable to find data for hero class {hero_class_name}")
    return data_models.HeroClass(**hero_class)


def get_hero_levels() -> Dict[int, Dict[str, Any]]:
    with open(pathlib.Path("data") / "hero_levels.json") as infile:
        hero_levels = json.load(infile)
    return {int(k): v for k, v in hero_levels.items()}


def compare_stats(
    stat_a: Union[int, float, None], stat_b: Union[int, float, None]
) -> bool:
    if not stat_a:
        return True
    if stat_b is None:
        stat_b = 0.0
    return stat_a < stat_b


def get_blueprints(
    remove_redundant: bool = False, max_tier: Optional[int] = None
) -> Dict[str, List[data_models.Blueprint]]:
    with open(pathlib.Path("data") / "items.json") as infile:
        raw_items = json.load(infile)
    if max_tier:
        raw_items = [
            i for i in raw_items if i[data_models.decode_attrib("tier")] <= max_tier
        ]
    if remove_redundant:
        redundant_items = []
        for item_a, item_b in itertools.permutations(raw_items, 2):
            if (
                item_a[data_models.decode_attrib("type")]
                != item_b[data_models.decode_attrib("type")]
            ):
                continue
            if all(
                compare_stats(
                    item_a[data_models.decode_attrib(stat)],
                    item_b[data_models.decode_attrib(stat)],
                )
                for stat in stats
            ):
                redundant_items.append(item_a)
        items = [
            data_models.Blueprint(**i) for i in raw_items if i not in redundant_items
        ]
    items_by_type = collections.defaultdict(list)
    for item in items:
        items_by_type[item.type].append(item)
    return items_by_type


def any_incompatible(skills: Iterable[data_models.Skill]) -> bool:
    for skill_a, skill_b in itertools.combinations(skills, 2):
        if (
            skill_a.name == skill_b.incompatibility
            or skill_b.name == skill_a.incompatibility
        ):
            return True
        if (
            "shield master " not in skill_a.name.lower()
            and "shield master " not in skill_b.name.lower()
        ):
            if (
                " master " in skill_a.name.lower()
                and " master " in skill_b.name.lower()
            ):
                return True
    return False


def get_skills(
    hero_class: data_models.HeroClass,
) -> List[Tuple[data_models.Skill, ...]]:
    with open(pathlib.Path("data") / "skills.json") as infile:
        raw_skills = json.load(infile)
    skills = [data_models.Skill(**s) for s in raw_skills if s[hero_class.name]]
    return [c for c in itertools.combinations(skills, r=4) if not any_incompatible(c)]
