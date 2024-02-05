import allure
import requests

from generates.generate_order import create_new_order_and_return_data
import urls
import handlers


class TestReturnOrder:
    data = []

    @classmethod
    def setup_class(cls):
        order = create_new_order_and_return_data()
        cls.data.append(order)

    @allure.title('Проверка возвращения списка заказов в теле ответа')
    def test_list_orders(self):
        response = requests.get(handlers.make_order_url)
        assert len(response.json()) > 0

    @classmethod
    def teardown_class(cls):
        cls.data.clear()