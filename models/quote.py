from dataclasses import dataclass


@dataclass
class Quote:
    symbol: str
    side: str
    price: float
    quantity: float
    quote_id: str
