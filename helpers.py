#!/usr/bin/env python

from scrape import DB, DBInsert
from scrape import collection as C

collection = C("News")
fields = ["_id", "full_text", "source", "scraped_date", "link", "tag"]

class NewsData(object):
	"""
	This class is used to pop out data or news articles on the basis of sevel params provided.

	'_id': id of the news given by mongodb
	'full_text', : Full text of the news
	'headline', : Headline of the news
	'published', : Published date of the news as was written on the website in human readble format
	'scraped_date', : human readable time stamp of the format dd/mm/yy when the news was scraped
	'summary',: Summary of the news article
	'source',: Source of the news i.e name of the website
		TOI_NDLS
		HIN_NDLS
		HT_NDLS
	'scraped_epoch', : Time in Epoch when the news was scraped and stored in database
	'link',: link of the news
	'published_date', : Time in seconds since epoch when the news was published
	"tag": Which is mostly empty and contains tag of the news 
	"""
	
	def __init__(self):
		pass

	@staticmethod
	def data_by_source(source, count=None, skip):
	"""
	This method will be used when a user asked for data for a particular source, If count is not provided all the
	data belonging to a source will be deleivered.
	Args:
		source:
			type=str 
		count: 
			type=int, Default is None, if count is provided that much news is deleivered
		skip: 
			type=int, Used for paging, if skip is 100, then 100 news, after sorting(newest to oldest) 
			will be skipped while deleivering.
	"""
		if count:
			
			data = [post for post in self.collection.find({"source": self.source}, fields=fields, sort =[("scraped_epoch", 1)], limit=count, skip=skip)]
			
			return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")  ) for news in data]

		
		data = [post for post in self.collection.find({"source": self.source}, fields=fields, sort =[("scraped_epoch", 1)], skip=skip)]
		
		return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")  ) for news in data]


	@staticmethod
	def without_tag(count=None, skip):w
	"""
	This method will be used when a user asked for data without source, If count is not provided all the
	data present in the database will be sent.
	Args:
		count: 
			type=int, Default is None, if count is provided that much news is deleivered
		skip: 
			type=int, Used for paging, if skip is 100, then 100 news, after sorting(newest to oldest) 
			will be skipped while deleivering.
	"""
		if count:
			
			data = [post for post in self.collection.find(fields=fields, sort=[("scraped_epoch", 1)], limit=count, skip=skip)]
			
			return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]
		
		data = [post for post in self.collection.find(fields=fields, sort=[("scraped_epoch", 1)], skip=skip)]
		return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]
	
	

	def for_date(published_date, count=None, skip):
	"""
	This method will be used when a user asked for data for a particular date, If count is not provided all the
	data belonging to a source will be deleivered.The date will be in format "dd mm yy"
	Args:
		published_date: 
			type= str, ex: 08 Jan 2014
		count: 
			type=int, Default is None, if count is provided that much news is deleivered
		skip: 
			type=int, Used for paging, if skip is 100, then 100 news, after sorting(newest to oldest) 
			will be skipped while deleivering.
	"""
		if count:

			data = [post for post in collection.find({"published": {"$regex": published_date, "$options": 'i'}}, fields=fields, limit=count, skip=skip)]
			
			return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]
			
		data = [post for post in collection.find({"published": {"$regex": published_date, "$options": 'i'}}, fields=fields, skip=skip)]
		
		return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]




