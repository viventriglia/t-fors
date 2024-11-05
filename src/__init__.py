from pathlib import Path

from dotenv import dotenv_values

# Solar Zenith Angle
LATITUDE = 50.110656
LONGITUDE = 8.682526
ALTITUDE = 350_000

# Data
DATA_IN = Path("..", "data", "in")

# MLFlow
ML_SERVER_URI = "http://localhost:5000"
EXPERIMENT_NAME = "CatBoost"
ML_MODEL_COLS = [
    "ie_fix",
    "ie_variation",
    "ie_mav_3h",
    "ie_mav_12h",
    "iu_fix",
    "iu_variation",
    "iu_mav_3h",
    "iu_mav_12h",
    "hf",
    "hf_mav_2h",
    "f_107_adj",
    "hp_30",
    "smr",
    "solar_zenith_angle",
    "newell",
    "bz",
    "vx",
    "rho",
    "spectral_contribution_at",
    "spectral_contribution_ff",
    "spectral_contribution_jr",
    "spectral_contribution_pq",
    "spectral_contribution_ro",
    "spectral_contribution_vt",
    "azimuth_at",
    "azimuth_ff",
    "azimuth_jr",
    "azimuth_pq",
    "azimuth_ro",
    "azimuth_vt",
    "velocity_at",
    "velocity_ff",
    "velocity_jr",
    "velocity_pq",
    "velocity_ro",
    "velocity_vt",
]

# FastAPI
FASTAPI_SUMMARY = """Traveling Ionospheric Disturbances Forecasting System
(T-FORS), funded by the European Community, Horizon Europe
"""
FASTAPI_DESC = """ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_)."""
FASTAPI_CONTACT = {
    "name": "The T-FORS Project",
    "url": "https://t-fors.eu/",
}
FASTAPI_LICENSE = {
    "name": "MIT License",
    "url": "https://opensource.org/license/mit",
}
