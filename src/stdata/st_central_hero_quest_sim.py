import collections
from typing import Any, Dict, List, Tuple

import requests

from . import google_sheets

DOCUMENT_URL = "https://rebrand.ly/heroquest"
SHEET_SKILL_DATA = "Skill Data"
SHEET_HERO_STATS = "Hero Stats"
SHEET_AUX_STUFF1 = "Aux_Stuff1"

EQ_QUEST_DOCUMENT_ID = "1nQCu8NDWFLANauYLL_sbBXKrsSjFnmD5BfRyzp_EqWU"
SHEET_EQ_DATA = "Eq_Data"


def get_heroquest_documet_id() -> str:
    redirect_resp = requests.get(DOCUMENT_URL, allow_redirects=False)
    if redirect_resp.next is None or redirect_resp.next.url is None:
        raise Exception("Unable to resolve document identifier.")
    return redirect_resp.next.url.rsplit("/", maxsplit=2)[-2]


def capture_classes() -> List[Dict[str, str]]:
    stat_types = ["HP", "ATK", "DEF"]

    hero_classes: Dict[str, Dict[str, Any]] = collections.defaultdict(dict)
    current_header: Tuple[Any, ...]

    for r in google_sheets.query_sheet_tuples(
        get_heroquest_documet_id(), SHEET_HERO_STATS
    ):
        if r[0] in stat_types:
            current_header = r
            continue
        hero_class = hero_classes[r[0]]
        hero_class["Name"] = r[0]
        hero_class[current_header[0]] = {
            k: int(v) for k, v in zip(range(1, len(r)), r[1:])
        }

    header = None
    for r in google_sheets.query_sheet_tuples(
        get_heroquest_documet_id(),
        SHEET_AUX_STUFF1,
        cell_range="A11:Y50",
    ):
        if header is None:
            header = list(r)
            header[0] = "Class"
            continue
        record = dict(zip(header, r))
        hero_class = hero_classes[record["Class"]]
        for option_label, option_value in record.items():
            if not option_label.startswith("Slot ") or not option_value:
                continue
            slot = option_label.split(" - ")[0]
            hero_class.setdefault(slot, list())
            hero_class[slot].append(option_value)

    return list(hero_classes.values())


def capture_skills() -> List[Dict[str, Any]]:
    return list(
        google_sheets.query_sheet_dicts(get_heroquest_documet_id(), SHEET_SKILL_DATA)
    )


def capture_items() -> List[Dict[str, Any]]:
    return list(google_sheets.query_sheet_dicts(EQ_QUEST_DOCUMENT_ID, SHEET_EQ_DATA))
