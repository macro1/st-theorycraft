import collections
import json
from typing import Dict, Iterator, List, Optional, Tuple, Union

import requests

CellValue = Union[None, float, str]

DOCUMENT_URL = "https://rebrand.ly/heroquest"
SHEET_SKILL_DATA = "Skill Data"
SHEET_HERO_STATS = "Hero Stats"


def query_sheet(
    sheet_name: str, tq: str = "SELECT *", as_dicts: bool = True
) -> Union[Iterator[Dict[str, CellValue]], Iterator[Tuple[CellValue, ...]]]:
    redirect_resp = requests.get(DOCUMENT_URL, allow_redirects=False)
    if redirect_resp.next is None or redirect_resp.next.url is None:
        raise Exception("Unable to resolve document identifier.")
    document_id = redirect_resp.next.url.rsplit("/", maxsplit=2)[-2]
    headers: Dict[str, str] = {"X-DataSource-Auth": ""}
    data_resp = requests.get(
        f"https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq",
        params={"tqx": "out:json", "tq": tq, "sheet": sheet_name},
        headers=headers,
    )

    sheet_data = json.loads(data_resp.text.split("\n", maxsplit=1)[1])  # type: ignore
    cols: List[str] = [c["label"] for c in sheet_data["table"]["cols"]]  # type: ignore
    sheet_rows: List[Optional[Dict[str, Union[float, str]]]] = sheet_data["table"]["rows"]  # type: ignore

    for record in sheet_rows:
        values: Iterator[CellValue] = (v["v"] if v else None for v in record["c"])  # type: ignore
        if as_dicts:
            r_dict: Dict[str, CellValue] = dict(
                zip(
                    cols,
                    values,
                )
            )
            yield r_dict
        else:
            r_tuple: Tuple[CellValue, ...] = tuple(values)
            yield r_tuple


def capture_classes():
    stat_types = ["HP", "ATK", "DEF"]

    hero_classes = collections.defaultdict(dict)

    current_header = None
    for r in query_sheet(SHEET_HERO_STATS, as_dicts=False):
        if r[0] in stat_types:
            current_header = r
            continue
        hero_class = hero_classes[r[0]]
        hero_class["Name"] = r[0]
        hero_class[current_header[0]] = {
            k: int(v) for k, v in zip(range(1, len(r)), r[1:])
        }

    return list(hero_classes.values())


def capture_skills():
    return list(query_sheet(SHEET_SKILL_DATA))
