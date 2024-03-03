# T-FORS
Traveling Ionospheric Disturbances Forecasting System (funded by the European Community, Horizon Europe)

## What is that?
We aim at the development of a machine-learning-based algorithm to forecast **Large Scale Traveling Ionospheric Disturbances**. The work is carried out within the ["T-FORS - Traveling Ionospheric Disturbances Forecasting System"](https://cordis.europa.eu/project/id/101081835) project.

## How can I run it?

- First, you need to install **dependencies** via [poetry](https://python-poetry.org/docs/) with `poetry install`

- To launch a web server and execute **jupyter notebooks**, (on Windows) you can run the `scripts/run-jupyter.ps1` script;
  Otherwise, you can activate the virtual environment manually (via `poetry shell`) and then execute the `poetry run jupyter notebook` command

- To start an **[MLflow](https://mlflow.org/) tracking server**, (on Windows) you can run the `scripts/run-mlflow-ui.ps1` script;
  The **tracking UI** can be accessed locally by navigating to `http://localhost:5000/`

- Launch the **web app** via `streamlit run ./app/0_🏠_Home.py`

## How can I help?

An (hopefully) up-to-date list of things to do can be found [here](https://github.com/viventriglia/t-fors/blob/develop/todo.md?plain=1).
