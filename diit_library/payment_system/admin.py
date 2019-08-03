from django.contrib import admin
from .models import Payment

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'bKash_ac', 'transaction_id', 'is_paid')
    list_filter = ('user', 'bKash_ac', 'is_paid')


admin.site.register(Payment, PaymentAdmin)
