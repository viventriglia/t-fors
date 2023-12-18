TODO Decomposizione della serie temporale (STL, pyquant), oltre a (P)ACF
TODO Profiling dei dati con stumpy?
TODO Sperimentare con [Nixtla](https://www.nixtla.io/open-source) per il forecast e l'analisi della serie storica [esempio](https://nixtlaverse.nixtla.io/mlforecast/docs/getting-started/end_to_end_walkthrough.html)
- [x] Individuare il metodo più appropriato per train-test split, evaluation metric ed eventuale stratificazione --> TimeSeriesSplit (sklearn) and [cross validation in Nixtla](https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/crossvalidation.html)
TODO mlflow per tracciare gli esperimenti di ML ([in congiunzione con Optuna](https://mlflow.org/docs/latest/traditional-ml/hyperparameter-tuning-with-child-runs/notebooks/hyperparameter-tuning-with-child-runs.html))
- [x] [has_time parameter](https://catboost.ai/en/docs/references/training-parameters/common#has_time) in CatBoost
TODO Tuning degli iperparametri [con Optuna](https://forecastegy.com/posts/catboost-hyperparameter-tuning-guide-with-optuna/)
TODO Calibrazione del classificatore! [sklearn doc](https://scikit-learn.org/stable/modules/calibration.html)

From 1st Review Meeting:
TODO 0 means no data (impute nan), 0.1 means no activity; I would model that with categories: NaN, no activity, low and high activity
TODO consider f10.7 from the previous day
TODO rate of change in IL might be helpful (suggestion by Hermann Opgenoorth); we could consider a decomposition according to the first derivative of the geomagnetic indices
- [x] consider solar zenith angle instead of local time (we will rely on [ephem](https://pypi.org/project/ephem/) library)

Feedback:
TODO imposta 350km di altitudine per SZA
TODO Integrare SMR e HP_30
TODO Derivata prima categorizzata di IE --> k-means on FB-EMA
TODO Integra IL e IU con derivata prima categorizzata