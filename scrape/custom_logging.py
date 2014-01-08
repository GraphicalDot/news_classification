#!/usr/bin/env python

from __future__ import absolute_import 
import logging
from logging.handlers import RotatingFileHandler
import os
LOGGING_PATH = os.path.dirname(os.path.realpath(__file__))

def exceptions_logger(error):
	path = "%s/exception_logs.logs"%(LOGGING_PATH)
	log = logging.getLogger("Exceptions_Logs")
	handler = RotatingFileHandler(path, maxBytes=10000, backupCount=1)
				        
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s %(module)s [in %(pathname)s:%(lineno)d]')
						   
	handler.setFormatter(formatter)
	log.addHandler(handler)
	log.error(error)
	return

def app_logger(app):
	path = "%s/flask_error_logs.logs"%(LOGGING_PATH)
	my_logger = logging.getLogger('MyLogger')

#	my_logger.setLevel(logging.DEBUG)

	handler = RotatingFileHandler(path, maxBytes=10000, backupCount=1)
	
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s %(module)s [in %(pathname)s:%(lineno)d]')
	
	handler.setFormatter(formatter)
	
	app.logger.addHandler(handler)

	#This will write a messge mentioned in the brackets whenever that kind of error occurred in the application
	app.logger.error('An error occurred')
	app.logger.debug('A value for debugging')
	app.logger.warning('A warning occurred (%d apples)', 42)
	app.logger.info("My App")
	return
