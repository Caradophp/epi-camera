import pymongo

class Connection:
    @staticmethod
    def conectar():
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["mydatabase"]
        mycol = mydb["epis"]
        return mycol