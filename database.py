#!/usr/bin/env python
"""
This python file have the important database functions to be used while insertion of data.

"""
from pymongo import MongoClient


CONNECTION = MongoClient("localhost", 27017, w=1, j=True)
DB = CONNECTION.news
#wValue == 1 perform a write acknowledgement
#journal(j) true: Sync to journal.



def collection(name):
	"""
	This function returns the collection object from the mongodb on the basis of the collection name provided to it 
	in the arguments.
	If the collection is not being present, it will be created
	"""
	
	try:
		collection = DB.create_collection(name)
		return collection
	except pymongo.errors.CollectionInvalid:
		return eval("DB.%s"%(name))







