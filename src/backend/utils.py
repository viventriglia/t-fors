from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from src.io import (
    get_techtide_hf,
    get_techtide_ionosondes,
    get_gfz_f107,
    get_gfz_hp30,
    get_noaa_l1,
    get_noaa_dst,
    get_fmi_iu_ie,
)
from src.preprocess import (
    resample_time_series,
    get_moving_avg,
    get_categories,
    get_solar_position,
)
from src import ML_MODEL_COLS


def get_real_time_data() -> pd.DataFrame:
    STOP_UTC_NOW = datetime.utcnow()
    START_UTC = STOP_UTC_NOW - timedelta(hours=6)
    STOP_UTC_NOW = STOP_UTC_NOW.strftime("%Y-%m-%d %H:%M:%S")
    START_UTC = START_UTC.strftime("%Y-%m-%d %H:%M:%S")
    # TechTIDE
    df_hf = get_techtide_hf(start=START_UTC, stop=STOP_UTC_NOW)
    df_hf_30 = resample_time_series(df_hf, aggregation_function="mean").round(2)
    df_hf_30 = get_moving_avg(df_hf_30, ["hf"], [2])
    df_iono = get_techtide_ionosondes(
        START_UTC,
        STOP_UTC_NOW,
        iono_list=["AT138", "FF051", "JR055", "PQ052", "RO041", "VT139"],
    )
    df_iono_30 = resample_time_series(
        df_iono,
        aggregation_function="median",
    ).round(2)
    # GFZ
    df_hp_30 = get_gfz_hp30()
    # NOAA
    df_l1 = get_noaa_l1(end_propagated_datetime=STOP_UTC_NOW)
    df_l1_30 = resample_time_series(
        df_l1,
        aggregation_function="median",
    )
    df_dst = get_noaa_dst(end_datetime=STOP_UTC_NOW)
    df_dst_30 = resample_time_series(df_dst, aggregation_function="median").ffill()
    # FMI
    fmi_cols = ["ie", "iu"]
    df_fmi = get_fmi_iu_ie()
    df_fmi_30 = resample_time_series(df_fmi, aggregation_function="median").round(2)
    df_fmi_30 = get_moving_avg(df_fmi_30, fmi_cols, [3, 12])
    hours = 6
    for col_ in fmi_cols:
        _, labels = get_categories(
            df_fmi_30[col_],
            window=2 * hours,
            zero_phase=False,
        )
        df_fmi_30[f"{col_}_variation"] = np.insert(labels, 0, 0, axis=0)
    # Merge all data
    df_j = (
        df_hf_30.merge(
            df_iono_30,
            how="outer",
            left_index=True,
            right_index=True,
        )
        .merge(
            df_hp_30,
            how="outer",
            left_index=True,
            right_index=True,
        )
        .merge(
            df_l1_30.drop(columns=["by", "speed"]),
            how="outer",
            left_index=True,
            right_index=True,
        )
        .merge(
            df_dst_30,
            how="outer",
            left_index=True,
            right_index=True,
        )
        .merge(
            df_fmi_30,
            how="outer",
            left_index=True,
            right_index=True,
        )
    )
    # Solar and Dst data need to be repeated, since they're provided on a daily/hourly basis
    df_j["dst"] = df_j["dst"].ffill()
    df_j["f_107_adj"] = get_gfz_f107().dropna().tail(1).values[0, 0]
    # Solar zenith angle
    df_j["solar_zenith_angle"] = get_solar_position(
        df_j.index,
        columns="zenith",
        altitude=0,
    ).round(1)

    dtypes = {
        "ie_fix": "float",
        "ie_variation": "int",
        "ie_mav_3h": "float",
        "ie_mav_12h": "float",
        "iu_fix": "float",
        "iu_variation": "int",
        "iu_mav_3h": "float",
        "iu_mav_12h": "float",
        "hf": "float",
        "hf_mav_2h": "float",
        "f_107_adj": "float",
        "hp_30": "float",
        "smr": "float",
        "solar_zenith_angle": "float",
        "newell": "float",
        "bz": "float",
        "vx": "float",
        "rho": "float",
        "spectral_contribution_at": "float",
        "spectral_contribution_ff": "float",
        "spectral_contribution_jr": "float",
        "spectral_contribution_pq": "float",
        "spectral_contribution_ro": "float",
        "spectral_contribution_vt": "float",
        "azimuth_at": "float",
        "azimuth_ff": "float",
        "azimuth_jr": "float",
        "azimuth_pq": "float",
        "azimuth_ro": "float",
        "azimuth_vt": "float",
        "velocity_at": "float",
        "velocity_ff": "float",
        "velocity_jr": "float",
        "velocity_pq": "float",
        "velocity_ro": "float",
        "velocity_vt": "float",
    }

    return (
        df_j.tail(1)
        .rename(columns={"ie": "ie_fix", "iu": "iu_fix", "dst": "smr"})
        .astype(dtypes)[ML_MODEL_COLS]
    )  # FIXME
