#!/usr/bin/python3
import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/babyURL/")

def application(environ, start_response):
    for key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'REDIS_HOST', 'REDIS_PORT', 'REDIS_PWD ', 'DOMAIN']:
        os.environ[key] = environ.get(key, '')

    from babyURL import app as application
    return application(environ, start_response)
