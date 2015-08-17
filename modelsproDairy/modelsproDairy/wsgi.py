"""
WSGI config for modelspro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site

try:
    #site.addsitedir('/home/user/developer/foo/lib/python3.4/site-packages')
    site.addsitedir('/home/user/developer/bar/lib/python3.4/site-packages')

    sys.path.append('/home/user/github/05Aug15/WebDairy/modelsproDairy')
    #sys.path.append('/home/user/github/24Jul15/WebDairy/modelsproDairy/modelsproDairy')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modelsproDairy.settings")

    # Activate your virtual env
    activate_env=os.path.expanduser("/home/user/developer/bar/bin/activate_this.py")
    #execfile(activate_env, dict(__file__=activate_env))
    exec(compile(open(activate_env).read(),activate_env,'exec'), dict(__file__=activate_env))
except Exception as e:
    print ("Exception occured ")
    print (e)
    sys.exit(-1)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
