from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='Savings')
    card_number = models.CharField(max_length=16, unique=True)
    card_pin = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    daily_limit = models.DecimalField(max_digits=12, decimal_places=2, default=1000.00)
    is_locked = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)
    account_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    customer_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
    ifsc_code = models.CharField(max_length=11, default="DKGB0000001")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        import random
        import string
        if not self.account_number:
            while True:
                acc_num = ''.join(random.choices(string.digits, k=12))
                if not Account.objects.filter(account_number=acc_num).exists():
                    self.account_number = acc_num
                    break
        if not self.customer_id:
            while True:
                cust_id = ''.join(random.choices(string.digits, k=8))
                if not Account.objects.filter(customer_id=cust_id).exists():
                    self.customer_id = cust_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.card_number}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('WITHDRAWAL', 'Withdrawal'),
        ('DEPOSIT', 'Deposit'),
        ('LOAN_DISBURSEMENT', 'Loan Disbursement'),
        ('LOAN_REPAYMENT', 'Loan Repayment'),
        ('TRANSFER', 'Transfer'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

class Loan(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CLOSED', 'Closed'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} - {self.status}"
