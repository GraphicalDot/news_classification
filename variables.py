#!/usr/bin/env python

import os
import sys
from pymongo import MongoClient

HINDUSTAN_TIMES_NDLS = "http://www.hindustantimes.com/HT-feed/FeedXml.aspx?c=NewDelhi"
TOI_NDLS = "http://timesofindia.feedsportal.com/c/33039/f/533976/index.rss"
HINDU_NDLS = "http://www.thehindu.com/news/cities/Delhi/?service=rss"
LOGGING_PATH = os.path.dirname(os.path.realpath(__file__))

CONNECTION = MongoClient("localhost", 27017, w=1, j=True)
DB = CONNECTION.news
#wValue == 1 perform a write acknowledgement
#journal(j) true: Sync to journal.

