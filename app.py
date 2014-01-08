#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api
from flask.ext.restful import reqparse
import json
import imp
from scrape import app_logger

"""
path = "%s/scrape"%os.path.dirname(os.path.realpath(__file__))
print path
sys.path.append(path)

from custom_logging import app_logger
"""
app = Flask(__name__)
app.config.from_pyfile('configs/flask_config.py')
api = Api(app)


tag_name_parser = reqparse.RequestParser()
tag_name_parser.add_argument('tag', type=str, required=True, help="Tag nname should be provided in the arguments", location="args")


image_parser = reqparse.RequestParser()
image_parser.add_argument('tag', type=str, required=True, help="Tag name should be provided in the arguments", location="args")
image_parser.add_argument('size', type=str, location="args")
image_parser.add_argument('count', type=str, location="args")


"""
parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name', type=str)
args = parser.parse_args()
parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")

#Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', type=str, location='headers')

# From http cookies
parser.add_argument('session_id', type=str, location='cookies')

# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
args = parser.parse_args()

##Example of simple function which uses the args defined above

class TodoSimple(Resource):
	def get(self, todo_id):
		return {todo_id: todos[todo_id]}

	def put(self, todo_id):
		todos[todo_id] = request.form['data']
		return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')



class TagsName(Resource):
	This method name return the tags names matching the tag name provided by the user in the get arguments

	def get(self):
		args = tag_name_parser.parse_args()
		print args, CLIENT_ID, CLIENT_SECRET
		instance = Instagram(CLIENT_ID, CLIENT_SECRET)
		data = instance.tag_names(args["tag"])
		data = [str(tag) for tag in data]
		return jsonify(data)

class PopularImages(Resource):

	def get(self):
		instance = Instagram(CLIENT_ID, CLIENT_SECRET)
		return json.dumps(instance.popular_images())

class ImagesByTag(Resource):

	def get(self):
		args = image_parser.parse_args()
		instance = Instagram(CLIENT_ID, CLIENT_SECRET)
		data = instance.images_by_tag(args["tag"], args["size"], args["count"])
		if data[0].get("image") is None:
			return json.dumps({
				"error": True,
				"messege": "You have not entered valid resolution size.\n Try entering.\n thumnail.\n standard_resolution.\n or low_resolution.\n" 
				})
		data = [str(tag) for tag in data]
		return json.dumps(data)

api.add_resource(TagsName, '/tags')
api.add_resource(PopularImages, '/popularImages')
api.add_resource(ImagesByTag, '/ImagesByTag')
"""		
		
if __name__ == "__main__":
	app_logger(app)
