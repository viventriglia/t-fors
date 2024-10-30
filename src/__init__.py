from pathlib import Path

from dotenv import dotenv_values

# Solar Zenith Angle
LATITUDE = 50.110656
LONGITUDE = 8.682526
ALTITUDE = 350_000

# Data
DATA_IN = Path("..", "data", "in")

# SSL certificates
TECHTIDE_CERT_PATH = dotenv_values("../.env.secret")["TECHTIDE_CERT_PATH"]

# MLFlow
ML_SERVER_URI = "http://localhost:5000"
EXPERIMENT_NAME = "CatBoost"

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
