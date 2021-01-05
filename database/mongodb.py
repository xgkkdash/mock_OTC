import mongoengine
from models.order import Order
from models.trade import Trade


class MongoDatabase:
    def __init__(self, db_name, db_url):
        self.db_connection = mongoengine.connect(db=db_name, host=db_url)
        self.db_name = db_name

    def get_order(self, order_id):
        pass

    def save_order(self, order: Order):
        pass

    def delete_order(self, order_id):
        pass

    def get_trade(self, trade_id):
        pass

    def save_trade(self, trade: Trade):
        pass

    def delete_trade(self, trade_id):
        pass

    # Warning: this method should be used carefully and only in the test environment
    def drop_database(self):
        self.db_connection.drop_database(self.db_name)
