from contextlib import asynccontextmanager
from datetime import datetime
import logging

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError
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
from model import (
    MODEL_PATH,
    THRESH_BALAN,
    THRESH_HPREC,
    THRESH_HSENS,
)
from model.calibration import get_venn_abers_score, X_cal, y_cal
from backend.utils import get_real_time_data, get_availability_score
from backend.validation import InputDataModel, OutputDataModel, ResponseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # ML model
        logger.info("Loading the CatBoost model...")
        from_file = cb.CatBoostClassifier()
        model = from_file.load_model(MODEL_PATH)
        logger.info("Model loaded successfully")

        # Assets storage
        app.state.model = model
    except Exception as e:
        logger.error(f"Error during asset loading: {e}")
        raise RuntimeError(f"Error loading assets: {e}")
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


@app.get("/", include_in_schema=False)
def root():
    return {"message": "The T-FORS LSTID forecasting service is up and running"}


@app.get("/data", tags=["data"], summary="Retrieve near real-time data")
async def get_data():
    try:
        return get_real_time_data().fillna("").to_dict("index")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")


@app.post(
    "/predict",
    tags=["predict"],
    summary="Get predictions based on near real-time data using a pre-trained model",
    response_model=OutputDataModel,
)
def predict(model=Depends(get_model)):
    try:
        df = get_real_time_data()
        # Check availability of near real-time data
        input_availability_score, input_availability_thr = get_availability_score(df)
        data_dict = df.to_dict(orient="records")[0]

        try:
            validated_data = InputDataModel(**data_dict)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {e}")

        df_validated = pd.DataFrame([validated_data.model_dump()])
        # Raw CatBoost score
        prediction_score = model.predict_proba(df_validated)
        # Calibrated score
        prediction_calib = get_venn_abers_score(
            p_cal=model.predict_proba(X_cal),
            y_cal=y_cal.values,
            p_test=prediction_score,
        )

        if isinstance(prediction_score, (list, np.ndarray)):
            prediction_score = float(prediction_score[:, 1][0])
        elif isinstance(prediction_score, (int, float)):
            prediction_score = float(prediction_score[:, 1])
        else:
            raise HTTPException(status_code=500, detail="Unexpected prediction format")

        # Operating modes (classification)
        prediction_hprec = 1 if prediction_score > THRESH_HPREC else 0
        prediction_balan = 1 if prediction_score > THRESH_BALAN else 0
        prediction_hsens = 1 if prediction_score > THRESH_HSENS else 0

        input_data = df.fillna("").replace("", None).to_dict(orient="records")[0]
        output_data = {
            "datetime_ref": df.index[0],
            "datetime_run": datetime.utcnow(),
            "prediction_score": np.round(prediction_score, 3),
            "prediction_calib": np.round(prediction_calib, 3),
            "prediction_hprec": prediction_hprec,
            "prediction_balan": prediction_balan,
            "prediction_hsens": prediction_hsens,
            "input_availability_score": input_availability_score,
            "input_availability_alert": input_availability_thr,
            **input_data,
        }
        return OutputDataModel(**output_data)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
