FROM python:3.10-slim

WORKDIR /src

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==1.8.4 && poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--reload"]

# docker run --rm -p 8081:8000 t-fors-api