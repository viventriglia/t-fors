# T-FORS
Traveling Ionospheric Disturbances Forecasting System (funded by the European Community, Horizon Europe)

## Table of Contents

- [What is it?](#what-is-it)

- [How can I run it?](#how-can-i-run-it)

    - [Run locally 💻](#run-locally-)

    - [Spin up a container 🐋](#spin-up-a-container-)

- [How can I help?](#how-can-i-help)

## What is it?
We aim at the development of a machine-learning-based algorithm to forecast **Large Scale Traveling Ionospheric Disturbances**. The work is carried out within the ["T-FORS - Traveling Ionospheric Disturbances Forecasting System"](https://cordis.europa.eu/project/id/101081835) project.

## How can I run it?

This project can be run either locally or within a Docker container (recommended).
Below are the instructions for both modes.

### Run locally 💻

- First, you need to clone the repo and install **dependencies** via [Poetry](https://python-poetry.org/docs/) with `poetry install`

- Activate a virtual environment

    - There are several virtual environments:
        - one in `./src` (back-end)
        - one in `./app` (front-end)
        - one in `./jupyters` (REPL environment for prototyping)

    - cd into the directory of interest and activate the corresponding environment via `poetry shell`

- To launch a web server and execute **jupyter notebooks**, (on Windows) you can run the `scripts/run-jupyter.ps1` script; otherwise, execute the `poetry run jupyter notebook` command

- To start a [MLflow](https://mlflow.org/) **tracking server**, (on Windows) you can run the `scripts/run-mlflow-ui.ps1` script; the **tracking UI** can be accessed locally by navigating to `http://localhost:5000/`

- To launch the [Streamlit](https://streamlit.io/) **web app**, execute the `streamlit run ./app/0_🏠_Home.py` command

### Spin up a container 🐋

- Clone the repo and ensure that the [Docker](https://docs.docker.com/) daemon is running

- Build a Docker image

    - There are several Dockerfiles:
        - [`./src/Dockerfile`](./src/Dockerfile) (back-end, exposing port 8000)
        - [`./app/Dockerfile`](./app/Dockerfile) (front-end, exposing port 8501)
        - [`./jupyters/Dockerfile`](./jupyters/Dockerfile) (REPL environment for prototyping, exposing port 8890)

    - cd into the directory of interest and build the corresponding image via `docker build -t <image-name> .`

- Run a container and expose it on a preferred port (for example, 8080) via `docker run --rm -p 8080:8501 <image-name>` – or run it using the host's network via `docker run --rm --network host <image-name>`

- To orchestrate the services, you can use [Docker Compose](https://docs.docker.com/compose/)

    - There are several services:
        - `api` (back-end, exposing port 8000)
        - `web-app` (front-end, exposing port 8501)
        - `jupyter` (REPL environment for prototyping, exposing port 8890)

- Run a specific service via `docker compose up --build <service-name>` (omit the `--build` flag if the image is already built) from the project root directory

## How can I help?

Contributions are what make the open source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature_amazing_feature`)
3. Commit your Changes (`git commit -m 'Add some amazing stuff'`)
4. Push to the Branch (`git push origin feature_amazing_feature`)
5. Open a Pull Request

An (hopefully) up-to-date list of things to do can be found [here](https://github.com/viventriglia/t-fors/blob/develop/todo.md?plain=1).