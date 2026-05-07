import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DKG_ATM.settings')
django.setup()

from django.contrib.auth.models import User
from BankInterface.models import Account

username = "testuser"
email = "test@example.com"
password = "testpassword123"

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
if created:
    user.set_password(password)
    user.save()
    Account.objects.get_or_create(user=user, defaults={'card_number': "1111222233334444", 'card_pin': "1111", 'balance': 5000.00})
    print(f"Created user: {username}")
else:
    print(f"User {username} already exists.")
