#!/usr/bin/python
import os
 
virtenv = os.environ['APPDIR'] + '/virtenv/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.6/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except:
    pass
 
# new codes we adding for Django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cherry.settings")
from django.core.wsgi import get_wsgi_application
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', os.environ['OPENSHIFT_APP_NAME']))
application = get_wsgi_application()
# application = django.core.handlers.wsgi.WSGIHandler()


