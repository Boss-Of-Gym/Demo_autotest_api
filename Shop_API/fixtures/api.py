import pytest
import random
import time
from mimesis import Text, Person
from datetime import datetime

set_order_status_list = [
    "canceled",
    "ready_to_transit",
    "in_transit",
    "done"
]

feedback_status = [
    "positive",
    "negative"
]

payment_satus = [
    "paid",
    "not_paid",
    "waiting"
]

payment_method = [
    "cash",
    "online",
    "card_upon_receipt"
]

list_id = [
    18108017,
    18108016,
    18108015,
    18108014
]

list_id_special_offers = [
    152717,
    152715,
    152712,
    152605,
    152604,
    152603,
    152602,
    152601,
    152600,
    152599,
    152598,
    152597,
    152596,
    152595,
    152721
]

list_id_vacancies = [
    "564",
    "526",
    "562",
    "556"
]

list_gender = [
    "man",
    "woman"
]

def random_date(start_year=1900, end_year=2025):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    if month == 2:
        max_day = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
    elif month in [4, 6, 9, 11]:
        max_day = 30
    else:
        max_day = 31
    day = random.randint(1, max_day)

    return datetime(year, month, day)

@pytest.fixture
def random_values_for_other_task():
    return {
        "set_payment_status": random.choice(seq=payment_satus),
        "set_payment_method": random.choice(seq=payment_method),
        "set_feedback_status": random.choice(seq=feedback_status),
        "set_order_status": random.choice(seq=set_order_status_list),
        "random_number_for_test_thousend": random.randint(1, 9999),
        "random_number_for_test_ten": random.randint(1, 10),
        "random_number_for_test_secound_field": random.randint(1, 20),
        "text_for_key_test": Text().title(),
        "random_id_items": random.choice(seq=list_id),
        "random_special_offers": random.sample(population=list_id_special_offers, k=3),
        "random_vacancies": random.choice(seq=list_id_vacancies),
        "name_test_key": Person().name(),
        "random_birthday": random_date().strftime("%Y-%m-%d"),
        "random_gender": random.choice(seq=list_gender),
        "random_phone_number": Person().phone_number("9#########")
    }

@pytest.fixture
def random_location():
    # Широта: от -90 до 90
    latitude = str(round(random.uniform(-90.0, 90.0), 6))
    
    # Долгота: от -180 до 180
    longitude = str(round(random.uniform(-180.0, 180.0), 6))

    # timestamp в секундах (Unix time)
    timestamp = int(time.time())

    return {
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp
    }

@pytest.fixture
def random_location_and_order_status(random_location, set_order_status):
    combined = random_location.copy()
    combined.update(set_order_status)
    return combined





