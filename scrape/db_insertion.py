#!/usr/bin/env python

"""
This is the file responsible for actually inserting data in the database.
"""

from full_text import hindustan_ndls_data, hindu_ndls_data, toi_ndls_data
from database import DB, collection
from custom_logging import exceptions_logger
import traceback
import sys
import logging
import inspect

LOG_FILENAME = 'exceptions_logger.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)


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
		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass

	@staticmethod
	def hin():
		try:
			__data = hin_ndls_data()
			InsertDB.__insert_db(__data)

		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass


	@staticmethod
	def toi():
		try:
			__data = toi_ndls_data()
			InsertDB.__insert_db(__data)
		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass







