import itertools

import glpk

from stdata import load_data

from . import quest_models


def run(hero_class_name: str, hero_level: int, gear_quality: str) -> quest_models.Hero:
    hero_class = load_data.get_class(hero_class_name)

    max_tier = load_data.get_hero_levels()[hero_level]["Max Item Tier"]

    all_items = load_data.get_blueprints(remove_redundant=True, max_tier=max_tier)

    blueprint_combo = []
    for combination in hero_class.item_type_combinations():
        for blueprint_option in itertools.product(
            *(all_items[btype] for btype in combination)
        ):
            blueprint_combo.append(blueprint_option)
    print(len(blueprint_combo))

    lp = glpk.LPX()
    glpk.env.term_on = False
    lp.cols.add(len(blueprint_combo))
    lp.rows.add(1)

    for col in lp.cols:
        col.kind = bool

    lp.rows[0].matrix = [1.0] * len(lp.cols)
    lp.rows[0].bounds = 1, 1

    for idx, bps in enumerate(blueprint_combo):
        lp.obj[idx] = (
            sum(b.base_atk for b in bps)
            + sum(b.base_def for b in bps)
            + (10 * sum(b.base_hp for b in bps))
        )

    lp.obj.maximize = True

    lp.simplex()

    solutions = []
    for col, bps in zip(lp.cols, blueprint_combo):
        if col.value < 0.1:
            continue
        solutions.append(bps)
    [blueprints] = solutions
    print(blueprints)

    return quest_models.Hero(
        hero_class=hero_class,
        items=[
            quest_models.Item(
                blueprint=bp, quality=gear_quality, ench_elem="T9", ench_soul="lion"
            )
            for bp in blueprints
        ],
        skill_names=[],
        level=hero_level,
    )
