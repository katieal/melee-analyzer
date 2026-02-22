from pymongo import MongoClient
import pandas as pd

# Import CRUD Module
from db_crud import MeleeAnalyzer

# Connect to database
username = "admin"
password = "AmyFest1"
db = MeleeAnalyzer(username, password)

# import data into dataframe
df = pd.DataFrame.from_records(db.read({}))
df.drop(columns=['_id'],inplace=True)