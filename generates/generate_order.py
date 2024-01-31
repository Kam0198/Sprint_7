import requests
from faker import Faker
import random
import datetime
import handlers
import urls
from generates.generate_random_string import generate_random_string

fake = Faker(locale="ru_RU")


def create_new_order_and_return_data():
    # создаём список
    order_data = {}

    # генерируем данные о заказе
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.address()
    metro_station = random.randint(1, 10)
    phone = fake.phone_number()
    rent_time = random.randint(1, 5)
    delivery_date = datetime.datetime.now().isoformat()
    comment = generate_random_string(9)

    # собираем тело запроса
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "address": address,
        "metroStation": metro_station,
        "phone": phone,
        "rentTime": rent_time,
        "deliveryDate": delivery_date,
        "comment": comment
    }
    response = \
        requests.post(f'{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список данные о заказе
    if response.status_code == 201:
        order_data.append(first_name)
        order_data.append(last_name)
        order_data.append(address)
        order_data.append(metro_station)
        order_data.append(phone)
        order_data.append(rent_time)
        order_data.append(delivery_date)
        order_data.append(comment)

    # возвращаем список
    return order_data



