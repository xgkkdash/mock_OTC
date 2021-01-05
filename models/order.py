from dataclasses import dataclass


@dataclass
class Order:
    symbol: str
    side: str
    price: float
    quantity: float
    order_id: str

    status: str = None
    filled_qty: float = 0
    trade_id: str = None
