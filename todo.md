TODO Decomposizione della serie temporale (STL, pyquant), oltre a (P)ACF
- [x] Sperimentare con [Nixtla](https://www.nixtla.io/open-source) per il forecast e l'analisi della serie storica [esempio](https://nixtlaverse.nixtla.io/mlforecast/docs/getting-started/end_to_end_walkthrough.html)
- [x] imposta 350km di altitudine per SZA
- TODO EDA multidimensionale per scoprire possibili pattern: https://facebookresearch.github.io/hiplot/
- TODO improvement of CatBoost hparams after new catalog: take inspiration from [here](https://www.kaggle.com/code/maiernator/exploration-of-baby-data-finetuned-catboost#Motivation-for-engineering-ILLB_R,ILOP_R,ILP_R)
TODO CatBoost doc: https://catboost.ai/en/docs/concepts/python-reference_catboostclassifier_fit (look for incremental) --> va nella direzione dell'incremental learning (od online learning)
"Data assimilation combines observations and models in a way that accounts for the uncertainties in each, while simultaneously respecting certain constraints.  These include the laws of motion of the system through the model equations, and how the measurements physically relate to the system’s variables.  In weather forecasting, recent weather observations are combined with today’s model forecast to obtain a complete picture of the atmosphere now in order to start a new forecast for the days ahead.  Data assimilation is often thought of as a way of keeping a model ‘on the tracks’ by constantly correcting it with fresh observations." (https://research.reading.ac.uk/met-darc/aboutus/what-is-data-assimilation/)
--> prototipo per il progetto --> piano possibile d'implementazione verso un prodotto da includere in servizi e portali di space weather, come quello ESA --> idee di sviluppo per future prosecuzione del progetto

Ebro
L1 parameters, substitute 10_000 with NaN values
use non projected features, but at L1
discussione su data/concept drift --> 2024 HF index not reliable

URSI
PINN loss --> https://github.com/catboost/catboost/blob/master/catboost/tutorials/custom_loss/custom_loss_and_metric_tutorial.ipynb