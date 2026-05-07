import os
import django
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DKG_ATM.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='Abhishek')
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
except User.DoesNotExist:
    print("User 'Abhishek' does not exist.")
except Exception as e:
    print("Error:", str(e))
