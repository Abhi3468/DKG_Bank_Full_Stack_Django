from django.contrib import admin
from .models import Account, Transaction, Loan

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'account_type', 'balance', 'is_locked', 'failed_attempts')
    search_fields = ('card_number', 'user__username')
    list_filter = ('account_type', 'is_locked')

admin.site.register(Transaction)
admin.site.register(Loan)
