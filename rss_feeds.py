#!/usr/bin/env python

import feedparser
from variables import HINDUSTAN_TIMES_NDLS, TOI_NDLS, HINDU_NDLS, DB
from database import collection
from  datetime import datetime
import time
import sys


def updating_epoch_collection(src_name, epoch):
	"""
	This function updates the enteries in the epoch collection.If the enteries is not present it will be created(
	as the upsert flag is set to be True.

	"""
	mongo_collection = collection("Epoch")
	mongo_collection.update({"name": src_name},{"$set": {"epoch": epoch}}, upsert = True)
	sys.exit(1)


def get_last_epoch(src_name):
	mongo_collection = collection("Epoch")
	try:
		return mongo_collection.find_one({"name": src_name}).get("epoch")

	except AttributeError:
		return None

def converting_to_epoch(time_struct_object):
	"""
	This function converts the time.struct_time time format into the epoch time

	"""

	date = datetime.fromtimestamp(time.mktime(time_struct_object))
	return time.mktime(date.timetuple())


def hindustan_ndls_rss():
	"""
	This function parses the hindustan times rss feed for delhi from the web address supplied to it from the 
	HINDUSTAN_TIMES_NDLS
	it parses following parametres of the particular new link present in the rss feed
	1.link
	2.published date (human readable format)
	3.summary 
	4.title of the news
	5.published date converted into epoch time(which will be later used to identify the news already present in our 
		database.

	variables:
		data_sort = This is the variable which will have the sorted data list on the basis of the epoch times 
		which ae stored under the name published_date
	"""
	rss_data = feedparser.parse(HINDUSTAN_TIMES_NDLS)
	data =  [dict(link= rss.get("link"), published=rss.get("published"), summary=rss.get("summary"), headline=rss.get("title"), published_date= converting_to_epoch(rss.get("published_parsed")), ) for rss in rss_data.get("entries")]
	data_sort = sorted(data, key=lambda x: x["published_date"], reverse=True)
	updating_epoch_collection("HT_NDLS", data_sort[0].get("published_date"))
	return data_sort



def hindu_ndls_rss():
	"""
	This function parses the hindu rss feed for delhi from the web address supplied to it from the 
	HINDU_NDLS
	it parses following parametres of the particular new link present in the rss feed
	1.link
	2.published date (human readable format)
	3.summary 
	4.title of the news
	5.published date converted into epoch time(which will be later used to identify the news already present in our 
		database.
	variables:
		data_sort = This is the variable which will have the sorted data list on the basis of the epoch times 
		which ae stored under the name published_date

	"""
	rss_data = feedparser.parse(HINDU_NDLS)
	data = [dict(link= rss.get("link"), published=rss.get("published"), summary=rss.get("summary"), headline=rss.get("title"), published_date= converting_to_epoch(rss.get("published_parsed")), ) for rss in rss_data.get("entries")]
	data_sort = sorted(data, key=lambda x: x["published_date"], reverse=True)
	updating_epoch_collection("HIN_NDLS", data_sort[0].get("published_date"))
	return data_sort



def toi_ndls_rss():
	"""
	This function parses the times of india rss feed for delhi from the web address supplied to it from the TOI_NDLS
	it parses following parametres of the particular new link present in the rss feed
	1.link
	2.published date (human readable format)
	3.summary 
	4.title of the news
	5.published date converted into epoch time(which will be later used to identify the news already present in our 
		database.

	variables:
		data_sort = This is the variable which will have the sorted data list on the basis of the epoch times 
		which ae stored under the name published_date
	"""

	rss_data = feedparser.parse(HINDUSTAN_TIMES_NDLS)
	data =  [dict(link= rss.get("link"), published=rss.get("published"), summary=rss.get("summary"), headline=rss.get("title"), published_date= converting_to_epoch(rss.get("published_parsed")),  ) for rss in rss_data.get("entries")]
	data_sort = sorted(data, key=lambda x: x["published_date"], reverse=True)
	updated = [item for item in data_sort if item.get("published_date") > get_last_epoch("TOI_NDLS")]
	print updated
	if updated:
		updating_epoch_collection("TOI_NDLS", updated[0].get("published_date"))
	return updated


if __name__ == "__main__":
	toi_ndls_rss()

