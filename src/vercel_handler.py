import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruit_and_veg.settings')
application = get_wsgi_application()

# Vercel requires an 'app' variable
app = application
