#!/usr/bin/env python


DEBUG = True

def custom_debugger():
            import logging
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler('python.log', maxBytes=1023 * 1024 * 100, backupCount=20)
            file_handler.setLevel(logging.ERROR)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            app.logger.addHandler(file_handler)
