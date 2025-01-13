from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, ValidationError
import pandas as pd
import numpy as np
import catboost as cb

from backend import (
    FASTAPI_SUMMARY,
    FASTAPI_DESC,
    FASTAPI_CONTACT,
    FASTAPI_LICENSE,
    FASTAPI_FAVICON_PATH,
)
from model import MODEL_PATH, THRESH_BALAN, THRESH_HPREC, THRESH_HSENS
from backend.utils import get_real_time_data


class InputDataModel(BaseModel):
    """(Pydantic-based) schema of model input data"""

    ie_fix: Optional[float] = Field(
        description="Auroral-zone magnetic activity produced by enhanced ionospheric currents flowing below and within the auroral oval in the sector covered by the FMI-IMAGE magnetometer network"
    )
    ie_variation: Optional[int] = Field(
        description="Change in the IE index (increase, decrease, stationary)"
    )
    ie_mav_3h: Optional[float] = Field(
        description="IE exponential moving averages within 3-hours window"
    )
    ie_mav_12h: Optional[float] = Field(
        description="IE exponential moving averages within 12-hours window"
    )
    iu_fix: Optional[float] = Field(
        description="Strongest current intensities of the eastward auroral electrojets in the sector covered by the FMI-IMAGE magnetometer network"
    )
    iu_variation: Optional[int] = Field(
        description="Change in the IE index (increase, decrease, stationary)"
    )
    iu_mav_3h: Optional[float] = Field(
        description="IE exponential moving averages within 3-hours window"
    )
    iu_mav_12h: Optional[float] = Field(
        description="IE exponential moving averages within 12-hours window"
    )
    hf: Optional[float] = Field(
        description="High-Frequency interferometry (HF-INT) index, identifying activity over the European network of ionosondes"
    )
    hf_mav_2h: Optional[float] = Field(
        description="HF-INT exponential moving averages within 2-hours window"
    )
    f_107_adj: Optional[float] = Field(
        description="Solar radio flux at 10.7 cm (2800 MHz)"
    )
    hp_30: Optional[float] = Field(description="Half-hourly geomagnetic index")
    dst: Optional[float] = Field(
        description="Disturbance-storm-time index, a measure of the severity of the geomagnetic storm"
    )
    solar_zenith_angle: Optional[float] = Field(
        description="Angle between the local zenith (i.e. directly above the point on the ground) and the line of sight from that point to the Sun"
    )
    newell: Optional[float] = Field(
        description="Coupling function which quantifies the energy transfer from the magnetosphere to the ionosphere"
    )
    bz: Optional[float] = Field(
        description="Strength of the interplanetary magnetic field in a north/south direction"
    )
    speed: Optional[float] = Field(description="Solar wind flux radial velocity")
    rho: Optional[float] = Field(description="Solar wind flux density")
    spectral_contribution_at: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Athens)"
    )
    spectral_contribution_ff: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Fairford)"
    )
    spectral_contribution_jr: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Juliusruh)"
    )
    spectral_contribution_pq: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Průhonice)"
    )
    spectral_contribution_ro: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Rome)"
    )
    spectral_contribution_vt: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (San Vito)"
    )
    azimuth_at: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Athens)"
    )
    azimuth_ff: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Fairford)"
    )
    azimuth_jr: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Juliusruh)"
    )
    azimuth_pq: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Průhonice)"
    )
    azimuth_ro: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Rome)"
    )
    azimuth_vt: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (San Vito)"
    )
    velocity_at: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Athens)"
    )
    velocity_ff: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Fairford)"
    )
    velocity_jr: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Juliusruh)"
    )
    velocity_pq: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Průhonice)"
    )
    velocity_ro: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Rome)"
    )
    velocity_vt: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (San Vito)"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        from_file = cb.CatBoostClassifier()
        model = from_file.load_model(MODEL_PATH)
        app.state.model = model
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
    yield


def get_model(request: Request):
    model = request.app.state.model
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return model


app = FastAPI(
    title="T-FORS",
    summary=FASTAPI_SUMMARY,
    description=FASTAPI_DESC,
    contact=FASTAPI_CONTACT,
    license_info=FASTAPI_LICENSE,
    lifespan=lifespan,
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(FASTAPI_FAVICON_PATH)


@app.get("/", tags=["health check"])
def root():
    return {"message": "The T-FORS LSTID forecasting service is up and running"}


@app.get("/data", tags=["data"])
async def get_data():
    try:
        return get_real_time_data().fillna("").to_dict("index")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")


@app.post("/predict", tags=["predict"], response_model=InputDataModel)
def predict(model=Depends(get_model)):
    try:
        df = get_real_time_data()
        data_dict = df.to_dict(orient="records")[0]

        try:
            validated_data = InputDataModel(**data_dict)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {e}")

        df_validated = pd.DataFrame([validated_data.model_dump()])
        prediction_score = model.predict_proba(df_validated)[:, 1]

        if isinstance(prediction_score, (list, np.ndarray)):
            prediction_score = float(prediction_score[0])
        elif isinstance(prediction_score, (int, float)):
            prediction_score = float(prediction_score)
        else:
            raise HTTPException(status_code=500, detail="Unexpected prediction format")

        prediction_hprec = 1 if prediction_score > THRESH_HPREC else 0
        prediction_balan = 1 if prediction_score > THRESH_BALAN else 0
        prediction_hsens = 1 if prediction_score > THRESH_HSENS else 0

        return {
            "datetime": df.index[0],
            "prediction_score": np.round(prediction_score, 3),
            "prediction_hprec": prediction_hprec,
            "prediction_balan": prediction_balan,
            "prediction_hsens": prediction_hsens,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
