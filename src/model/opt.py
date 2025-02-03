import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import TimeSeriesSplit
import optuna

from model.model import instantiate_and_fit_model


def objective(
    trial: optuna.Trial,
    X: pd.DataFrame,
    y: pd.Series,
    cv: TimeSeriesSplit,
    params: dict,
) -> float:
    """
    Convenience function performing Bayesian optimisation on a set of model hyper-parameters

    Parameters
    ----------
    trial : optuna.Trial
        Trial object, namely a process of evaluating an objective function
    X : pd.DataFrame
        Full features DataFrame, to be split according to the cv object
    y : pd.Series
        Full target Series, to be split according to the cv object
    cv : TimeSeriesSplit
        Time Series cross-validator object
    params : dict
        "Static" hyper-parameters of the model, not subject to optimisation

    Returns
    -------
    float
        Average F1 score after cross validation
    """
    # Hyper-parameters subject to optimisation
    params_to_be_optimised = {
        "iterations": trial.suggest_int("iterations", 100, 5_000),
        "learning_rate": trial.suggest_float("learning_rate", 0.0001, 0.1),
        "depth": trial.suggest_int("depth", 2, 9),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 100),
        "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 0.01, 10),
        "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1, 5),
    }
    params.update(params_to_be_optimised)

    f1_scores = []

    # Cross-validated training
    for train_idx, test_idx in cv.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model = instantiate_and_fit_model(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            loss_function="Logloss",
            params=params,
        )

        y_pred = model.predict(X_test)
        f1_scores.append(f1_score(y_test, y_pred))

    return np.mean(f1_scores)
