import allure
import pytest
import requests

import handlers
import urls
from generates.generate_registration import register_new_courier_and_return_login_password as generate_data


class TestAuth:
    data = {}

    @classmethod
    def setup_class(cls):
        courier_log_pass = generate_data()
        cls.data["login"] = courier_log_pass[0]
        cls.data["password"] = courier_log_pass[1]

    @staticmethod
    def courier_registration():
        requests.post(
            f"{urls.MAIN_URL}{handlers.CREATE_COURIER_HANDLER}",
            data=TestAuth.data)

    @allure.title('Проверка авторизации курьера, возвращения правильного код ответа'
                  'и возвращение id пользователя')
    def test_courier_auth(self):
        response = requests.post(f"{urls.MAIN_URL}{handlers.LOGIN_COURIER_HANDLER}",
                                 data=TestAuth.data)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize(
        'login, password',
        [
            ('', generate_data()),
            (generate_data(), '',),
            ('', '')
        ]
    )
    @allure.title('Проверка авторизации без заполнения обязательных полей'
                  'и возвращения правильного код ответа')
    def test_courier_auth_with_invalid_data(self, login, password):
        TestAuth.courier_registration()
        invalid_data = {'login': login, 'password': password}

        response = requests.post(f"{urls.MAIN_URL}{handlers.LOGIN_COURIER_HANDLER}",
                                 data=invalid_data)
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для входа"
        }

    @pytest.mark.parametrize(
        'login, password',
        [
            ('yytr', generate_data()),
            (generate_data(), '123456'),
            (generate_data(), generate_data())
        ]
    )
    @allure.title('Проверка появления ошибки при заполнении невалидного логина/пароля '
                  'и возвращения правильного код ответа')
    def test_return_error_message_with_invalid_data(self, login, password):
        TestAuth.courier_registration()
        invalid_data = {'login': login, 'password': password}

        response = requests.post(f"{urls.MAIN_URL}{handlers.LOGIN_COURIER_HANDLER}",
                                 data=invalid_data)
        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }

    @classmethod
    def teardown_class(cls):
        cls.data.clear()


