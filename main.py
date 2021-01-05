from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    pass


@app.get("/trades/{trade_id}")
def get_trade(trade_id: str):
    pass


@app.post("/quotes/")
def request_quote():
    pass


@app.post("/orders/")
def send_order():
    pass
