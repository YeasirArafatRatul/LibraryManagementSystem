from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('user', 'amount', 'bKash_ac', 'transaction_id')
