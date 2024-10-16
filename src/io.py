import requests
from io import StringIO, BytesIO
from pathlib import Path
from typing import Literal
import zipfile
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
    product = "hficond"
    response = techtide_response(start=start, stop=stop, product=product)

    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            results = []

            for file_ in z.namelist():
                if file_.startswith(f"TechTIDE_{product}_"):
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


def get_techtide_ionosondes(
    start: str, stop: str, iono_list: list[str]
) -> pd.DataFrame:
    """
    Convenience function to fetch ionosondes data from TechTIDE API

    Parameters
    ----------
    start : str
        Start date-time in 'YYYY-MM-DD HH:MM:SS' format
    stop : str
        End date-time in 'YYYY-MM-DD HH:MM:SS' format
    iono_list : list[str]
        List of ionosondes of interest; those available are:
        AT138, DB049, EB040, FF051, GR13L, HE13N, JR055,
        LV12P, MU12K, PQ052, RL052, RO041, SO148, VT139

    Returns
    -------
    pd.DataFrame
    """
    product = "hfi"
    cols_dict = {
        "STA": "cod_station",
        "DATE&TIME": "datetime",
        "SPCONT": "spectral_contribution",
        "VEL": "velocity",
        "AZI": "azimuth",
    }
    response = techtide_response(start=start, stop=stop, product=product)

    results = []
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            for file_ in z.namelist():
                if file_.startswith(f"TechTIDE_{product}_"):
                    with z.open(file_) as f:
                        df_ = pd.read_csv(
                            f, sep="\s+", skiprows=1, usecols=cols_dict.keys()
                        )
                        df_.columns = cols_dict.values()

                        df_ = df_[df_["cod_station"].isin(iono_list)]

                        df_["datetime"] = pd.to_datetime(
                            df_["datetime"], format="%Y%m%d%H%M"
                        )

                        df_["cod_station"] = (
                            df_["cod_station"].str.slice(0, 2).str.lower()
                        )

                        results.append(df_)

        df = pd.concat(objs=results).set_index(["datetime", "cod_station"]).unstack()
        df.columns = ["_".join(col).strip() for col in df.columns.values]
        return df
    else:
        print(response.status_code)
        return pd.DataFrame({})


def get_gfz_f107(end_date: str = None, last_n_days: int = 1) -> pd.DataFrame:
    """
    Function that downloads F10.7 (adjusted) within a specified time interval
    as collected by GFZ German Research Centre for Geosciences

    Parameters
    ----------
    end_date : str, optional
        End date of the time interval in 'YYYY-MM-DD' format, by default None
        If None, the function returns the last `last_n_days` days retrieved
    last_n_days : int, optional
        Number of days to return from the end of the dataset, by default 1

    Returns
    -------
    pd.DataFrame
    """
    response = requests.get(
        "https://kp.gfz-potsdam.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt"
    )
    if response.status_code != 200:
        raise Exception(f"Error while downloading data: {response.status_code}")

    data = StringIO(response.text)

    # Skipping the header
    data_lines = []
    for line in data:
        if not line.startswith("#"):
            data_lines.append(line)

    df = pd.read_csv(
        StringIO("".join(data_lines)),
        sep="\s+",
        header=None,
        usecols=[0, 1, 2, 26],
        names=[
            "year",
            "month",
            "day",
            "f_107_adj",
        ],
        na_values=[-1.0],
    )

    df["date"] = pd.to_datetime(
        df["year"].astype(str)
        + "-"
        + df["month"].astype(str)
        + "-"
        + df["day"].astype(str)
    )

    df = df.drop(columns=["year", "month", "day"]).set_index("date")

    if end_date is None:
        return df.tail(last_n_days)
    else:
        end_date = pd.to_datetime(end_date)
        return df.loc[:end_date].tail(last_n_days)


def get_gfz_hp30(start: str, stop: str) -> pd.DataFrame:
    """
    Function that downloads Hp30 within a specified time interval
    as produced by GFZ German Research Centre for Geosciences

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
    response = requests.get(
        "https://kp.gfz-potsdam.de/app/files/Hp30_ap30_complete_series.txt"
    )
    if response.status_code != 200:
        raise Exception(f"Error while downloading data: {response.status_code}")

    data = StringIO(response.text)

    # Skipping the header
    data_lines = []
    for line in data:
        if not line.startswith("#"):
            data_lines.append(line)

    df = pd.read_csv(
        StringIO("".join(data_lines)),
        sep="\s+",
        header=None,
        usecols=[0, 1, 2, 3, 7],
        names=[
            "year",
            "month",
            "day",
            "hour",
            "hp_30",
        ],
        na_values=[-1.000],
    )

    df["date"] = pd.to_datetime(
        df["year"].astype(str)
        + "-"
        + df["month"].astype(str)
        + "-"
        + df["day"].astype(str)
    )

    # Pre-filtering the dataframe (by dates) to reduce its size
    df = df[df["date"].between(start[:10], stop[:10])]

    df["datetime"] = pd.to_datetime(
        df["year"].astype(str)
        + "-"
        + df["month"].astype(str)
        + "-"
        + df["day"].astype(str)
        + " "
        + pd.to_datetime(df["hour"] * 3600, unit="s").dt.strftime("%H:%M")
    )

    return (
        df.drop(columns=["year", "month", "day", "date", "hour"])
        .set_index("datetime")
        .loc[start:stop]
    )
