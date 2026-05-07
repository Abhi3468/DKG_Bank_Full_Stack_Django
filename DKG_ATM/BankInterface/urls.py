from django.urls import path
from .views import (
    WithdrawalView, DepositView, PinChangeView, 
    VerifyPinView, AvailableBalanceView, TransactionHistoryView, 
    GenerateReceiptView, AnalyticsView, LoanRequestView
)

app_name = 'BankInterface'

urlpatterns = [
    path('verify_pin/', VerifyPinView.as_view(), name='verify_pin'),
    path('available_balance/', AvailableBalanceView.as_view(), name='available_balance'),
    path('withdraw/', WithdrawalView.as_view(), name='withdraw'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('pin_change/', PinChangeView.as_view(), name='pin_change'),
    path('loan_request/', LoanRequestView.as_view(), name='loan_request'),
    path('history/<str:card_number>/', TransactionHistoryView.as_view(), name='transaction_history'),
    path('receipt/<int:transaction_id>/', GenerateReceiptView.as_view(), name='generate_receipt'),
    path('analytics/<str:card_number>/', AnalyticsView.as_view(), name='analytics'),
]
