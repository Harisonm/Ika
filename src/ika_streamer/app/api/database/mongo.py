# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os 

#MONGO_URI="mongodb://localhost:27017/"  
# MONGO_URI=os.environ.get("MONGO_URI", default=False)

myclient = MongoClient('mongodb', 27017)
mdb = myclient["ika"]
