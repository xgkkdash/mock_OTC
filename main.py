import os
import random
import uuid
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from database.mongodb import MongoDatabase
from models.order import Order
from models.trade import Trade
from models.quote import Quote

app = FastAPI()


class Rfq(BaseModel):
    symbol: str
    quantity: float
    side: str


class SendOrder(BaseModel):
    symbol: str
    side: str
    price: float
    quantity: float
    order_id: Optional[str] = None
    should_fill: Optional[bool] = None


# Dependency
def get_db():
    db_name = "test_mock_otc"
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    db_url = "mongodb://" + DB_HOST + ":27017/"
    db = MongoDatabase(db_name, db_url)
    yield db


def gen_id():
    return uuid.uuid4().hex


def gen_price():
    return random.uniform(3000, 5000)


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/orders/{order_id}")
def get_order(order_id: str, db=Depends(get_db)):
    order = None
    try:
        order = db.get_order(order_id)
    except Exception as e:
        print(e)
    if order:
        return order.__dict__
    else:
        raise HTTPException(status_code=400, detail="order not found")


@app.get("/trades/{trade_id}")
def get_trade(trade_id: str, db=Depends(get_db)):
    trade = None
    try:
        trade = db.get_trade(trade_id)
    except Exception as e:
        print(e)
    if trade:
        return trade.__dict__
    else:
        raise HTTPException(status_code=400, detail="trade not found")


@app.post("/quotes/")
def request_quote(rfq: Rfq):
    quote = Quote(rfq.symbol, rfq.side, gen_price(), rfq.quantity, gen_id())
    return quote.__dict__


@app.post("/orders/")
def send_order(send_o: SendOrder, db=Depends(get_db)):
    order_id = send_o.order_id or gen_id()  # if client has an order_id, use it, else, gen an order_id
    order_filled = send_o.should_fill or random.randint(0, 1)
    order_status = 'filled' if order_filled else 'rejected'
    filled_qty = send_o.quantity if order_filled else 0
    trade_id = gen_id() if order_filled else None

    result_order = Order(send_o.symbol, send_o.side, send_o.price, send_o.quantity,
                         order_id, order_status, filled_qty, trade_id)
    db.save_order(result_order)
    if order_filled:
        trade = Trade(result_order.symbol, result_order.side, result_order.price, result_order.quantity,
                      result_order.trade_id, result_order.order_id)
        db.save_trade(trade)
    return result_order.__dict__
