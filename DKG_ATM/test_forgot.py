import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DKG_ATM.settings')
django.setup()

from django.test import Client
c = Client(SERVER_NAME='localhost')
try:
    response = c.post('/forgot-password/', {'email': 'abhishekr0313@gmail.com'})
    print("STATUS CODE:", response.status_code)
    print("CONTENT:", response.content.decode('utf-8'))
except Exception as e:
    print("EXCEPTION:", e)
