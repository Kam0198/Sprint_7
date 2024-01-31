import allure
import pytest
import requests

import handlers
import urls
from generates.generate_registration import register_new_courier_and_return_login_password as generate_data


class TestCreateCourier:
    data = {}

    @classmethod
    def setup_class(cls):
        courier = generate_data()
        cls.data["login"] = courier[0]
        cls.data["password"] = courier[1]
        cls.data["firstName"] = courier[2]

    @allure.title('Проверка создания курьера, возвращения правильного код ответа и возвращения {"ok":true}')
    def test_create_new_courier(self):
        response_body = {
            "ok": True
        }
        response = requests.post(
            f'{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}',
            data=TestCreateCourier.data)
        assert response.status_code == 201
        assert response.json() == response_body

    @allure.title('Проверка регистрации двух одинаковых курьеров и возвращения правильного код ответа') # не нравится, что тесты не атомарные и зависят друг от друга
    def test_create_same_couriers(self):
        response = requests.post(
            f"{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}",
            data=TestCreateCourier.data)
        assert response.status_code == 409
        assert response.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
             }
        print(response.json())

    @pytest.mark.parametrize(
        'login, password, firstName',
        [
            ('', '', ''),
            ('', '15363', 'KAM'),
            ('kam', '', 'Kam'),
            ('akam', '', ''),  # не проходит кейс (поле не является обязательным??)
        ]
    )
    @allure.title('Проверка регистрации курьера без заполнения обязательных полей '
                  'и возвращения правильного код ответа')
    def test_create_courier_with_invalid_date(self, login, password, firstName):
        invalid_data = {'login': login, 'password': password, 'firstName': firstName}

        response = requests.post(f"{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}",
                                 data=invalid_data)
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для создания учетной записи"
        }
        print(response.json())

    @classmethod
    def teardown_class(cls):
        cls.data.clear()
