from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from decimal import Decimal
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.db.models import Sum
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

import logging
logger = logging.getLogger('bank_audit')

from .models import Account, Transaction, Loan
from .serializers import TransactionSerializer, LoanSerializer

class WithdrawalView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        card_number = request.data.get('card_number')
        amount = Decimal(request.data.get('amount', 0))
        
        with transaction.atomic():
            account = get_object_or_404(Account.objects.select_for_update(), card_number=card_number)
            if account.balance < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
            
            account.balance -= amount
            account.save()
            
            Transaction.objects.create(
                account=account, 
                amount=amount, 
                transaction_type='WITHDRAWAL',
                description='ATM Withdrawal'
            )
            logger.info(f"AUDIT: Successful Withdrawal of ${amount} from card {card_number}. New Balance: ${account.balance}")
            
        return Response({'message': 'Withdrawal successful', 'new_balance': account.balance})

class DepositView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        card_number = request.data.get('card_number')
        amount = Decimal(request.data.get('amount', 0))
        
        with transaction.atomic():
            account = get_object_or_404(Account.objects.select_for_update(), card_number=card_number)
            account.balance += amount
            account.save()
            
            Transaction.objects.create(
                account=account, 
                amount=amount, 
                transaction_type='DEPOSIT',
                description='ATM Deposit'
            )
            logger.info(f"AUDIT: Successful Deposit of ${amount} to card {card_number}. New Balance: ${account.balance}")
            
        return Response({'message': 'Deposit successful', 'new_balance': account.balance})

class PinChangeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        card_number = request.data.get('card_number')
        new_pin = request.data.get('new_pin')
        account = get_object_or_404(Account, card_number=card_number)
        account.card_pin = new_pin
        account.save()
        return Response({'message': 'PIN changed successfully'})

class VerifyPinView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'message': 'Session expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        card_pin = request.data.get('card_pin')
        try:
            account = Account.objects.get(user=request.user, card_pin=card_pin)
            logger.info(f"AUDIT: Successful PIN Verification for user {request.user.username}")
            return Response({'message': 'Verified', 'card_number': account.card_number})
        except Account.DoesNotExist:
            logger.warning(f"SECURITY: Failed PIN Verification attempt for user {request.user.username}")
            return Response({'message': 'Invalid PIN'}, status=status.HTTP_400_BAD_REQUEST)

class AvailableBalanceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        card_number = request.data.get('card_number')
        account = get_object_or_404(Account, card_number=card_number)
        return Response({'balance': account.balance})

class TransactionHistoryView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, card_number):
        account = get_object_or_404(Account, card_number=card_number)
        transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
        
        if getattr(request, 'accepted_renderer', None) and request.accepted_renderer.format == 'html':
            return render(request, 'history.html', {'history': transactions, 'account': account})
        
        # Fallback to HTML if not specifically asking for JSON, to keep old UI working
        if 'application/json' not in request.META.get('HTTP_ACCEPT', ''):
             return render(request, 'history.html', {'history': transactions, 'account': account})
             
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class GenerateReceiptView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, transaction_id):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        obj = get_object_or_404(Transaction, id=transaction_id)
            
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(300, 750, "DKG BANK ATM")
        p.setFont("Helvetica", 14)
        p.drawCentredString(300, 730, f"{obj.transaction_type} RECEIPT")
        p.line(100, 710, 500, 710)
        p.drawString(100, 680, f"Date: {obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        p.drawString(100, 660, f"Card Number: **** **** **** {obj.account.card_number[-4:]}")
        p.drawString(100, 640, f"Transaction ID: {obj.id}")
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 610, f"Amount: ${obj.amount}")
        p.setFont("Helvetica", 12)
        p.drawString(100, 580, f"Balance: ${obj.account.balance}")
        p.line(100, 550, 500, 550)
        p.drawCentredString(300, 530, "Thank you for banking with us!")
        p.showPage()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

class LoanRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        card_number = request.data.get('card_number')
        amount = Decimal(request.data.get('amount', 0))
        account = get_object_or_404(Account, card_number=card_number)
        Loan.objects.create(account=account, loan_amount=amount)
        return Response({'message': 'Loan application submitted for review'})

class AnalyticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, card_number):
        account = get_object_or_404(Account, card_number=card_number)
        withdrawals = Transaction.objects.filter(account=account, transaction_type='WITHDRAWAL').aggregate(Sum('amount'))['amount__sum'] or 0
        deposits = Transaction.objects.filter(account=account, transaction_type='DEPOSIT').aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({
            'withdrawals': float(withdrawals),
            'deposits': float(deposits)
        })
