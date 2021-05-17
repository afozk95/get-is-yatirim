import pathlib
from typing import Any, Dict, List, Optional, Union
import datetime as dt
import json
from pathlib import Path
import requests


def save_json(path: Union[Path, str], data: Union[Dict[str, Any], List[Any]]) -> None:
    with open(path, "w") as f:
        json.dump(data, f)


def get_stock_recommendations_by_sector_and_year(
    sector_code: str,
    year_code: str,
) -> Dict[str, Any]:
    url = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/SirketBilgileriBySektor"
    r = requests.get(url, params = {"takip": "Yes", "sektor": sector_code, "yil": year_code})
    return r.json()["value"]


def get_all_stock_recommendations(output_path: Optional[Union[Path, str]] = None) -> Dict[str, Any]:
    current_year = dt.datetime.now().year
    SECTOR_CODES = {
        "industry": "00",
        "insurance": "0040",
        "banking": "0001",
        "reic": "0015",
        "holding": "0019",
        "leasing": "0014",
    }
    YEAR_CODES = {f"{i}": current_year+i-1 for i in range(0, 3+1)}

    all_data = {}
    for year_code, year in YEAR_CODES.items():
        data_by_year = []
        for sector_code in SECTOR_CODES.values():
            data_by_year_and_sector = get_stock_recommendations_by_sector_and_year(sector_code, year_code)
            data_by_year.extend(data_by_year_and_sector)
        all_data[year] = data_by_year
    
    if output_path is not None:
        save_json(output_path, all_data)

    return all_data


if __name__ == "__main__":
    get_all_stock_recommendations("all_data.json")
