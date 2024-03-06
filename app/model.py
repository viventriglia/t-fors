import streamlit as st
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import MinMaxScaler
import shap
import umap

from var import MODEL_PATH


def load_model() -> CatBoostClassifier:
    return CatBoostClassifier().load_model(MODEL_PATH)


def get_shap_values(X: pd.DataFrame) -> tuple[shap.TreeExplainer, np.ndarray]:
    model = load_model()
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(X)
    return explainer, shap_vals


@st.cache_data(show_spinner=False, max_entries=2)
def evaluate_umap(X: pd.DataFrame, n_comps: int, n_neighbors: int) -> np.ndarray:
    X_sc = MinMaxScaler().fit_transform(X.values)

    umap_ = umap.UMAP(
        n_components=n_comps,
        n_neighbors=n_neighbors,
        min_dist=0.1,
        n_jobs=-1,
        metric="euclidean",
    )

    return umap_.fit_transform(X_sc)
