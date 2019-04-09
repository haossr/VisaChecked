import pandas as pd
from pymongo import MongoClient

HOST = "ds135456.mlab.com"
PORT = 35456
USERNAME = "hao"
PASSWORD = "hao000"
DB = "visa"
COLLECTION = "visa"


def get_raw_data():
    db = _connect_mongo(HOST, PORT, USERNAME, PASSWORD, DB)
    return _mongo_to_df(db, COLLECTION)


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://{}:{}@{}:{}/{}'.format(username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def _mongo_to_df(db, collection, query=None):
    """ Read from Mongo and Store into DataFrame """
    return pd.DataFrame.from_records(db[collection].find(query))
