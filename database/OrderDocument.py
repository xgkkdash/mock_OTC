from mongoengine import Document, FloatField, StringField

from models.order import Order


class OrderDocument(Document):
    symbol = StringField(required=True)
    side = StringField(required=True)
    price = FloatField(required=True)
    quantity = FloatField(required=True)
    order_id = StringField(required=True, unique=True)
    status = StringField()
    filled_qty = FloatField(default=0)
    trade_id = StringField()
    meta = {
        'collection': 'orders',
        'indexes': ['symbol', 'order_id'],
        'index_background': True,
    }

    @classmethod
    def from_order(cls, order: Order):
        order_doc = cls(**vars(order))
        return order_doc

    def to_order(self) -> Order:
        doc_dict = self.to_mongo().to_dict()
        doc_dict.pop('_id')
        return Order(**doc_dict)
