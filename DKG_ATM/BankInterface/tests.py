from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Account, Transaction
import json
import concurrent.futures

class BankConcurrencyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.account = Account.objects.create(
            user=self.user,
            card_number='1234567890123456',
            card_pin='1234',
            balance=Decimal('100.00')
        )
        self.client = Client()

    def test_withdrawal_success(self):
        # Test standard withdrawal via the new DRF API
        response = self.client.post(reverse('BankInterface:withdraw'), json.dumps({
            'card_number': '1234567890123456',
            'amount': 50.00
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('50.00'))

    def test_concurrent_withdrawals_prevent_negative_balance(self):
        """
        Simulate two simultaneous requests trying to withdraw $100 from an account that only has $100.
        Without transaction.atomic() and select_for_update(), both might succeed, leaving a balance of -$100.
        With our Phase 1 fix, one will succeed and the other will safely fail.
        """
        def make_request():
            # Create a separate client for thread
            client = Client()
            return client.post(reverse('BankInterface:withdraw'), json.dumps({
                'card_number': '1234567890123456',
                'amount': 100.00
            }), content_type='application/json')

        # Using Python threading to simulate concurrent API requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(make_request)
            future2 = executor.submit(make_request)
            
            res1 = future1.result()
            res2 = future2.result()

        status_codes = []
        try:
            status_codes.append(res1.status_code)
        except Exception as e:
            pass
            
        try:
            status_codes.append(res2.status_code)
        except Exception as e:
            pass
            
        # Verify balance never dropped below 0
        self.account.refresh_from_db()
        self.assertTrue(self.account.balance >= Decimal('0.00'), "CRITICAL BUG: Balance dropped below zero! Concurrency fix failed.")
        
        # Verify only one transaction was created
        transactions = Transaction.objects.filter(account=self.account, transaction_type='WITHDRAWAL')
        self.assertEqual(transactions.count(), 1, "There should only be exactly one successful transaction.")
