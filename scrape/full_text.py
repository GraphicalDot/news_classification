#!/usr/bin/env python

import os
import goose
import time
import logging
from rss_feeds import Rss as R
from custom_logging import exceptions_logger
_g_instance = goose.Goose()

def extracting_text(link):
	try:
		extract = _g_instance.extract(link)
		time.sleep(5)
		return extract.cleaned_text
	except Exception as e:
		exceptions_logger(e)

def hindustan_ndls_data():
	"""
	This functions gets the latest news from R.ht_ndls_rss() function and adds a two new fields to this list of 
	dictionaries
	1. full_text, Which will have the full text of the news link scraped by the Goose library.
	2. source, Which will have the name of the news source
	3. scraped_on, the time stamp on which it was scraped
	4. scraped_date, The human readable time foramt on which the data was scraped
	"""
	data = R.ht_ndls_rss()
	for news in data:
		news.update(dict(full_text = extracting_text(news.get("link")), source="HT_NDLS", scraped_epoch= time.time(), scraped_date=time.strftime("%d/%m/%Y")))
	return data


def hindu_ndls_data():
	"""
	This functions gets the latest news from R.hin_ndls_rss() function and adds a two new fields to this list of 
	dictionaries
	1. full_text, Which will have the full text of the news link scraped by the Goose library.
	2. source, Which will have the name of the news source
	3. scraped_on, the time stamp on which it was scraped
	4. scraped_date, The human readable time foramt on which the data was scraped
	"""
	data = R.hin_ndls_rss()
	for news in data[0:1]:
		news.update(dict(full_text = extracting_text(news.get("link")), source="HIN_NDLS", scraped_epoch= time.time(), scraped_date=time.strftime("%d/%m/%Y")))
	return data



def toi_ndls_data():
	"""
	This functions gets the latest news from R.toi_ndls_rss() function and adds a two new fields to this list of 
	dictionaries
	1. full_text, Which will have the full text of the news link scraped by the Goose library.
	2. source, Which will have the name of the news source
	3. scraped_on, the time stamp on which it was scraped
	4. scraped_date, The human readable time foramt on which the data was scraped
	"""
	data = R.toi_ndls_rss()
	for news in data:
		news.update(dict(full_text = extracting_text(news.get("link")), source="TOI_NDLS", scraped_epoch= time.time(), scraped_date=time.strftime("%d/%m/%Y")))
	return data






