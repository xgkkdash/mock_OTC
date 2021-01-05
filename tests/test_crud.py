import pytest
import uuid
from database.mongodb import MongoDatabase
from models.order import Order
from models.trade import Trade


# this test requires mongo is already start at local pc
@pytest.fixture()
def db():
    db_name = "test_mock_otc"
    url = "mongodb://localhost:27017/"
    database = MongoDatabase(db_name, url)
    yield database
    database.drop_database()


def gen_id():
    return uuid.uuid4().hex


@pytest.fixture()
def order():
    return Order("BTC/USD", "buy", 3000, 0.1, gen_id())


@pytest.fixture()
def trade():
    return Trade("BTC/USD", "buy", 3000, 0.1, gen_id(), gen_id())


def test_get_invalid_order(db, order):
    # empty db, gen a invalid order_id and get
    assert not db.get_order(order.order_id)
    assert not db.get_order("invalid_id")


def test_save_order(db, order):
    # gen an order and save it to db
    assert db.save_order(order)
    # get saved order with order_id
    get_o = db.get_order(order.order_id)
    assert get_o
    assert get_o.order_id == order.order_id


def test_delete_order(db, order):
    # gen an order and save it to db
    assert db.save_order(order)
    # get saved order with order_id
    assert db.get_order(order.order_id)
    # delete order by passing order_id or order_object
    assert db.delete_order(order.order_id)
    # get by order_id after delete, should get None
    assert not db.get_order(order.order_id)


def test_get_invalid_trade(db, trade):
    # empty db, gen a invalid trade_id and get
    assert not db.get_trade(trade.trade_id)
    assert not db.get_order("invalid_id")


def test_save_trade(db, trade):
    # gen a trade and save it to db
    assert db.save_trade(trade)
    # get saved trade with trade_id
    get_trade = db.get_trade(trade.trade_id)
    assert get_trade
    assert get_trade.trade_id == trade.trade_id


def test_delete_trade(db, trade):
    # gen a trade and save it to db
    assert db.save_trade(trade)
    # get saved trade with trade_id
    assert db.get_trade(trade.trade_id)
    # delete trade by passing trade_id or trade_object
    assert db.delete_trade(trade.trade_id)
    # get by trade_id after delete, should get None
    assert not db.get_trade(trade.trade_id)
