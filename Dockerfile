FROM python:3.11-slim

WORKDIR /code

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY readme.md ./
RUN uv sync --frozen --no-dev || uv sync --no-dev

COPY ./app /code/app
COPY ./ml /code/ml
COPY ./mlruns /code/mlruns

ENV PATH="/code/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
