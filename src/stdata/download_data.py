import collections
import itertools
import json
from pathlib import Path
from typing import Any, Dict, Iterable, TextIO, Union

from . import official_spreadsheet, st_central_hero_quest_sim


def dump_json(
    data: Union[Iterable[Dict[str, Any]], Dict[Union[int, str], Any]], outfile: TextIO
) -> None:
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
    with open(output_path, "w") as outfile:
        dump_json(st_central_items, outfile)


def download_hero_levels(output_path: Path) -> None:
    official_hero_levels = official_spreadsheet.capture_hero_levels()
    with open(output_path, "w") as outfile:
        dump_json(official_hero_levels, outfile)
