import json
from typing import Dict, Iterator, List, Optional, Tuple, Union

import requests

CellValue = Union[None, float, str]


def query_sheet(
    document_id: str,
    sheet_name: str,
    tq: str = "SELECT *",
    as_dicts: bool = True,
    cell_range: Optional[str] = None,
) -> Union[Iterator[Dict[str, CellValue]], Iterator[Tuple[CellValue, ...]]]:

    headers: Dict[str, str] = {"X-DataSource-Auth": ""}
    params = {"tqx": "out:json", "tq": tq, "sheet": sheet_name}
    if cell_range is not None:
        params["range"] = cell_range
    data_resp = requests.get(
        f"https://docs.google.com/spreadsheets/d/{document_id}/gviz/tq",
        params=params,
        headers=headers,
    )

    sheet_data = json.loads(data_resp.text.split("\n", maxsplit=1)[1])
    cols: List[str] = [c["label"] for c in sheet_data["table"]["cols"]]
    sheet_rows: List[Optional[Dict[str, Union[float, str]]]] = sheet_data["table"][
        "rows"
    ]

    for record in sheet_rows:
        values: Iterator[CellValue] = (v["v"] if v else None for v in record["c"])  # type: ignore
        if as_dicts:
            r_dict: Dict[str, CellValue] = dict(
                zip(
                    cols,
                    values,
                )
            )
            try:
                del r_dict[""]
            except KeyError:
                pass
            yield r_dict
        else:
            r_tuple: Tuple[CellValue, ...] = tuple(values)
            yield r_tuple
