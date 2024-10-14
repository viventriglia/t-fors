from pathlib import Path
from typing import Literal
import requests
import zipfile
from io import BytesIO
from urllib.parse import quote
import re

import pandas as pd


def read_time_series(
    data_in_path: Path,
    column_names: list[str],
    datetime_format: str = "%d-%b-%Y %H:%M:%S",
    **kwargs,
) -> pd.DataFrame:
    """
    Convenience function to load time-series data from CSV files

    Parameters
    ----------
    data_in_path : Path
        Input file path
    column_names : list[str]
        Column names for the resulting DataFrame
    datetime_format : str, optional
        String format (according to https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), by default "%d-%b-%Y %H:%M:%S"

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_csv(
        filepath_or_buffer=data_in_path,
        header=0,
        names=column_names,
        **kwargs,
    )

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], format=datetime_format)
        df = df.set_index("datetime")
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format=datetime_format)
        df = df.set_index("date")

    return df


def techtide_response(
    start: str, stop: str, product: Literal["hfi", "hficond"]
) -> requests.Response:
    """
    Convenience function to perform get requests to the TechTIDE API

    Parameters
    ----------
    start : str
        Start date-time in 'YYYY-MM-DD HH:MM:SS' format
    stop : str
        End date-time in 'YYYY-MM-DD HH:MM:SS' format
    product : str
        TechTIDE data product to be retrieved: "hfi" accesses ionosonde data,
        while "hficond" fetches the HF-INT index

    Returns
    -------
    requests.Response
    """
    URL = "https://techtide-srv-pub.space.noa.gr:8443/api/products/hfi/data/"
    URL += f"?date_from={quote(start)}&date_to={quote(stop)}&product={product}&withmanifest=false"

    return requests.get(
        URL,
        headers={"accept": "application/zip"},
        verify=False,  # FIXME
    )


def get_techtide_hf(start: str, stop: str) -> pd.DataFrame:
    """
    Convenience function to fetch HF-INT EU data from TechTIDE API

    Parameters
    ----------
    start : str
        Start date-time in 'YYYY-MM-DD HH:MM:SS' format
    stop : str
        End date-time in 'YYYY-MM-DD HH:MM:SS' format

    Returns
    -------
    pd.DataFrame
    """
    response = techtide_response(start=start, stop=stop, product="hficond")

    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            results = []

            for file_ in z.namelist():
                if file_.startswith("TechTIDE_hficond"):
                    with z.open(file_) as f:
                        first_line = f.readline().decode("utf-8").strip()
                        datetime_match = re.search(r"(\d{8})(\d{4})", first_line)
                        activity_index_match = re.search(
                            r"ActivityIndex=\s*([\d.]+)", first_line
                        )

                        if datetime_match and activity_index_match:
                            datetime = f"{datetime_match.group(1)[:4]}-{datetime_match.group(1)[4:6]}-{datetime_match.group(1)[6:8]} {datetime_match.group(2)[:2]}:{datetime_match.group(2)[2:]}"
                            activity_index = activity_index_match.group(1)
                            results.append(
                                {
                                    "datetime": pd.to_datetime(datetime),
                                    "hf": float(activity_index),
                                }
                            )

            return pd.DataFrame(results).set_index("datetime")
    else:
        print(response.status_code)
        return pd.DataFrame({})


def get_techtide_ionosondes(start: str, stop: str) -> pd.DataFrame:
    """
    Convenience function to fetch ionosondes data from TechTIDE API

    Parameters
    ----------
    start : str
        Start date-time in 'YYYY-MM-DD HH:MM:SS' format
    stop : str
        End date-time in 'YYYY-MM-DD HH:MM:SS' format

    Returns
    -------
    pd.DataFrame
    """
    response = techtide_response(start=start, stop=stop, product="hfi")
