#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api
from flask.ext.restful import reqparse
import json
from helpers import NewsData, NotValidDateFormatError
from scrape import app_logger

app = Flask(__name__)
app.config.from_pyfile('configs/flask_config.py')
api = Api(app)

news_parser = reqparse.RequestParser()
news_parser.add_argument('skip', type=int, required=True, help="skip should be provided in the arguments", location="args")
news_parser.add_argument('source', type=str, required=False, location="args")
news_parser.add_argument('count', type=int, required=False, location="args")
news_parser.add_argument('published_date', type=str, required=False, location="args")


tag_parser = reqparse.RequestParser()
tag_parser.add_argument('news_list', required=True, help="News List should be provided", location="form")


##Example of simple function which uses the args defined above

class GetNews(Resource):
	"""
	This Class is used to get on the basis of the arguments provided in the get request
	Args:
		source: Source of the news which in our case could be of three types yet.
			HT_NDLS
			HIN_NDLS
			TOI_NDLS
		published_date:
			Get news on the basis of the day it was published.Right now you cannot get news on the basis of 
			source from which its been published and the published date
			Format:
				"18 jun 2014"
		skip:
			News to be skipped in the db before the count starts.For example if skip = 100, 100 latest news will
			be skipped before new news will be delivered.

		count: NUmber of new article to be delivered.
	Exceptions Raised:
		NotVaildDateFormatError:
			when the format of the news is not in the format as mentioned above in puclished date format.

	"""
	def get(self):
		args = news_parser.parse_args()

		if args.get("source"):
			return jsonify(result = NewsData.data_by_source(source=args.get("source"), skip=args.get("skip"), count=args.get("count")),
				error = False,
				succes= True, )


		if args.get("published_date"):
			try:
				return jsonify(result = NewsData.for_date(published_date=args.get("published_date"), skip=args.get("skip"), count=args.get("count")),
						error=False,
						success=True, )
			except NotValidDateFormatError as e:
				return jsonify(error=True,
						success= False,
						messege=e.str(),)
		
		return json.dumps(NewsData.without_tag(skip=args.get("skip"), count=args.get("count") ))


class PostTags(Resource):
	"""
	How to test
	import request
	request = requests.post("http://localhost:5000/tags", data={"news_list": json.dumps(new_data)})
	"""

	def post(self):
		args = tag_parser.parse_args()
		news_list = json.loads(args["news_list"])
		return jsonify(result = NewsData.post_tags(news_list),
				error = False,
				succes= True, )


api.add_resource(GetNews, '/news')
api.add_resource(PostTags, '/tags')
		
if __name__ == "__main__":
	app_logger(app)
	print "kaali"
	app.run(debug=True)

