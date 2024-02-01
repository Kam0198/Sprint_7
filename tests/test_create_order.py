import json

import allure
import pytest
import requests

import handlers
import urls
from generates.generate_order import create_new_order_and_return_data


class TestCreateOrder:

    @allure.title('Проверка создания заказа без указания цвета и содержание track в теле ответа')
    def test_order_without_scooter_color(self):
        response = requests.post(
            f'{urls.MAIN_URL}{handlers.MAKE_ORDER_HANDLER}',
            data=create_new_order_and_return_data())
        response_data = response.json()
        assert response.status_code == 201
        assert "track" in response_data.keys()

    @allure.title('Проверка выбора цвета самоката и содержание track в теле ответа')
    @pytest.mark.parametrize(
        'color',
        [
            ['BLACK'],
            ['GREY'],
            ['BLACK', 'GREY']
        ]
    )
    def test_choose_different_color(self, color):
        payload = create_new_order_and_return_data()
        payload["color"] = color
        response = requests.post(
                    f'{urls.MAIN_URL}{handlers.MAKE_ORDER_HANDLER}',
                    json=payload)
        response_data = response.json()
        assert "track" in response_data.keys()
