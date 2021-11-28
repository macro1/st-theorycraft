from typing import Any, Dict, Iterable, List, Tuple

import requests

from . import google_sheets

DOCUMENT_URL = "http://bit.ly/shoptitans"
SHEET_HERO_CLASSSES = "Heroes"
SHEET_HERO_LEVELS = "Hero Levels"
CLASS_SHEET_COLUMN_WIDTH = 8
CLASS_TYPES = ["Red", "Green", "Blue"]


class InvalidDocumentURL(Exception):
    ...


def get_official_document_id() -> str:
    redirect_resp = requests.get(DOCUMENT_URL, allow_redirects=False)
    if redirect_resp.next is None or redirect_resp.next.url is None:
        raise InvalidDocumentURL("Unable to resolve redirect")
    return redirect_resp.next.url.split("/")[-1]


def capture_single_class(
    class_type: str, raw_data: List[Tuple[str, ...]]
) -> Dict[str, Any]:
    name_value = raw_data[0][1]
    name_value = name_value.split("\n")[0].title()
    return {"Name": name_value, "Class Type": class_type}


def capture_classes() -> Iterable[Dict[str, Any]]:

    hero_classes: List[Dict[str, Any]] = []
    raw_class_row_data: List[List[Any]] = []
    for record in google_sheets.query_sheet_tuples(
        get_official_document_id(), SHEET_HERO_CLASSSES
    ):
        if record[5] == "HP":
            if raw_class_row_data:
                for class_type, raw_class_data in zip(CLASS_TYPES, raw_class_row_data):
                    hero_classes.append(
                        capture_single_class(class_type, raw_class_data)
                    )
            raw_class_row_data = [list() for idx in range(len(CLASS_TYPES))]
        for column, raw_data in zip(range(len(CLASS_TYPES)), raw_class_row_data):
            offset = CLASS_SHEET_COLUMN_WIDTH * column
            raw_data.append(record[offset : offset + CLASS_SHEET_COLUMN_WIDTH])

    return hero_classes


def capture_hero_levels() -> Dict[int, Dict[str, Any]]:
    return {
        int(r["Hero Level"]): r
        for r in google_sheets.query_sheet_dicts(
            get_official_document_id(), SHEET_HERO_LEVELS
        )
    }
