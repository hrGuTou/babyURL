#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/babyURL/")
sys.path.insert(0,"~/.aws/")

from babyURL import app as application
application.secret_key = 'giao!'