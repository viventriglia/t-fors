.\.venv\Scripts\activate.ps1

poetry run mlflow server --default-artifact-root mlruns/ --host 0.0.0.0 --port 5000