#!/usr/bin/env python

"""
This is the file responsible for actually inserting data in the database.
"""

from full_text import hindustan_ndls_data, hindu_ndls_data, toi_ndls_data, toi_india_data, ht_india_data, hin_india_data
from database import DB, collection
from custom_logging import exceptions_logger
import traceback
import sys
import logging
import inspect

LOG_FILENAME = 'exceptions_logger.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)


class DBInsert(object):


	@staticmethod
	def __db_insert(data):
		mongo_collection = collection("News")
		[mongo_collection.insert(post, upsert=True) for post in data]
		return


	@staticmethod
	def ht():
		try:
			__data = hindustan_ndls_data()
			DBInsert.__db_insert(__data)
			return __data
		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass


	@staticmethod
	def hin():
		try:
			__data = hindu_ndls_data()
			DBInsert.__db_insert(__data)

		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass


	@staticmethod
	def toi():
		try:
			__data = toi_ndls_data()
			DBInsert.__db_insert(__data)
		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass



	@staticmethod
	def toi_india():
		try:
			__data = toi_india_data()
			DBInsert.__db_insert(__data)
		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass


	
	@staticmethod
	def ht_india():
		try:
			__data = ht_india_data()
			DBInsert.__db_insert(__data)
		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass


	@staticmethod
	def hin_india():
		try:
			__data = hin_india_data()
			DBInsert.__db_insert(__data)
		except:
			logging.exception('Got exception in %s'%(inspect.stack()[0][3]))
			pass

