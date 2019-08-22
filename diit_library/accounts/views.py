from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.views.generic import CreateView


# Create your views here.


class SignUpView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('home')
