import os
import sys
import certifi
from pymongo import MongoClient

with open('out2.txt', 'w') as f:
    f.write("Starting...\n")
    try:
        mongo_uri = "mongodb+srv://janish1771_db_user:janish1771_db_user@cluster0.v72gzzr.mongodb.net/?appName=Cluster0"
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
        client.server_info()
        f.write("Success!\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
