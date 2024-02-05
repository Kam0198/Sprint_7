from urls import MAIN_URL

CREATE_COURIER_HANDLER = '/api/v1/courier'
LOGIN_COURIER_HANDLER = '/api/v1/courier/login'
MAKE_ORDER_HANDLER = '/api/v1/orders'

login_url = f"{MAIN_URL}{LOGIN_COURIER_HANDLER}"
make_order_url = f"{MAIN_URL}{MAKE_ORDER_HANDLER}"
create_courier_url = f"{MAIN_URL}{CREATE_COURIER_HANDLER}"