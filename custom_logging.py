#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import 
import logging
from logging.handlers import RotatingFileHandler
from variables import LOGGING_PATH

def exceptions_logging(error):
	print LOGGING_PATH
	path = "%s/exception_logs.logs"%(LOGGING_PATH)
	log = logging.getLogger("Exceptions_Logs")
	handler = RotatingFileHandler(path, maxBytes=10000, backupCount=1)
	
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s %(module)s [in %(pathname)s:%(lineno)d]')
	
	handler.setFormatter(formatter)
	log.addHandler(handler)
	log.error(error)

def app_logger(app):
	my_logger = logging.getLogger('MyLogger')

#	my_logger.setLevel(logging.DEBUG)
	handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10000, backupCount=1)
	
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s %(module)s [in %(pathname)s:%(lineno)d]')
	
	handler.setFormatter(formatter)
	
	app.logger.addHandler(handler)

	#This will write a messge mentioned in the brackets whenever that kind of error occurred in the application
	app.logger.error('An error occurred')
	app.logger.debug('A value for debugging')
	app.logger.warning('A warning occurred (%d apples)', 42)
	app.logger.info("My App")


