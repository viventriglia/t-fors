import pickle

from venn_abers import VennAbersCalibrator
from . import CALIB_X_DATA_PATH, CALIB_Y_DATA_PATH


def get_venn_abers_score(p_cal, y_cal, p_test):
    calibrator = VennAbersCalibrator(inductive=True)

    score = calibrator.predict_proba(
        p_cal=p_cal,
        y_cal=y_cal,
        p_test=p_test,
        p0_p1_output=False,
    )

    return score[:, 1]


with open(CALIB_X_DATA_PATH, "rb") as f:
    X_cal = pickle.load(f)

with open(CALIB_Y_DATA_PATH, "rb") as f:
    y_cal = pickle.load(f)
