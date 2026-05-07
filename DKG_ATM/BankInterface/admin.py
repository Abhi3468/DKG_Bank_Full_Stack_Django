from django.contrib import admin
from .models import Account, Transaction, Loan

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Loan)
