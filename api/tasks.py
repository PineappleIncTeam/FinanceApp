import os

import requests
from celery import shared_task
from django.core.cache import cache
from dotenv import load_dotenv

from api.models import CurrencyData

load_dotenv()


@shared_task
def fetch_currency_data():
    url = "https://api.apilayer.com/currency_data/live"
    api_key = os.getenv("CURRENCY_API_KEY")
    params_list = [
        {"source": "USD", "currencies": "RUB"},
        {"source": "EUR", "currencies": "RUB"},
        {"source": "BTC", "currencies": "RUB"},
    ]
    headers = {"apikey": api_key}
    data_all = []

    for params in params_list:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()["quotes"]
            data_all.append(data)
            print(data_all)
            for currency, value in data.items():
                CurrencyData.objects.update_or_create(currency=currency, defaults={"rate": value})
        else:
            print(f"Ошибка {response.status_code}: {response.text}")


@shared_task
def update_redis():
    data = list(CurrencyData.objects.all().values("currency", "rate"))
    cache.set("currency_data", data, timeout=4200)
