import collections
import itertools
import json
from pathlib import Path
from typing import Any, Dict, TextIO

from . import official_spreadsheet, st_central_hero_quest_sim


def dump_json(data: Any, outfile: TextIO) -> None:
    json.dump(data, outfile, indent=2, sort_keys=True)


def download_classes(output_path: Path) -> None:

    all_classes: Dict[str, Dict[str, Any]] = collections.defaultdict(dict)
    for class_data in itertools.chain(
        st_central_hero_quest_sim.capture_classes(),
        official_spreadsheet.capture_classes(),
    ):
        all_classes[class_data["Name"]].update(class_data)

    with open(output_path, "w") as outfile:
        dump_json(list(all_classes.values()), outfile)


def download_skills(output_path: Path) -> None:
    st_central_skills = st_central_hero_quest_sim.capture_skills()
    with open(output_path, "w") as outfile:
        dump_json(st_central_skills, outfile)


def download_items(output_path: Path) -> None:
    st_central_items = st_central_hero_quest_sim.capture_items()
    official_items = official_spreadsheet.capture_items()
    combined_items = collections.defaultdict(dict)
    for item in itertools.chain(st_central_items, official_items):
        combined_items[item["Name"]].update(item)
    with open(output_path, "w") as outfile:
        dump_json(list(combined_items.values()), outfile)


def download_hero_levels(output_path: Path) -> None:
    official_hero_levels = official_spreadsheet.capture_hero_levels()
    with open(output_path, "w") as outfile:
        dump_json(official_hero_levels, outfile)
