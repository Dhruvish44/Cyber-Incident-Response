# config.py

import os

SECRET_KEY = os.environ.get('SECRET_KEY', '80d4b6b52d9c9cb49d7f42358c76b6d9be2af6bf4b1a70d8e6d0a59489793c7b')
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
