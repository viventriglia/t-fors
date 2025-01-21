import requests
from io import StringIO, BytesIO
from pathlib import Path
from typing import Literal
import zipfile
from urllib.parse import quote
import re

import pandas as pd
import numpy as np

from backend import L1_DIST, BSN_DIST


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


def get_gfz_f107(end_date: str = None, last_n_days: int = 10) -> pd.DataFrame:
    """
    Convenience function that downloads F10.7 (adjusted) within a specified time
    interval as collected by GFZ German Research Centre for Geosciences

    Parameters
    ----------
    end_date : str, optional
        End date of the time interval in 'YYYY-MM-DD' format, by default None
        If None, the function returns the last `last_n_days` days retrieved
    last_n_days : int, optional
        Number of days to return from the end of the dataset, by default 10

    Returns
    -------
    pd.DataFrame
    """
    response = requests.get(
        "https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_Ap_SN_F107_nowcast.txt"
        # "https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_Ap_SN_F107_since_1932.txt"
    )
    if response.status_code != 200:
        raise Exception(f"Error while downloading data: {response.status_code}")

    data = StringIO(response.text)

    data_lines = []
    for line in data:
        # Skipping comments at the top
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

    df = df.drop(columns=["year", "month", "day"]).set_index("date").ffill()

    if end_date is None:
        return df.tail(last_n_days)
    else:
        end_date = pd.to_datetime(end_date)
        return df.loc[:end_date].tail(last_n_days)


def _get_gfz_hp30(start: str, stop: str) -> pd.DataFrame:
    """
    Convenience function that downloads Hp30 within a specified time interval
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

    data_lines = []
    for line in data:
        # Skipping comments at the top
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


def get_gfz_hp30(end_datetime: str = None, last_n_days: int = 1) -> pd.DataFrame:
    """
    Convenience function that downloads Hp30 within a specified time interval
    as produced by GFZ German Research Centre for Geosciences

    Parameters
    ----------
    end_datetime : str, optional
        End date-time in 'YYYY-MM-DD HH:MM:SS' format, by default None
        If None, the function returns the last `last_n_days` days retrieved
    last_n_days : int, optional
        Number of days to return from the end of the dataset, by default 1

    Returns
    -------
    pd.DataFrame
    """
    response = requests.get(
        "https://www-app3.gfz-potsdam.de/kp_index/Hp30_ap30_nowcast.txt"
    )
    if response.status_code != 200:
        raise Exception(f"Error while downloading data: {response.status_code}")

    data = StringIO(response.text)

    data_lines = []
    for line in data:
        # Skipping comments at the top
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

    df["datetime"] = pd.to_datetime(
        df["year"].astype(str)
        + "-"
        + df["month"].astype(str)
        + "-"
        + df["day"].astype(str)
        + " "
        + pd.to_datetime(df["hour"] * 3600, unit="s").dt.strftime("%H:%M")
    )

    # Here it is important to remove NaN values, which correspond to future
    # values (not yet recorded); if they remained, we would still have
    # last_n_days, but with several NaN values
    df = (
        df.drop(columns=["year", "month", "day", "hour"]).dropna().set_index("datetime")
    )

    last_n_half_hours = 2 * 24 * last_n_days
    if end_datetime is None:
        return df.tail(last_n_half_hours)
    else:
        end_datetime = pd.to_datetime(end_datetime)
        return df.loc[:end_datetime].tail(last_n_half_hours)


def _get_noaa_l1(
    end_propagated_datetime: str, include_newell: bool = True
) -> pd.DataFrame:
    """
    Convenience function to retrieve magnetic field and solar wind data from
    NOAA, collected at the L1 Lagrange point and projected to estimate
    conditions at Earth's bow shock

    Parameters
    ----------
    end_propagated_datetime : str
        End date-time in 'YYYY-MM-DD HH:MM:SS' format
    include_newell : bool, optional
        If True, calculates the Newell coupling function, which estimates
        the energy transfer from solar wind to the magnetosphere, by default True

    Returns
    -------
    pd.DataFrame
    """
    cols = ["propagated_time_tag", "density", "by", "bz", "speed"]

    df = pd.read_json(
        "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json",
        convert_dates=False,
    )

    df.columns = df.iloc[0]
    df = df[1:][cols].reset_index(drop=True)

    for col_ in cols:
        if "time_" in col_:
            df[col_] = pd.to_datetime(df[col_])
        else:
            df[col_] = pd.to_numeric(df[col_])

    # Assuming speed ~ |vx| -- gulp!
    df["vx"] = -df["speed"]

    df = df.rename(
        columns={
            "propagated_time_tag": "datetime",
            "density": "rho",
        }
    )

    if include_newell:
        df["newell"] = (
            df["speed"] ** (4 / 3)
            * (df["by"] ** 2 + df["bz"] ** 2) ** (1 / 3)
            * (np.sin(np.arctan((df["by"].div(df["bz"]).abs())) / 2) ** (8 / 3))
        ).round(1)

    return df[df["datetime"].lt(end_propagated_datetime)].set_index("datetime")


def get_noaa_l1(end_propagated_datetime: str) -> pd.DataFrame:

    try:
        response = requests.get(
            "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
        )
        df_mag = pd.DataFrame(response.json()[1:], columns=response.json()[0])
        response = requests.get(
            "https://services.swpc.noaa.gov/products/solar-wind/plasma-6-hour.json"
        )
        df_plasma = pd.DataFrame(response.json()[1:], columns=response.json()[0])
    except:
        raise Exception(
            f"Error in retrieving solar wind data. Status code: {response.status_code}. Text: {response.text}"
        )

    df = df_mag.merge(df_plasma, on="time_tag", how="outer")
    df.index = pd.Index(pd.to_datetime(df.pop("time_tag")), name="datetime_measure")
    df = df.apply(pd.to_numeric).reset_index()

    df.columns = df.columns.str.removesuffix("_gsm")

    df["seconds_to_arrive"] = np.round((L1_DIST - BSN_DIST) / df["speed"])
    df["datetime"] = df["datetime_measure"] + pd.to_timedelta(
        df["seconds_to_arrive"], unit="s"
    )

    df["newell"] = (
        df["speed"] ** (4 / 3)
        * (df["by"] ** 2 + df["bz"] ** 2) ** (1 / 3)
        * (np.sin(np.arctan((df["by"].div(df["bz"]).abs())) / 2) ** (8 / 3))
    ).round(1)

    return (
        df[df["datetime"].lt(end_propagated_datetime)]
        .drop(
            columns=[
                "datetime_measure",
                "seconds_to_arrive",
                "lon",
                "lat",
                "temperature",
                "bx",
                "bt",
            ]
        )
        .rename(columns={"density": "rho"})
        .set_index("datetime")
    )


def get_noaa_dst(end_datetime: str) -> pd.DataFrame:
    """
    Convenience function to retrieve Disturbance Storm Time (Dst) data from
    NOAA, derived from a network of near-equatorial geomagnetic observatories
    that measures the intensity of the globally symmetrical equatorial
    electrojet (the "ring current")

    Parameters
    ----------
    end_datetime : str
        End date-time in 'YYYY-MM-DD HH:MM:SS' format

    Returns
    -------
    pd.DataFrame
    """
    cols = ["time_tag", "dst"]

    df = pd.read_json(
        "https://services.swpc.noaa.gov/products/kyoto-dst.json",
        convert_dates=False,
    )

    df.columns = df.iloc[0]
    df = df[1:][cols].reset_index(drop=True)

    for col_ in cols:
        if "time_" in col_:
            df[col_] = pd.to_datetime(df[col_])
        else:
            df[col_] = pd.to_numeric(df[col_])

    df = df.rename(
        columns={
            "time_tag": "datetime",
        }
    )

    return df[df["datetime"].lt(end_datetime)].set_index("datetime")


def get_fmi_iu_ie() -> pd.DataFrame:
    """
    Convenience function to get IU and IE derived from IMAGE magnetometers
    as curated by FMI (https://space.fmi.fi/image/realtime/eurisgic/)

    Returns
    -------
    pd.DataFrame
    """
    response = requests.get(
        "https://space.fmi.fi/image/realtime/eurisgic/realtime_iu_il.txt"
    )
    if response.status_code != 200:
        raise Exception(f"Error while downloading data: {response.status_code}")

    data = StringIO(response.text)

    data_lines = []
    for line in data:
        # Skipping comments at the top
        if not line.startswith("%"):
            data_lines.append(line)

    df = pd.read_csv(
        StringIO("".join(data_lines)),
        sep="\s+",
        header=None,
        usecols=[0, 1, 2, 3, 4, 5, 6, 7],
        names=[
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
            "iu",
            "il",
        ],
    )

    df["datetime"] = pd.to_datetime(
        df["year"].astype(str)
        + "-"
        + df["month"].astype(str)
        + "-"
        + df["day"].astype(str)
        + " "
        + df["hour"].astype(str)
        + ":"
        + df["minute"].astype(str)
        + ":"
        + df["second"].astype(str)
    )

    # Evaluating the proper electrojet indicator, IE
    df["ie"] = df["iu"] - df["il"]

    return df.drop(
        columns=["year", "month", "day", "hour", "minute", "second", "il"]
    ).set_index("datetime")
