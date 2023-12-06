from pathlib import Path

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
