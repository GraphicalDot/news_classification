#!/usr/bin/env python


import os
import goose
import time
import logging
from rss_feeds import hindustan_ndls_rss, toi_ndls_rss, hindu_ndls_rss
from custom_logging import exceptions_logging
_g_instance = goose.Goose()


def extracting_text(link):
	try:
		extract = _g_instance.extract(link)
		time.sleep(5)
		return extract.cleaned_text
	except Exception as e:
		exceptions_logging(e)

def hindustan_ndls_data():
	data = hindustan_ndls_rss()
	for news in data:
		news["full_text"] =  extracting_text(news.get("link"))
	return data


def hindu_ndls_data():
	data = hindu_ndls_rss()
	for news in data[0:1]:
		news["full_text"] =  extracting_text(news.get("link"))
	return data



def toi_ndls_data():
	data = toi_ndls_rss()
	for news in data:
		news["full_text"] =  extracting_text(news.get("link"))
	return data






