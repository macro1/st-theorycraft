from typing import List, cast

from . import quest_models


def get_hero_for_string(hero_string: str) -> quest_models.Hero:
    (
        promoted,
        class_type,
        hero_class,
        gear1_type,
        gear2_type,
        gear3_type,
        gear4_type,
        gear5_type,
        gear6_type,
        gear1_name,
        gear2_name,
        gear3_name,
        gear4_name,
        gear5_name,
        gear6_name,
        gear1_quality,
        gear2_quality,
        gear3_quality,
        gear4_quality,
        gear5_quality,
        gear6_quality,
        gear1_elem_tier,
        gear2_elem_tier,
        gear3_elem_tier,
        gear4_elem_tier,
        gear5_elem_tier,
        gear6_elem_tier,
        gear1_soul,
        gear2_soul,
        gear3_soul,
        gear4_soul,
        gear5_soul,
        gear6_soul,
        skill1,
        skill2,
        skill3,
        skill4,
        _,
        seed_hp,
        seed_atk,
        seed_def,
        _,
    ) = hero_string.split("|")
    fn_locals = locals()
    return quest_models.Hero(
        hero_class_name=hero_class,
        items=[
            quest_models.Item(
                blueprint_name=fn_locals[f"gear{n}_name"],
                quality=fn_locals[f"gear{n}_quality"],
                ench_elem=fn_locals[f"gear{n}_elem_tier"],
                ench_soul=fn_locals[f"gear{n}_soul"],
            )
            for n in range(1, 7)
        ],
        skill_names=cast(List[str], [skill1, skill2, skill3, skill4]),
        seed_hp=seed_hp,
        seed_atk=seed_atk,
        seed_def=seed_def,
    )


def get_string_for_hero(hero: quest_models.Hero) -> str:
    return "|".join(
        [
            "",  # promoted
            "",  # class type
            hero.hero_class.name,
        ]
    )
