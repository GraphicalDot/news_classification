#!/usr/bin/env python

from scrape import DB, DBInsert
from scrape import collection as C
import re
from bson import ObjectId

collection = C("News")
fields = ["_id", "full_text", "source", "scraped_date", "link", "tag"]

class NewsData(object):
	"""
	This class is used to pop out data or news articles on the basis of several params provided.

	Following are the keys stored for each news present in the databse.
	_id: id of the news as stored by mongodb
	full_text : Full text of the news
	headline : Headline of the news
	published : Published date of the news as was written on the website in human readble format
	scraped_date : human readable time stamp of the format dd/mm/yy when the news was scraped
	summary : Summary of the news article
	source : Source of the news i.e name of the website
		TOI_NDLS
		HIN_NDLS
		HT_NDLS
	scraped_epoch : Time in Epoch when the news was scraped and stored in database
	link : link of the news
	published_date : Time in seconds since epoch when the news was published
	tag : Which is mostly empty and contains tag of the news when marked.
	
	"""
	
	def __init__(self):
		pass

	
	@staticmethod
	def data_by_source(source, skip, count=None,):
		"""
		This method will be used when a user asked for data for a particular source, If count is not provided all the
		data belonging to a source will be delivered.
		Args:
			source:
				type=str 
			count: 
				type=int, Default is None, if count is provided that much news is deleivered
			skip: 
				type=int, Used for paging, if skip is 100, then 100 news, after sorting(newest to oldest) 
				will be skipped while delivering.

		"""
		if count:
			
			data = [post for post in collection.find({"source": source}, fields=fields, sort =[("scraped_epoch", 1)], limit=count, skip=skip)]
			
			return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")  ) for news in data]

		
		data = [post for post in collection.find({"source": source}, fields=fields, sort =[("scraped_epoch", 1)], skip=skip)]
		
		return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")  ) for news in data]


	@staticmethod
	def without_tag(skip, count=None,):
		"""
		This method will be used when a user asked for data without source, If count is not provided all the
		data present in the database will be sent.
		Args:
			count: 
				type=int, Default is None, if count is provided that much news is deleivered
			skip: 
				type=int, Used for paging, if skip is 100, then 100 news, after sorting(newest to oldest) 
				will be skipped while delivering.
		"""	
		if count:
			
			data = [post for post in collection.find(fields=fields, sort=[("scraped_epoch", 1)], limit=count, skip=skip)]
			
			return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]
		
		data = [post for post in collection.find(fields=fields, sort=[("scraped_epoch", 1)], skip=skip)]
		return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]
	
	@staticmethod
	def for_date(published_date, skip, count=None,):
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
				will be skipped while delivering.
		"""
		if not re.search("\d{2}\s+\w{3}\s+\d{4}", published_date):
			raise NotValidDateFormatError

		if count:

			data = [post for post in collection.find({"published": {"$regex": published_date, "$options": 'i'}}, fields=fields, limit=count, skip=skip)]
			
			return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]
			
		data = [post for post in collection.find({"published": {"$regex": published_date, "$options": 'i'}}, fields=fields, skip=skip)]
		
		return [dict(id=str(news.get("_id")), full_text=news.get("full_text"), source=news.get("source"), link=news.get("link"), tag=news.get("tag")) for news in data]


	@staticmethod
	def post_tags(news_list):
		"""
		This function is used to tag or edit their tags of the news posts present in the database
		Args:
			news_list: list of dictionaries with each dictionary having id and tag as keys
		Variables:
			invalid_ids: List of ids which are not present in the database
			scraped_ids: List of ids which are either shorter then 24 digits or have empty tags
			success_ids: List of ids which are successfully updated._
		"""
			
		invalid_ids = list()

		def edit_db(id, tag):
			if collection.find_one({"_id": ObjectId(id)}):
				collection.update({"_id": id}, {"$set": {"tag": tag}})	
				return
			invalid_ids.append(id)
			return 

		#Below is the list which have all the id which have discrepancy wither in their id or in their tag empty
		scraped_ids = [entry.get("id") for entry in news_list if len(entry.get("id")) < 24 or entry.get("tag") == ""]

		#Below is the list which have id of length 24 and non empty tags
		success_ids = [news for news in news_list if not news.get("id") in scraped_ids]
				
		for entry in success_ids:
			edit_db(entry.get("id"), entry.get("tag"))

		success_ids = [news for news in news_list if not news.get("id") in invalid_ids]
			
		return dict(invalid_ids=invalid_ids, scraped_ids=scraped_ids, success_ids=success_ids)




class NotValidDateFormatError(Exception):
	def __init__(self):
		pass

	def str(self):
		return "Not a valid date format, should be like '18 jun 1985'"


class EntryDoesntExistsError(Exception):
	def __init__(self, id):
		self.id = id	

	def str(self):
		return "The news corresponding to %s id doesnt exists in the database"%(self.id)
