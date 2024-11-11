from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, Request, HTTPException
from pydantic import BaseModel, Field, ValidationError
import pandas as pd
import numpy as np
import mlflow

from src import FASTAPI_SUMMARY, FASTAPI_DESC, FASTAPI_CONTACT, FASTAPI_LICENSE
from src.api.utils import get_real_time_data


class InputDataModel(BaseModel):
    """Pydantic-based data model"""

    ie_fix: Optional[float]  # = Field(description="AAA")
    ie_variation: Optional[int]  # TODO
    ie_mav_3h: Optional[float]
    ie_mav_12h: Optional[float]
    iu_fix: Optional[float]
    iu_variation: Optional[int]
    iu_mav_3h: Optional[float]
    iu_mav_12h: Optional[float]
    hf: Optional[float]
    hf_mav_2h: Optional[float]
    f_107_adj: Optional[float]
    hp_30: Optional[float]
    smr: Optional[float]
    solar_zenith_angle: Optional[float]
    newell: Optional[float]
    bz: Optional[float]
    vx: Optional[float]
    rho: Optional[float]
    spectral_contribution_at: Optional[float]
    spectral_contribution_ff: Optional[float]
    spectral_contribution_jr: Optional[float]
    spectral_contribution_pq: Optional[float]
    spectral_contribution_ro: Optional[float]
    spectral_contribution_vt: Optional[float]
    azimuth_at: Optional[float]
    azimuth_ff: Optional[float]
    azimuth_jr: Optional[float]
    azimuth_pq: Optional[float]
    azimuth_ro: Optional[float]
    azimuth_vt: Optional[float]
    velocity_at: Optional[float]
    velocity_ff: Optional[float]
    velocity_jr: Optional[float]
    velocity_pq: Optional[float]
    velocity_ro: Optional[float]
    velocity_vt: Optional[float]


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        model = mlflow.catboost.load_model(
            "runs:/47379e58abff4b18989898a5b6ecbe08/model"
        )
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


@app.get("/", tags=["health check"])
def root():
    return {"message": "The T-FORS LSTID forecasting service is up and running"}


@app.get("/data", tags=["data"])
async def get_data():
    try:
        return get_real_time_data().fillna("").to_dict("index")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")


@app.post("/predict", tags=["predict"])
def predict(model=Depends(get_model)):
    try:
        df = get_real_time_data()
        data_dict = df.to_dict(orient="records")[0]

        try:
            validated_data = InputDataModel(**data_dict)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {e}")

        df_validated = pd.DataFrame([validated_data.model_dump()])
        prediction = model.predict(df_validated)

        if isinstance(prediction, (list, np.ndarray)):
            prediction = float(prediction[0])
        elif isinstance(prediction, (int, float)):
            prediction = float(prediction)
        else:
            raise HTTPException(status_code=500, detail="Unexpected prediction format")

        return {"prediction": prediction}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
