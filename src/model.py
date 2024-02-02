from typing import Literal

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import TimeSeriesSplit
from catboost import CatBoostClassifier
import mlflow
from mlflow.models import ModelSignature


def get_or_create_experiment(experiment_name: str) -> str:
    """
    Retrieves the ID of an existing MLflow experiment or creates a new one if it doesn't exist.

    Parameters
    ----------
    experiment_name : str
        Name of the MLflow experiment

    Returns
    -------
    str
        ID of the existing or newly created MLflow experiment
    """
    if experiment := mlflow.get_experiment_by_name(experiment_name):
        return experiment.experiment_id
    else:
        return mlflow.create_experiment(experiment_name)


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
        Trained CatBoostClassifier model
    """
    model = CatBoostClassifier(loss_function=loss_function, **params)
    model.fit(X_train, y_train, eval_set=(X_test, y_test), silent=True)
    return model


def start_crossvalidated_run(
    X: pd.DataFrame,
    y: pd.Series,
    time_series_cross_validator: TimeSeriesSplit,
    model_params: dict = None,
    model_signature: ModelSignature = None,
    model_loss: str = "Logloss",
    run_id: str = None,
    log_params: bool = True,
    log_metrics: bool = True,
    log_model: bool = True,
) -> tuple[CatBoostClassifier, tuple[list]]:
    """
    Convenience function to perform cross-validated training of a model.
    It returns an already trained and logged model with MLflow,
    or allows one to be trained and logged from scratch, given the hyper-parameters.

    Parameters
    ----------
    X : pd.DataFrame
        Input features
    y : pd.Series
        Target variable
    time_series_cross_validator : TimeSeriesSplit
        Cross-validator for time series
    model_params : dict, optional
        Hyper-parameters for the model, to be provided if `run_id` is None, by default None
    model_signature : ModelSignature, optional
        Model signature, required for logging the model, by default None
    model_loss : str, optional
        Loss function for the model, by default "Logloss"
    run_id : str, optional
        MLflow identifier of a past run to be loaded, by default None
    log_params : bool, optional
        Whether to log model parameters, by default True
    log_metrics : bool, optional
        Whether to log evaluation metrics, by default True
    log_model : bool, optional
        Whether to log the final model (if `model_signature` is also specified), by default True

    Returns
    -------
    tuple[CatBoostClassifier, tuple[list]]
        Trained model, evaluation metrics for the positive class (F1-score, precision, recall)
    """
    with mlflow.start_run():
        f1s, prs, rcs = [], [], []

        # Check if a MLflow run_id is specified
        if run_id is not None:
            # Retrieve the corresponding model
            cat_model = mlflow.catboost.load_model(f"runs:/{str(run_id)}/model")

            for train_idx, test_idx in time_series_cross_validator.split(X):
                X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

                y_pred = cat_model.predict(X_test)
                # Evaluate in-fold metrics
                p, r, f, _ = precision_recall_fscore_support(y_test, y_pred)
                f1s.append(f[1])
                prs.append(p[1])
                rcs.append(r[1])
        else:
            # Train a model from scratch
            for i, (train_idx, test_idx) in enumerate(
                time_series_cross_validator.split(X)
            ):
                X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

                cat_model = instantiate_and_fit_model(
                    X_train=X_train,
                    y_train=y_train,
                    X_test=X_test,
                    y_test=y_test,
                    loss_function=model_loss,
                    params=model_params,
                )
                # Check if h-params need to be logged
                if log_params:
                    # See GitHub issue #8044 (MLflow) to understand why we need i
                    params = {
                        f"{param}_{i}": value
                        for param, value in cat_model.get_all_params().items()
                    }
                    mlflow.log_params(params)

                y_pred = cat_model.predict(X_test)
                # Evaluate in-fold metrics
                p, r, f, _ = precision_recall_fscore_support(y_test, y_pred)
                f1s.append(f[1])
                prs.append(p[1])
                rcs.append(r[1])
                # Check if metrics need to be logged
                if log_metrics:
                    mlflow.log_metrics(
                        {
                            "f1_0": f[0],
                            "precision_0": p[0],
                            "recall_0": r[0],
                            "f1_1": f[1],
                            "precision_1": p[1],
                            "recall_1": r[1],
                        }
                    )
            # Check if model needs to be logged
            if log_model and model_signature is not None:
                mlflow.catboost.log_model(cat_model, "model", signature=model_signature)

    return cat_model, (f1s, prs, rcs)


def evaluate_crossvalidated_metrics(
    metrics: dict,
    weights: list = None,
) -> None:
    """
    Evaluate and display summary statistics for cross-validated model

    Parameters
    ----------
    metrics : dict
        Dictionary containing metric names as keys and corresponding metric values
        from cross-validation as values
    weights : list, optional
        List of weights to compute weighted averages of metrics, by default None and
        unweighted averages are printed
    """
    if weights is None:
        for name, values in metrics.items():
            print(
                f"Achieved {name}:\t{np.mean(values):.2f} ± {np.std(values, ddof=1):.2f}"
            )
    else:
        for name, values in metrics.items():
            values_w = sum(val_ * w_ for val_, w_ in zip(values, weights)) / sum(
                weights
            )
            print(
                f"Achieved {name} (weighted):\t{np.mean(values_w):.2f} ± {np.std(values, ddof=1):.2f}"
            )
