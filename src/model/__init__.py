from pathlib import Path

MODEL_PATH = Path(
    "assets",
    "models",
    # "836438889763744696",
    # "47379e58abff4b18989898a5b6ecbe08",
    "model.cb",
)
CALIB_X_DATA_PATH = Path(
    "assets",
    "data",
    "X_cal.pkl",
)
CALIB_Y_DATA_PATH = Path(
    "assets",
    "data",
    "y_cal.pkl",
)

THRESH_HPREC = 0.836
THRESH_BALAN = 0.636
THRESH_HSENS = 0.476
