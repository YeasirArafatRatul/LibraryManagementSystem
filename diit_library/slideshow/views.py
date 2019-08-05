from django.shortcuts import render
from . models import SlideShow
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.


def slides(request):
    """Main listing."""
    slides = SlideShow.objects.get(id=1)
    return render("partials/_slider.html")
