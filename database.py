#!/usr/bin/env python

import pymongo
from full_text import hindustan_ndls_data, hindu_ndls_data, toi_ndls_data 
connection = pymongo.Connection()
database = connection.news
collection = database.create

def collection(name):
	try:
		collection = database.create_collection(name)
		return collection
	except pymongo.errors.CollectionInvalid:
		return eval("database.%s"%(name))




if __name__ == "__main__":





