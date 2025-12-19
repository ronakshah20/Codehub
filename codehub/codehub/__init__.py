# codehub/__init__.py

import firebase_admin
from firebase_admin import credentials
from django.conf import settings
import os

# Build the path to your credentials file in the root directory
cred_path = os.path.join(settings.BASE_DIR, 'firebase_credentials.json')

# Initialize the app if it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
