#!/usr/bin/env python

"""
This is the file responsible for actually inserting data in the database.
"""

from full_text import hindustan_ndls_data, hindu_ndls_data, toi_ndls_data
from database import DB, collection
from custom_logging import exceptions_logger

class InsertDB(object):


	@staticmethod
	def __insert_db(self, data):
		mongo_collection = collection("News")
		mongo_collection.insert(post, upsert=true)
		return 

	@staticmethod
	def ht():
		try:
			__data = hindustan_ndls_data()
			InsertDB.__insert_db(__data)
		except Exception as error:
			exceptions_logger(error)
			pass


	@staticmethod
	def hin():
		try:
			__data = hin_ndls_data()
			InsertDB.__insert_db(__data)

		except Exception as error:
			exceptions_logger(error)
			pass


	@staticmethod
	def toi():
		try:
			__data = toi_ndls_data()
			InsertDB.__insert_db(__data)
		except Exception as error:
			exceptions_logger(error)
			pass







