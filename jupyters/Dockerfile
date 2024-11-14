FROM python:3.10-slim

WORKDIR /app

COPY ./jupyters/pyproject.toml ./jupyters/poetry.lock ./

RUN pip install poetry==1.8.4 && poetry install --no-root --no-dev

ENV PYTHONPATH /app:/app/src

EXPOSE 8890

ENTRYPOINT ["poetry", "run", "jupyter", "notebook", "--ip", "0.0.0.0", "--port", "8890", "--no-browser", "--notebook-dir=/app", "--allow-root"]
