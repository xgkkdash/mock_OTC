import asyncio
import motor.motor_asyncio
import os
import random
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database.mongodb import find_order, find_trade, insert_order, insert_trade
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
    db_name = os.environ.get('DB_NAME', 'mock_otc_dev')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '27017')
    db_url = "mongodb://" + db_host + ":" + str(db_port) + "/"
    db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    return db_client[db_name]


db = get_db()


def gen_id():
    return uuid.uuid4().hex


def gen_price():
    return random.uniform(3000, 5000)


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = None
    try:
        order_doc = await find_order(db, order_id)
        if order_doc:
            order_doc.pop('_id')
            order = Order(**order_doc)
    except Exception as e:
        print(e)
    if order:
        return order.__dict__
    else:
        raise HTTPException(status_code=400, detail="order not found")


@app.get("/trades/{trade_id}")
async def get_trade(trade_id: str):
    trade = None
    try:
        trade_doc = await find_trade(db, trade_id)
        if trade_doc:
            trade_doc.pop('_id')
            trade = Trade(**trade_doc)
    except Exception as e:
        print(e)
    if trade:
        return trade.__dict__
    else:
        raise HTTPException(status_code=400, detail="trade not found")


@app.post("/quotes/")
async def request_quote(rfq: Rfq):
    quote = Quote(rfq.symbol, rfq.side, gen_price(), rfq.quantity, gen_id())
    return quote.__dict__


@app.post("/orders/")
async def send_order(send_o: SendOrder):
    order_id = send_o.order_id or gen_id()  # if client has an order_id, use it, else, gen an order_id
    order_filled = send_o.should_fill or random.randint(0, 1)
    order_status = 'filled' if order_filled else 'rejected'
    filled_qty = send_o.quantity if order_filled else 0
    trade_id = gen_id() if order_filled else None

    result_order = Order(send_o.symbol, send_o.side, send_o.price, send_o.quantity,
                         order_id, order_status, filled_qty, trade_id)
    tasks = [insert_order(db, result_order)]
    if order_filled:
        trade = Trade(result_order.symbol, result_order.side, result_order.price, result_order.quantity,
                      result_order.trade_id, result_order.order_id)
        tasks.append(insert_trade(db, trade))
    await asyncio.gather(*tasks)
    return result_order.__dict__
