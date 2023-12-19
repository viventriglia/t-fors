from typing import Literal

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import pvlib

from src.var import LATITUDE, LONGITUDE, ALTITUDE


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
    altitude: float = ALTITUDE,
    **kwargs,
) -> pd.DataFrame:
    """
    Convenience wrapper for solar position data

    Parameters
    ----------
    time : pd.DatetimeIndex
        Must be localized or UTC will be assumed
    columns : list[str], optional
        Solar position attributes to return, by default ["zenith"]
    latitude : float, optional
        Latitude in decimal degrees; positive north of equator, negative to south
    longitude : float, optional
        Longitude in decimal degrees; positive east of prime meridian, negative to west
    altitude : float, optional
        Altitude in metres
    **kwargs
        Other keywords to be passed to the underlying solar position function

    Returns
    -------
    pd.DataFrame
    """
    return pvlib.solarposition.get_solarposition(
        time=time,
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
        **kwargs,  # FIXME is SZA accurate for 350km altitude?
    )[columns]


def get_categories(
    series: pd.Series, window: int = 20, n_categories: int = 3
) -> tuple[pd.Series, np.ndarray]:
    """
    The function filters the time series with a forward-backward (FB) exponential moving average (EMA),
    fits a K-Means clustering algorithm and returns FB-EMA values along with the estimated labels (categories)

    Parameters
    ----------
    series : pd.Series
        Time series to filter and categorise
    window : int, optional
        Time window for smoothing, by default 20
    n_categories : int, optional
        Number of categories to extract, by default 3

    Returns
    -------
    tuple[pd.Series, np.ndarray]
        FB-EMA values, estimated labels (categories)
    """
    # FB filtering with EMA
    f_ema = series.ewm(span=window).mean()
    fb_ema = f_ema[::-1].ewm(span=window).mean()[::-1]

    # Evaluate log-differences and fit the clustering model
    log_diff = np.diff(np.log(fb_ema.values))
    km = KMeans(n_clusters=n_categories, n_init="auto", random_state=42).fit(
        log_diff.reshape(-1, 1)
    )
    lb = km.labels_

    # Change the labels to get some semblance of order
    cluster_centers = km.cluster_centers_.flatten()
    temp = [(cluster_centers[i], i) for i in range(n_categories)]
    temp = sorted(temp, key=lambda x: x[0])

    labels = np.zeros(len(lb), dtype=int)
    for i in range(1, n_categories):
        old_lb = temp[i][1]
        idx = np.where(lb == old_lb)[0]
        labels[idx] = i

    return fb_ema, labels
