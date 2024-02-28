import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
import shap

from var import MODEL_PATH


def load_model() -> CatBoostClassifier:
    return CatBoostClassifier().load_model(MODEL_PATH)


def get_shap_values(X: pd.DataFrame) -> tuple[shap.TreeExplainer, np.ndarray]:
    model = load_model()
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(X)
    return explainer, shap_vals
