FROM python:3.8 as builder

ENV POETRY_VERSION=1.4.2
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

FROM python:3.8-slim

WORKDIR /app

COPY --from=builder /app ./

CMD ["python", "/manage.py", "runserver", "0.0.0.0:8000"]
