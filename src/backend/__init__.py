from pathlib import Path

# Geo-Physical parameters
LATITUDE = 50.110656
LONGITUDE = 8.682526
ALTITUDE = 350_000
L1_DIST = 1_500_000
BSN_DIST = 90_000

# Data
DATA_IN = Path("..", "data", "in")

# MLFlow & FastAPI
ML_SERVER_URI = "http://localhost:5000"
EXPERIMENT_NAME = "CatBoost"
ML_MODEL_COLS = {
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
    "dst": "float",
    "solar_zenith_angle": "float",
    "newell": "float",
    "bz": "float",
    "speed": "float",
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

# FastAPI
FASTAPI_SUMMARY = """
Travelling Ionospheric Disturbances Forecasting System (T-FORS),
funded by the European Community, Horizon Europe
"""
FASTAPI_DESC = """
T-FORS is a near real-time forecasting service that exploits solar and geomagnetic
data to forecast Travelling Ionospheric Disturbances (TIDs). This API currently
offers three endpoints:

- **Health check**: checks that the service is active
- **Data retrieval**: retrieves near real-time data
- **Prediction**: provides predictions based on near real-time data using
 a pre-trained machine learning model
"""
FASTAPI_CONTACT = {
    "name": "The T-FORS Project",
    "url": "https://t-fors.eu/",
}
FASTAPI_LICENSE = {
    "name": "MIT License",
    "url": "https://opensource.org/license/mit",
}
FASTAPI_FAVICON_PATH = Path("assets", "images", "favicon.ico")
