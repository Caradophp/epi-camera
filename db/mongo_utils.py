class MongoUtils:
    def __init__(self, connection):
        self.connection = connection

    def insert_event(self, data):
        self.connection.insert_one(data)
        
    def find_events(self, query):
        return self.connection.find(query)
    
    def delete_events(self, query):
        self.connection.delete_many(query)