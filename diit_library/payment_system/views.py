from django.shortcuts import render
from .models import Payment
from .forms import PaymentForm
from django.contrib import messages
from all_books.models import Fine
# Create your views here.


def finepayment(request, commit=True):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_paid = True
        form.save()
        messages.success(request, "Fine Paid")

    context = {
        "form": form,
    }

    return render(request, "payment.html", context)
