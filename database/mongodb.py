import mongoengine
from mongoengine import DoesNotExist
from database.OrderDocument import OrderDocument
from database.TradeDocument import TradeDocument
from models.order import Order
from models.trade import Trade


class MongoDatabase:
    def __init__(self, db_name, db_url):
        self.db_connection = mongoengine.connect(db=db_name, host=db_url)
        self.db_name = db_name

    def get_order(self, order_id):
        try:
            doc = OrderDocument.objects.get(order_id=order_id)
            return doc.to_order()
        except DoesNotExist:
            return None

    def save_order(self, order: Order):
        doc = OrderDocument.from_order(order)
        return doc.save()

    def delete_order(self, order_id):
        doc = None
        try:
            doc = OrderDocument.objects.get(order_id=order_id)
        except DoesNotExist:
            pass
        if doc:
            doc.delete()
            # return True after delete success
            return True
        else:  # target order not Found, return False
            return False

    def get_trade(self, trade_id):
        try:
            doc = TradeDocument.objects.get(trade_id=trade_id)
            return doc.to_trade()
        except DoesNotExist:
            return None

    def save_trade(self, trade: Trade):
        doc = TradeDocument.from_trade(trade)
        return doc.save()

    def delete_trade(self, trade_id):
        doc = None
        try:
            doc = TradeDocument.objects.get(trade_id=trade_id)
        except DoesNotExist:
            pass
        if doc:
            doc.delete()
            # return True after delete success
            return True
        else:  # target trade not Found, return False
            return False

    # Warning: this method should be used carefully and only in the test environment
    def drop_database(self):
        self.db_connection.drop_database(self.db_name)
