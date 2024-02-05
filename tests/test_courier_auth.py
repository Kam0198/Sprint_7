import allure
import pytest
import requests

import handlers
from generates.generate_registration import register_new_courier_and_return_login_password as generate_data


class TestAuth:

    @pytest.fixture(scope="function")
    def login_password_data(self):
        return generate_data()

    @allure.title('Проверка авторизации курьера, возвращения правильного код ответа'
                  ' и возвращение id пользователя')
    def test_courier_auth(self, login_password_data):
        response = requests.post(handlers.login_url,
                                 data={"login": login_password_data[0], "password": login_password_data[1]})
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
                  ' и возвращения правильного код ответа')
    def test_courier_auth_with_invalid_data(self, login, password):
        invalid_data = {'login': login, 'password': password}

        response = requests.post(handlers.login_url,
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
                  ' и возвращения правильного код ответа')
    def test_return_error_message_with_invalid_data(self, login, password):
        invalid_data = {'login': login, 'password': password}

        response = requests.post(handlers.login_url,
                                 data=invalid_data)
        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }


