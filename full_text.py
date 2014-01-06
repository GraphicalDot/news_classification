#!/usr/bin/env python


import os
import goose
import time
import logging
from rss_feeds import hindustan_ndls_rss, toi_ndls_rss
_g_instance = goose.Goose()


def extracting_text(link):
	try:
		extract = _g_instance.extract(link)
		time.sleep(5)
		return extract.cleaned_text
	except Exception as e:
		pass

def hindustan_ndls_text():
	for news in hindustan_ndls_rss():
		news["full_text"] =  extracting_text(news.get("link"))
	return data



def toi_ndls_text():
	for news in toi_ndls_rss():
		news["full_text"] =  extracting_text(news.get("link"))
	return data










