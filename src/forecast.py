from typing import Literal

import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import TimeSeriesSplit
import optuna


def instantiate_and_fit_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    loss_function: Literal["Logloss", "CrossEntropy"],
    params: dict,
) -> CatBoostClassifier:
    """
    Convenience wrapper to instantiate and fit a CatBoostClassifier model

    Parameters
    ----------
    X_train : pd.DataFrame
        Data to train the model on
    y_train : pd.Series
        Target variable for training
    X_test : pd.DataFrame
        Data to test the model on
    y_test : pd.Series
        Target variable for testing (ground truth)
    loss_function : str
        Loss function to use for optimization of the classification problem
    params : dict
        Further keyword arguments

    Returns
    -------
    CatBoostClassifier
        Fitted CatBoostClassifier model
    """
    model = CatBoostClassifier(loss_function=loss_function, **params)
    model.fit(X_train, y_train, eval_set=(X_test, y_test), silent=True)
    return model


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
        "depth": trial.suggest_int("depth", 2, 10),
        "od_wait": trial.suggest_int("od_wait", 100, 500),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 100),
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
