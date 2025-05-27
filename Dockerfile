FROM python:3.11

RUN apt-get update && apt-get install -y telnet tcpdump iputils-ping dnsutils
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/FinanceApp

COPY . /opt/FinanceApp


# RUN pip install -r /opt/FinanceApp/requirements.txt
# Установка Poetry
RUN pip install poetry

# Копируем только файлы зависимостей сначала (для кеширования)
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi


# Указываем Python, где искать модули
ENV PYTHONPATH=/app
CMD ["python3", "/manage.py", "runserver", "0.0.0.0:8000"]


