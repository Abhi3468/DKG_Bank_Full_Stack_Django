from rest_framework import serializers
from .models import Account, Transaction, Loan

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['card_number', 'account_type', 'balance', 'created_at']
        read_only_fields = ['balance', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'timestamp', 'description']
        
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'loan_amount', 'interest_rate', 'status', 'created_at']
