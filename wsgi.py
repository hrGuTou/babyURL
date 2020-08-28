#!/usr/bin/env python

import sys
import site

site.addsitedir('/var/www/babyURL/venv/lib/python3.7/site-packages')
sys.path.insert(0, '/var/www/babyURL')

from run import app as application