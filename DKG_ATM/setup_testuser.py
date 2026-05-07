import os
import django
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DKG_ATM.settings')
django.setup()

from django.contrib.auth.models import User
from django.conf import settings

print("Checking testuser...")
try:
    user, created = User.objects.get_or_create(username='testuser')
    user.email = settings.EMAIL_HOST_USER
    if created:
        user.set_password('testpassword123')
    user.save()
    print(f"Test user email set to: {user.email}")
except Exception as e:
    print("Error updating user:", str(e))
