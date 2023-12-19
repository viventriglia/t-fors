TODO Decomposizione della serie temporale (STL, pyquant), oltre a (P)ACF
TODO Profiling dei dati con stumpy?
TODO Sperimentare con [Nixtla](https://www.nixtla.io/open-source) per il forecast e l'analisi della serie storica [esempio](https://nixtlaverse.nixtla.io/mlforecast/docs/getting-started/end_to_end_walkthrough.html)
- [x] Individuare il metodo più appropriato per train-test split, evaluation metric ed eventuale stratificazione --> TimeSeriesSplit (sklearn) and [cross validation in Nixtla](https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/crossvalidation.html)
TODO MLFlow per tracciare gli esperimenti di ML ([in congiunzione con Optuna](https://mlflow.org/docs/latest/traditional-ml/hyperparameter-tuning-with-child-runs/notebooks/hyperparameter-tuning-with-child-runs.html)); [API per CB](https://mlflow.org/docs/latest/python_api/mlflow.catboost.html)
- [x] Tuning degli iperparametri [con Optuna](https://forecastegy.com/posts/catboost-hyperparameter-tuning-guide-with-optuna/); [altri parametri da provare a ottimizzare](https://catboost.ai/en/docs/concepts/parameter-tuning#l2-reg), esempi [dal repo di Optuna](https://github.com/optuna/optuna-examples/tree/main/catboost)
TODO Calibrazione del classificatore! [sklearn doc](https://scikit-learn.org/stable/modules/calibration.html)
TODO Confusion matrix

From 1st Review Meeting:
TODO consider f10.7 from the previous day
- [x] rate of change in IL might be helpful (suggestion by Hermann Opgenoorth); we could consider a decomposition according to the first derivative of the geomagnetic indices

Feedback:
- [x] imposta 350km di altitudine per SZA
TODO Plot delle feature e del target entro una finestra di ±3h
TODO Integrare SMR e HP_30
TODO Derivata prima categorizzata di IE --> k-means on FB-EMA
TODO Integra IL e IU con derivata prima categorizzata