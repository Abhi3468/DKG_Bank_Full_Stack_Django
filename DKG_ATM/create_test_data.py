import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DKG_ATM.settings')
django.setup()

from BankInterface.models import Account

# Create a test account
account, created = Account.objects.get_or_create(
    card_number="1234567890123456",
    defaults={'card_pin': "1234", 'balance': 1000.00}
)

if created:
    print(f"Created account: {account.card_number} with PIN: {account.card_pin}")
else:
    print(f"Account {account.card_number} already exists.")
