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

from BankInterface.models import Account, Transaction, Loan
from BankInterface.serializers import TransactionSerializer, LoanSerializer

class WithdrawalView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        card_number = request.data.get('card_number')
        amount = Decimal(request.data.get('amount', 0))
        
        from django.utils import timezone
        
        with transaction.atomic():
            account = get_object_or_404(Account.objects.select_for_update(), card_number=card_number)
            
            if account.is_locked:
                return Response({'error': 'Account is locked. Transactions are disabled.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Calculate today's total withdrawals
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            todays_withdrawals = Transaction.objects.filter(
                account=account, 
                transaction_type='WITHDRAWAL', 
                timestamp__gte=today_start
            ).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
            
            if todays_withdrawals + amount > account.daily_limit:
                logger.warning(f"SECURITY: Withdrawal limit exceeded attempt for card {card_number}. Amount: ${amount}, Today's Total: ${todays_withdrawals}")
                return Response({'error': f'Daily withdrawal limit exceeded. Remaining limit: ${account.daily_limit - todays_withdrawals}'}, status=status.HTTP_400_BAD_REQUEST)

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
            
            if account.is_locked:
                return Response({'error': 'Account is locked. Transactions are disabled.'}, status=status.HTTP_403_FORBIDDEN)
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
        # Get the account for this user
        account = get_object_or_404(Account, user=request.user)
        
        # 1. Check if account is already locked
        if account.is_locked:
            logger.warning(f"SECURITY: Blocked access attempt to LOCKED account for user {request.user.username}")
            return Response({'message': 'Account is locked due to multiple failed attempts. Please contact support.'}, status=status.HTTP_403_FORBIDDEN)

        # 2. Verify PIN
        if account.card_pin == card_pin:
            # Success: Reset failed attempts
            account.failed_attempts = 0
            account.save()
            logger.info(f"AUDIT: Successful PIN Verification for user {request.user.username}")
            return Response({
                'message': 'Verified', 
                'card_number': account.card_number,
                'account_number': account.account_number,
                'customer_id': account.customer_id,
                'ifsc_code': account.ifsc_code
            })
        else:
            # Failure: Increment failed attempts
            account.failed_attempts += 1
            if account.failed_attempts >= 3:
                account.is_locked = True
                logger.critical(f"SECURITY: Account AUTOMATICALLY LOCKED for user {request.user.username} after 3 failed attempts.")
            account.save()
            
            remaining = 3 - account.failed_attempts
            msg = f"Invalid PIN. {remaining} attempts remaining." if remaining > 0 else "Account locked."
            logger.warning(f"SECURITY: Failed PIN attempt for user {request.user.username}. {msg}")
            return Response({'message': msg}, status=status.HTTP_400_BAD_REQUEST)

class AvailableBalanceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        card_number = request.data.get('card_number')
        account = get_object_or_404(Account, card_number=card_number)
        
        if account.is_locked:
            return Response({'error': 'Account is locked.'}, status=status.HTTP_403_FORBIDDEN)
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
