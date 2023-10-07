from datetime import datetime, timedelta

import requests
from celery import shared_task

from rates.models import Currency, Rate


def add_existings_currency(currency_data):
    currency_list = list(currency_data.keys())
    existing_currencies = (Currency.objects.filter(char_code__in=currency_list)
                           .values_list('char_code', flat=True))

    new_currencies = [currency for currency in currency_list if currency not in existing_currencies]

    new_currency_objects = [Currency(
        char_code=currency,
        name=currency_data[currency].get("Name")
    ) for currency in new_currencies
    ]
    Currency.objects.bulk_create(new_currency_objects)


def add_rates(date, currency_data):
    unique_char_codes = set(currency.get("CharCode") for currency in currency_data.values())

    currency_mapping = {currency.char_code: currency for currency in
                        Currency.objects.filter(char_code__in=unique_char_codes)}

    data = [
        Rate(date=date,
             currency=currency_mapping[currency.get("CharCode")],
             value=currency.get("Value"))
        for currency in currency_data.values()
    ]
    Rate.objects.bulk_create(data)


def get_currency_data(url, date):
    response = requests.get(url)
    if response.status_code == 200:
        quotation_data = response.json()
        return quotation_data.get("Valute")
    else:
        print(f"Ошибка при загрузке данных для {date}: {response.status_code}")


@shared_task
def update_rates():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=14)

    base_url = "https://www.cbr-xml-daily.ru/archive/"

    if not Rate.objects.filter(date=start_date).exists():
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y/%m/%d")
            url = f"{base_url}{date_str}/daily_json.js"
            try:
                currency_data = get_currency_data(url, current_date)
                add_existings_currency(currency_data)
                add_rates(current_date, currency_data)
                current_date += timedelta(days=1)
            except:
                print(f"Ошибка при загрузке данных на {current_date}")



    else:
        current_date = datetime.now().date()
        if not Rate.objects.filter(date=current_date).exists():
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            try:
                currency_data = get_currency_data(url, current_date)
                add_existings_currency(currency_data)
                add_rates(current_date, currency_data)
            except:
                print(f"Ошибка при загрузке данных на {current_date}")


if __name__ == '__main__':
    update_rates()
