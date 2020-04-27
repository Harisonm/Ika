# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os 

MONGO_URI = os.environ.get("MONGO_URI", default=False)

myclient = MongoClient(MONGO_URI)
mdb = myclient["ika"]
