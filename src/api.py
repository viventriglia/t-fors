from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
import pandas as pd
import numpy as np
import mlflow


class InputDataModel(BaseModel):
    """Pydantic-based data model"""

    ie_fix: float
    ie_variation: int
    ie_mav_3h: float
    ie_mav_12h: float
    iu_fix: float
    iu_variation: int
    iu_mav_3h: float
    iu_mav_12h: float
    hf: float
    hf_mav_2h: float
    f_107_adj: float
    hp_30: float
    smr: float
    solar_zenith_angle: float
    newell: float
    bz: float
    vx: float
    rho: float
    spectral_contribution_at: float
    spectral_contribution_ff: float
    spectral_contribution_jr: float
    spectral_contribution_pq: float
    spectral_contribution_ro: float
    spectral_contribution_vt: float
    azimuth_at: float
    azimuth_ff: float
    azimuth_jr: float
    azimuth_pq: float
    azimuth_ro: float
    azimuth_vt: float
    velocity_at: float
    velocity_ff: float
    velocity_jr: float
    velocity_pq: float
    velocity_ro: float
    velocity_vt: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    model = mlflow.catboost.load_model("runs:/47379e58abff4b18989898a5b6ecbe08/model")
    app.state.model = model
    yield


def get_model(request: Request):
    return request.app.state.model


app = FastAPI(lifespan=lifespan)


@app.get("/", tags=["Check Health"])
def root():
    return {"message": "The T-FORS LSTID forecasting service is running"}


@app.post("/predict", tags=["Predict"])
def predict(input_data: InputDataModel, model=Depends(get_model)):
    # Preprocessing dei dati (da definire)
    df = pd.DataFrame([input_data.model_dump()])
    prediction = model.predict(df)

    if isinstance(prediction, (list, np.ndarray)):
        prediction = float(prediction[0])
    elif isinstance(prediction, (int, float)):
        prediction = float(prediction)
    else:
        raise ValueError("Unexpected prediction format")

    return {"prediction": prediction}
