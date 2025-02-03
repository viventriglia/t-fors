FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==1.8.4 && poetry install --no-root --no-dev

COPY . .

EXPOSE 8501

ENTRYPOINT ["poetry", "run", "streamlit", "run", "./0_🏠_Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
