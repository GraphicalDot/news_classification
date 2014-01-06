#!/usr/bin/env python

from variables import DB
import pymongo


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







