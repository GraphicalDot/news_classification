#!/usr/bin/env python

import feedparser
from database import collection, DB
from  datetime import datetime
import time
import sys
HINDUSTAN_TIMES_NDLS = "http://www.hindustantimes.com/HT-feed/FeedXml.aspx?c=NewDelhi"
TOI_NDLS = "http://timesofindia.feedsportal.com/c/33039/f/533976/index.rss"
HINDU_NDLS = "http://www.thehindu.com/news/cities/Delhi/?service=rss"
HINDUSTAN_INDIA = "http://feeds.hindustantimes.com/HT-India"
TOI_INDIA = "http://timesofindia.feedsportal.com/c/33039/f/533916/index.rss"
HINDU_INDIA = "http://www.thehindu.com/news/national/?service=rss"
class Rss(object):
	def __init__(self, src_name, rss_link):
		self.src_name = src_name
		self.rss_link = rss_link
		self.mongo_collection = collection("Epoch")#This uses the collection method imported above which returns 
							#collection obejct in case it exists or create if it doesnt

	def __updating_epoch_collection(self, epoch):
		"""
		This function updates the enteries in the epoch collection.If the enteries is not present it will be created(
		as the upsert flag is set to be True.
	
		"""
		self.mongo_collection.update({"name": self.src_name},{"$set": {"epoch": epoch}}, upsert = True)
		return


	def __get_last_epoch(self):
		"""
		This function gets the last epoch time stored in the pymongo collection corresponding to the self.src_name

		"""
		try:
			return self.mongo_collection.find_one({"name": self.src_name}).get("epoch")
	
		except AttributeError:
			return None

	def __converting_to_epoch(self, time_struct_object):
		"""
		This function converts the time.struct_time time format into the epoch time
	
		"""
	
		date = datetime.fromtimestamp(time.mktime(time_struct_object))
		return time.mktime(date.timetuple())



	def __main_logic(self):
		#Getting rss feed from the self.rss_link
		rss_data = feedparser.parse(self.rss_link)
		
		#Filtering data by list comprehension
		data =  [dict(link= rss.get("link"), published=rss.get("published"), summary=rss.get("summary"), headline=rss.get("title"), published_date= self.__converting_to_epoch(rss.get("published_parsed")), ) for rss in rss_data.get("entries")]
		
		#Sorting the above list on the basis of epoch time 
		data_sort = sorted(data, key=lambda x: x["published_date"], reverse=True)
		
		#breaking list on the basis of the news stored in the pymongo collection already
		updated = [item for item in data_sort if item.get("published_date") > self.__get_last_epoch()]
		print updated
		#if the list is not empty, updating the pymongo collection with new epoch time
		if updated:
			self.__updating_epoch_collection(updated[0].get("published_date"))
		
		
		return updated

	@staticmethod
	def ht_ndls_rss():
		instance = Rss("HT_NDLS", HINDUSTAN_TIMES_NDLS)
		return instance.__main_logic()
	
	@staticmethod
	def hin_ndls_rss():
		instance = Rss("HIN_NDLS", HINDU_NDLS)
		return instance.__main_logic()
	
	
	
	@staticmethod
	def toi_ndls_rss():
		instance = Rss("TOI_NDLS", TOI_NDLS)
		return instance.__main_logic()
	
	@staticmethod
	def ht_india_rss():
		instance = Rss("HT_INDIA", HINDUSTAN_INDIA)
		return instance.__main_logic()
	
	@staticmethod
	def hin_india_rss():
		instance = Rss("HINDU_INDIA", HINDU_INDIA)
		return instance.__main_logic()
	
	@staticmethod
	def toi_india_rss():
		instance = Rss("TOI_INDIA", TOI_INDIA)
		return instance.__main_logic()
	
	
