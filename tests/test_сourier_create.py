import allure
import pytest
import requests

import handlers
from generates.generate_random_string import generate_random_string


class TestCreateCourier:

    @pytest.fixture
    def user_data(self):
        data = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        yield data

    @allure.title('Проверка создания курьера, возвращения правильного код ответа и возвращения тела ответа')
    def test_create_new_courier(self, user_data):
        response_body = {
            "ok": True
        }
        response = requests.post(handlers.create_courier_url,
                                 data=user_data)
        assert response.status_code == 201
        assert response.json() == response_body

    @allure.title('Проверка регистрации двух одинаковых курьеров и возвращения правильного код ответа')
    @pytest.mark.usefixtures("user_data")
    def test_create_same_couriers(self, user_data):
        for i in range(2):
            response = requests.post(handlers.create_courier_url,
                                     data=user_data)
            response = requests.post(handlers.create_courier_url,
                                     data=user_data)
        assert response.status_code == 409
        assert response.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
        }

    @pytest.mark.parametrize(
        'login, password, firstName',
        [
            ('', '', ''),
            ('', '15363', 'KAM'),
            ('kam', '', 'Kam'),
            ('akao1om', '', '')
        ]
    )
    @allure.title('Проверка регистрации курьера без заполнения обязательных полей '
                  'и возвращения правильного код ответа')
    def test_create_courier_with_invalid_date(self, login, password, firstName):
        invalid_data = {'login': login, 'password': password, 'firstName': firstName}

        response = requests.post(handlers.create_courier_url,
                                 data=invalid_data)
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для создания учетной записи"
        }
