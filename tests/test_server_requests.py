from fastapi.testclient import TestClient

from main import app
from tests.conftest import *


@pytest.fixture
def client():
    client = TestClient(app)
    yield client


def test_request_buy_quote(client):
    params = {"symbol": "BTC/USD", "quantity": 0.1, "side": "buy"}
    response = client.post('/quotes/', json=params)
    assert response.status_code == 200
    assert response.json().get('buy_px')


def test_request_two_way_quote(client):
    params = {"symbol": "BTC/USD", "quantity": 0.1}
    response = client.post('/quotes/', json=params)
    assert response.status_code == 200
    assert response.json().get('buy_px')
    assert response.json().get('sell_px')


def test_send_order(client, order):
    params = order.__dict__
    response = client.post('/orders/', json=params)
    assert response.status_code == 200
    assert response.json().get('status') in {'filled', 'rejected'}


def test_get_order(client, order):
    params = order.__dict__
    send_response = client.post('/orders/', json=params)
    assert send_response.status_code == 200
    assert send_response.json().get('status') in {'filled', 'rejected'}

    order_id = order.order_id or send_response.json().get('order_id')
    get_response = client.get('/orders/' + order_id)
    assert get_response.status_code == 200
    assert get_response.json().get('status') == send_response.json().get('status')
    assert get_response.json().get('order_id') == send_response.json().get('order_id')


def test_get_trade(client, order):
    # send an order and receive filled back
    params = order.__dict__
    params['should_fill'] = True
    send_o_response = client.post('/orders/', json=params)
    assert send_o_response.status_code == 200
    assert send_o_response.json().get('status') == 'filled'
    assert send_o_response.json().get('trade_id')
    order_id = order.order_id or send_o_response.json().get('order_id')

    # get trade by request with trade_id
    trade_id = send_o_response.json().get('trade_id')
    get_trade_response = client.get('/trades/' + trade_id)
    assert get_trade_response.status_code == 200
    assert get_trade_response.json().get('trade_id') == trade_id
    assert get_trade_response.json().get('order_id') == order_id
