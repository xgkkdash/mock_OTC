from dataclasses import dataclass


@dataclass
class Trade:
    symbol: str
    side: str
    price: float
    quantity: float
    trade_id: str
    order_id: str
