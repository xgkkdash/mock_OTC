import mongoengine


class MongoDatabase:
    def __init__(self, db_name, db_url):
        self.db_connection = mongoengine.connect(db=db_name, host=db_url)
        self.db_name = db_name

    def get_order(self):
        pass

    def save_order(self):
        pass

    def delete_order(self):
        pass

    def get_trade(self):
        pass

    def save_trade(self):
        pass

    def delete_trade(self):
        pass

    # Warning: this method should be used carefully and only in the test environment
    def drop_database(self):
        self.db_connection.drop_database(self.db_name)
