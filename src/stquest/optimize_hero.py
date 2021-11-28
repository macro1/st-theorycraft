import itertools
from typing import List, Optional, Tuple

import glpk

from stdata import data_models, load_data

from . import quest_models


def run(
    hero_class_name: str,
    hero_level: int,
    gear_quality: str,
    seeds: bool = True,
    override_skills: Optional[List[str]] = None,
) -> quest_models.Hero:
    hero_class = load_data.get_class(hero_class_name)

    max_tier = load_data.get_hero_levels()[hero_level]["Max Item Tier"]

    all_items = load_data.get_blueprints(remove_redundant=True, max_tier=max_tier)

    blueprint_combo = []
    for combination in hero_class.item_type_combinations():
        for blueprint_option in itertools.product(
            *(all_items[btype] for btype in combination)
        ):
            blueprint_combo.append(blueprint_option)

    lp = glpk.LPX()
    glpk.env.term_on = False
    lp.cols.add(len(blueprint_combo))
    lp.rows.add(1)

    for col in lp.cols:
        col.kind = bool

    lp.rows[0].matrix = [1.0] * len(lp.cols)
    lp.rows[0].bounds = 1, 1

    for idx, bps in enumerate(blueprint_combo):
        items = [
            quest_models.Item(
                blueprint=b, quality=gear_quality, ench_elem=9, ench_soul="lion"
            )
            for b in bps
        ]
        lp.obj[idx] = (
            sum(i.get_atk() for i in items)
            + sum(i.get_def() for i in items)
            + (10 * sum(i.get_hp() for i in items))
            + (10 * sum(i.get_eva() for i in items))
        )

    lp.obj.maximize = True

    lp.simplex()

    solutions = []
    for col, bps in zip(lp.cols, blueprint_combo):
        if col.value < 0.1:
            continue
        solutions.append(bps)
    [blueprints] = solutions

    hero = quest_models.Hero(
        hero_class=hero_class,
        items=[
            quest_models.Item(
                blueprint=bp, quality=gear_quality, ench_elem=9, ench_soul="lion"
            )
            for bp in blueprints
        ],
        skills=[],
        level=hero_level,
        seed_hp=40 if seeds else 0,
        seed_atk=40 if seeds else 0,
        seed_def=40 if seeds else 0,
    )

    try:
        [weapon_bp] = [b for b in blueprints if b.type in ["wand"]]
    except ValueError:
        estimated_weapon_importance = 0.0
    else:
        estimated_weapon_importance = weapon_bp.base_atk / sum(
            b.base_atk for b in blueprints
        )

    skill_options = load_data.get_skills(hero_class=hero_class)
    if override_skills:
        skill_options = [
            option
            for option in skill_options
            if all(
                any(s.name.lower().startswith(o.lower()) for s in option)
                for o in override_skills
            )
        ]

    def score_skill_combo(skills: Tuple[data_models.Skill, ...]) -> float:
        linear_atk = sum(
            s.get_atk()
            + s.get_weapon_atk() * estimated_weapon_importance
            + s.get_eq_bonus()
            for s in skills
        )
        crit_amt = (
            linear_atk
            * (hero.stat_crit_mult + sum(s.get_crit_damage() for s in skills))
            / 100.0
        )
        crit_chance = (
            hero.stat_crit_chance + sum(s.get_crit_chance() for s in skills)
        ) / 100.0
        if hero.hero_class.name == "Dancer":
            crit_chance = (
                crit_chance * (hero.stat_eva + sum(s.get_eva() for s in skills)) / 100.0
            )
        avg_atk = linear_atk * (1.0 - crit_chance) + crit_amt * crit_chance
        return avg_atk

    skills = max(skill_options, key=score_skill_combo)

    return quest_models.Hero(
        hero_class=hero_class,
        items=[
            quest_models.Item(
                blueprint=bp, quality=gear_quality, ench_elem=9, ench_soul="lion"
            )
            for bp in blueprints
        ],
        skills=skills,
        level=hero_level,
        seed_hp=40 if seeds else 0,
        seed_atk=40 if seeds else 0,
        seed_def=40 if seeds else 0,
    )
