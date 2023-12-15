from typing import Literal

import pandas as pd
import numpy as np
import pvlib

from src.var import LATITUDE, LONGITUDE


def resample_time_series(
    df: pd.DataFrame,
    aggregation_function: Literal["mean", "median", "max"],
    time_interval: str = "30T",
    on_column: str = None,
) -> pd.DataFrame:
    """
    Convenience function to resample time series with a given aggregation method

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be resampled
    aggregation_function : Literal["mean", "median", "max"]
        Aggregation function to use
    time_interval : str, optional
        String format (according to https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), by default "30T"
    on_column : str, optional
        DataFrame column to use for resampling, by default None (the index is used)

    Returns
    -------
    pd.DataFrame
    """
    return df.resample(time_interval, on=on_column).agg(aggregation_function)


def log_transform(X: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function to apply a log transformation

    Parameters
    ----------
    X : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    return X.apply(np.log1p)


def get_solar_position(
    time: pd.DatetimeIndex,
    columns: Literal[
        "apparent_zenith",
        "zenith",
        "apparent_elevation",
        "elevation",
        "azimuth",
        "equation_of_time",
    ] = ["zenith"],
    latitude: float = LATITUDE,
    longitude: float = LONGITUDE,
) -> pd.DataFrame:
    """
    Convenience wrapper for solar position data

    Parameters
    ----------
    time : pd.DatetimeIndex
        Must be localized or UTC will be assumed
    columns : list[str], optional
        Solar position attributes to return, by default ["zenith"]
    latitude : float
        Latitude in decimal degrees; positive north of equator, negative to south
    longitude : float
        Longitude in decimal degrees; positive east of prime meridian, negative to west

    Returns
    -------
    pd.DataFrame
    """
    return pvlib.solarposition.get_solarposition(time, latitude, longitude)[columns]
