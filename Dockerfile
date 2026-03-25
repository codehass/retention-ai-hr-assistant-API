FROM python:3.11-slim

WORKDIR /code

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY readme.md ./
RUN uv sync --frozen --no-dev || uv sync --no-dev

COPY ./app /code/app
COPY ./ml /code/ml
COPY ./mlruns /code/mlruns

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
