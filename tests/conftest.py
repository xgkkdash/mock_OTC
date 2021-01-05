import pytest
import uuid
from models.order import Order
from models.trade import Trade


def gen_id():
    return uuid.uuid4().hex


@pytest.fixture()
def order():
    return Order("BTC/USD", "buy", 3000, 0.1, gen_id())


@pytest.fixture()
def trade():
    return Trade("BTC/USD", "buy", 3000, 0.1, gen_id(), gen_id())
