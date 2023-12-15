from typing import Literal

import pandas as pd
from catboost import CatBoostClassifier


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
