from pathlib import Path
from typing import Literal, Union

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import pvlib

from src.io import read_time_series
from src.var import LATITUDE, LONGITUDE, ALTITUDE, DATA_IN


def resample_time_series(
    df: pd.DataFrame,
    aggregation_function: Union[
        Literal["mean", "median", "max"], dict[str, Union[str, list[str]]]
    ],
    time_interval: str = "30T",
    on_column: str = None,
) -> pd.DataFrame:
    """
    Convenience function to resample time series with a given aggregation method

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be resampled
    aggregation_function : Literal["mean", "median", "max"], dict[str, Union[str, list[str]]]
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
    series: pd.Series, window: int = 10, n_categories: int = 3, zero_phase: bool = True
) -> tuple[pd.Series, np.ndarray]:
    """
    Convenience function which filters the time series with a exponentially-weighted
    moving average (EMA) or with a forward-backward (FB) EMA (if `zero_phase` is set
    to True); the function then fits a K-Means algorithm and returns the smoothed
    values along with the estimated labels (categories)

    Parameters
    ----------
    series : pd.Series
        Time series to filter and categorise
    window : int, optional
        Time window steps for smoothing, by default 10
    n_categories : int, optional
        Number of categories to extract, by default 3
    zero_phase : bool, optional
        Whether or not to make the filter zero-phase (i.e., a non-causal filter),
        by default True; if the filter is zero-phase, the smoothed series is not
        appropriate for prediction due to data leakage from future values

    Returns
    -------
    tuple[pd.Series, np.ndarray]
        Smoothed series, estimated labels (categories)
    """
    filtered_series = series.ewm(span=window).mean()

    if zero_phase:
        # Backward filtering as well
        filtered_series = filtered_series[::-1].ewm(span=window).mean()[::-1]

    zeroes = filtered_series.lt(0).sum() > 0

    # Evaluate log-differences (with an offset in case of negative values)
    if not zeroes:
        log_diff = np.diff(np.log1p(filtered_series.values))
    else:
        log_diff = np.diff(
            np.log1p(filtered_series.values + abs(filtered_series.min()))
        )

    # Fit the clustering model
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

    return filtered_series, labels


def preprocess_ionosonde_data(
    station_name: str,
    aggregation_function: Union[
        Literal["mean", "median", "max"], dict[str, Union[str, list[str]]]
    ],
    resample_time_interval: str = "30T",
) -> pd.DataFrame:
    """
    Convenience function that loads the specified ionosonde data, resamples it and applies some other standardisation transformations

    Parameters
    ----------
    station_name : str
        Name of the ionosonde, e.g. JR055
    aggregation_function : Union[Literal["mean", "median", "max"], dict[str, Union[str, list[str]]]]
        Aggregation function to use for resampling the original time series
    resample_time_interval : str, optional
        String format (according to https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), by default "30T"

    Returns
    -------
    pd.DataFrame
    """
    path = Path(DATA_IN, f"{station_name}.csv")
    station_abbreviation = path.stem[:2].lower()

    # Load raw ionosonde data
    df_ionosonde = read_time_series(
        path,
        column_names=[
            "spectral_contribution",
            "velocity",
            "azimuth",
            "local_warning_level",
            "datetime",
        ],
        usecols=[12, 13, 14, 15, 18],
    )

    # Resample the time series
    df_ionosonde_30 = resample_time_series(
        df=df_ionosonde,
        aggregation_function=aggregation_function,
        time_interval=resample_time_interval,
    )

    # Categorisation of the local warning level (TrL)
    conds = [
        df_ionosonde_30["local_warning_level"].eq(0),
        df_ionosonde_30["local_warning_level"].eq(1),
        df_ionosonde_30["local_warning_level"].eq(2),
        df_ionosonde_30["local_warning_level"].eq(3),
        df_ionosonde_30["local_warning_level"].eq(4),
        df_ionosonde_30["local_warning_level"].eq(5),
    ]
    choices = ["no data", "quiet", "weak", "moderate", "strong", "very strong"]
    df_ionosonde_30["local_warning_level"] = np.select(
        condlist=conds, choicelist=choices, default="X"
    )

    # Adding suffixes to all columns
    df_ionosonde_30.columns = [
        col_ + f"_{station_abbreviation}" for col_ in df_ionosonde_30.columns
    ]

    return df_ionosonde_30
