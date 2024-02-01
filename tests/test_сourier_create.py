import allure
import pytest
import requests

import handlers
import urls
from generates.generate_random_string import generate_random_string


class TestCreateCourier:
    data = {}

    @classmethod
    def setup_class(cls):
        cls.data["login"] = generate_random_string(10)
        cls.data["password"] = generate_random_string(10)
        cls.data["firstName"] = generate_random_string(10)

    @allure.title('Проверка создания курьера, возвращения правильного код ответа и возвращения тела ответа')
    def test_create_new_courier(self):
        response_body = {
            "ok": True
        }
        response = requests.post(
            f'{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}',
            data=TestCreateCourier.data)
        assert response.status_code == 201
        assert response.json() == response_body

    @allure.title('Проверка регистрации двух одинаковых курьеров и возвращения правильного код ответа')
    def test_create_same_couriers(self):
        response = requests.post(
            f"{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}",
            data=TestCreateCourier.data)
        response = requests.post(
            f"{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}",
            data=TestCreateCourier.data)
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
            ('akao1om', '', ''),  # не проходит кейс (поле не является обязательным??)
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

    @classmethod
    def teardown_class(cls):
        cls.data.clear()
