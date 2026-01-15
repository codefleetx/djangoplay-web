import os
import sys
from pathlib import Path

# Ensure the project directory is in the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paystream.settings')

from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
except Exception as e:
    import traceback
    traceback.print_exc()
    raise e
