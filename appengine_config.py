"""`appengine_config` gets loaded when starting a new application instance."""
import sys
import os.path
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

# NOTE: You must change this to a random 16 character string
SECRET_KEY='0000000000000000'

if SECRET_KEY == '0000000000000000' or len(SECRET_KEY) < 16:
    print "ERROR: Invalid SECRET_KEY. You must specify a complex secret key at least 16 characters long"
    sys.exit(1)
