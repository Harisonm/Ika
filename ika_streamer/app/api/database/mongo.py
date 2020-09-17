# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os 

#
MONGO_URI="mongodb://localhost:27017/"  
# MONGO_URI=os.environ.get("MONGO_URI", default=False)
# TODO : Pour docker a changer à la fin
# myclient = MongoClient('mongodb', 27017)
myclient = MongoClient(MONGO_URI)
mdb = myclient["ika"]
