# Author: Katie LaCerda
# Program to display and analyze results from Smash Melee tournaments
from pymongo import MongoClient
from bson.objectid import ObjectId
from collections.abc import MutableMapping

class MeleeAnalyzer(object):
    def __init__(self, username, password):
        # Connection variables
        USER = username
        PASS = password
        DB = "mele"
        COL = 'results'

        # Initialize Connection
        uri = ('mongodb+srv://%s:%s@prod-aws-mele.5ez5u0x.mongodb.net/?appName=prod-aws-mele' % (USER, PASS))
        self.client = MongoClient(uri)
        self.database = self.client.get_database(DB)
        self.collection = self.database.get_collection(COL)

    # Method for the C in CRUD (Create)
    def create(self, data):
        if data is not None:
            self.database.results.insert_one(data)
            return True
        else:
            raise Exception("Insert failed: no data provided")
            return False

    # Method for the R in CRUD (Read)
    def read(self, query):
        if query is not None:
            return list(self.database.results.find(query))
        else:
            raise Exception("Search failed: no parameter specified")
            return []  # return empty list if search fails

    # Method for the U in CRUD (Update)
    def update(self, query, data):
        if query is not None and data is not None:
            return self.database.results.update_many(query, {"$set": data}).modified_count
        else:
            raise Exception("Update failed: no parameter and/or data provided")
            return 0  # return 0 if update fails

    # Method for the D in CRUD (Delete)
    def delete(self, query):
        if query is not None:
            return self.database.results.delete_many(query).deleted_count
        else:
            raise Exception("Delete failed: no parameter specified")
            return 0  # return 0 if delete fails

