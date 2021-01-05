from mongoengine import Document, FloatField, StringField

from models.trade import Trade


class TradeDocument(Document):
    symbol = StringField(required=True)
    side = StringField(required=True)
    price = FloatField(required=True)
    quantity = FloatField(required=True)
    trade_id = StringField(required=True, unique=True)
    order_id = StringField(required=True)
    meta = {
        'collection': 'trades',
        'indexes': ['symbol', 'trade_id'],
        'index_background': True,
    }

    @classmethod
    def from_trade(cls, trade: Trade):
        trade_doc = cls(**vars(trade))
        return trade_doc

    def to_trade(self) -> Trade:
        doc_dict = self.to_mongo().to_dict()
        doc_dict.pop('_id')
        return Trade(**doc_dict)
