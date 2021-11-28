import json
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

import requests


def query_sheet(
    document_id: str,
    sheet_name: str,
    tq: str = "SELECT *",
    cell_range: Optional[str] = None,
) -> Tuple[List[str], Iterable[Iterable[Any]]]:

    headers = {"X-DataSource-Auth": ""}
    params = {"tqx": "out:json", "tq": tq, "sheet": sheet_name}
    if cell_range is not None:
        params["range"] = cell_range
    data_resp = requests.get(
        f"https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq",
        params=params,
        headers=headers,
    )

    sheet_data = json.loads(data_resp.text.split("\n", maxsplit=1)[1])
    cols = [c["label"] for c in sheet_data["table"]["cols"]]
    sheet_rows = sheet_data["table"]["rows"]

    return cols, ((v["v"] if v else None for v in record["c"]) for record in sheet_rows)


def query_sheet_tuples(*args: Any, **kwargs: Any) -> Iterator[Tuple[Any, ...]]:

    _, sheet_rows = query_sheet(*args, **kwargs)

    return (tuple(r) for r in sheet_rows)


def query_sheet_dicts(*args: Any, **kwargs: Any) -> Iterator[Dict[str, Any]]:

    cols, sheet_rows = query_sheet(*args, **kwargs)
    for record in sheet_rows:
        r_dict = dict(
            zip(
                cols,
                record,
            )
        )
        try:
            del r_dict[""]
        except KeyError:
            pass
        yield r_dict
