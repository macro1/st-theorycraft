import json

from . import st_central_hero_quest_sim


def dump_json(data, outfile):
    json.dump(data, outfile, indent=2, sort_keys=True)


def download_classes(output_path):
    st_central_classes = st_central_hero_quest_sim.capture_classes()
    with open(output_path, "w") as outfile:
        dump_json(st_central_classes, outfile)


def download_skills(output_path):
    st_central_skills = st_central_hero_quest_sim.capture_skills()
    with open(output_path, "w") as outfile:
        dump_json(st_central_skills, outfile)


def download_items(output_path):
    st_central_items = st_central_hero_quest_sim.capture_items()
    with open(output_path, "w") as outfile:
        dump_json(st_central_items, outfile)
