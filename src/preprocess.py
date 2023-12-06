from typing import Literal

import pandas as pd


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
