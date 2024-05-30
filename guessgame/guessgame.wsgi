import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/guessgame")

from app import app as application
application.secret_key = 'supersecretkey'
