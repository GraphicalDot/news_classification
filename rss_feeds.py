#!/usr/bin/env python

import feedparser
from variables import HINDUSTAN_TIMES_NDLS, TOI_NDLS, HINDU_NDLS, DB
from database import collection
from  datetime import datetime
import time


def updating_epoch_collection(src_name, epoch):
	"""
	This function updates the enteries in the epoch collection.If the enteries is not present it will be created(
	as the upsert flag is set to be True.

	"""
	collection = collection("Epoch")
	collection.update({"name": src_name},{"$set": {"epoch": epoch}}, upsert = True)
	sys.exit(1)


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

	"""
	rss_data = feedparser.parse(HINDUSTAN_TIMES_NDLS)
	return [dict(link= rss.get("link"), published=rss.get("published"), summary=rss.get("summary"), headline=rss.get("title"), published_date= converting_to_epoch(rss.get("published_parsed")), ) for rss in rss_data.get("entries")]

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

	"""
	rss_data = feedparser.parse(HINDU_NDLS)
	return [dict(link= rss.get("link"), published=rss.get("published"), summary=rss.get("summary"), headline=rss.get("title"), published_date= converting_to_epoch(rss.get("published_parsed")), ) for rss in rss_data.get("entries")]



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

	"""

	rss_data = feedparser.parse(HINDUSTAN_TIMES_NDLS)
	return [dict(link= rss.get("link"), published=rss.get("published"), summary=rss.get("summary"), headline=rss.get("title"), published_date= converting_to_epoch(rss.get("published_parsed")),  ) for rss in rss_data.get("entries")]




