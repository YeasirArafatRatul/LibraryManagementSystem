import datetime
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from slideshow.models import SlideShow
from payment_system.models import Payment
from .models import Book
from accounts.models import UserProfile, User
from .models import Borrow, BorrowItem, Fine
from diit_library.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from all_books.forms import FineForm
# from all_books.tasks import fine_user
# from background_task import background


class HomeView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 12
    template_name = 'all_books/home.html'  # books/home.html
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = SlideShow.objects.all()
        return context


class DetailsView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'all_books/book_detail.html'
    context_object_name = 'book'


class BorrowSummuryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            borrow = Borrow.objects.get(
                borrower=self.request.user, is_borrowed=False)
            context = {
                'object': borrow
            }
            return render(self.request, 'all_books/borrow_list.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You didn't add any book in the list")
            return redirect('home')

        return render(self.request, "all_books/borrow_list.html")


@login_required
def add_to_cart(request, slug):  # slug is the book-slug
    book = get_object_or_404(Book, slug=slug)
    borrow_item, created = BorrowItem.objects.get_or_create(
        borrow_book=book,
        borrower=request.user,
        is_added=False)
    borrow_qs = Borrow.objects.filter(
        borrower=request.user, is_borrowed=False)

    if borrow_qs.exists():
        borrow = borrow_qs[0]
        if borrow.items.filter(borrow_book__slug=book.slug).exists():
         # check if the item is in the list
            #borrow_item.quantity += 0
            # borrow_item.save()
            messages.info(request, "You can not borrow the same book twice.")
        else:
            messages.info(request, "Item is added to the borrow list.")
            borrow.items.add(borrow_item)
    else:
        borrow_date = timezone.now()
        borrow = Borrow.objects.create(
            borrower=request.user, borrow_date=borrow_date)
        borrow.items.add(borrow_item)
        messages.info(request, "Item is added to the borrow list .")
    return redirect("home")


@login_required
def remove_from_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    borrow_qs = Borrow.objects.filter(
        borrower=request.user, is_borrowed=False)
    if borrow_qs.exists():
        borrow = borrow_qs[0]
        if borrow.items.filter(borrow_book__slug=book.slug).exists():
            borrow_item = BorrowItem.objects.filter(
                borrow_book=book,
                borrower=request.user,
                is_added=False)[0]
            borrow_item.delete()
            # borrow.items.remove(borrow_item)
            messages.info(request, "Item is removed from the borrow list.")
            return redirect("borrow-list")
        else:
            messages.info(request, "Item is not in the borrow list.")
            return redirect("book-detail", slug=slug)
    else:
        messages.info(request, "Item is not in the borrow list.")
        return redirect("borrow-list")
    return redirect("borrow-list")


@login_required
def confirm(request, pk):
    if request.method == 'POST':
        try:
            borrow = Borrow.objects.get(
                pk=pk, borrower=request.user, is_borrowed=False)
            borrow.is_borrowed = True
            current_date = timezone.now()
            borrow.return_date = current_date + datetime.timedelta(days=7)
            borrow.save()
            messages.info(
                request, "Your Request Is Submitted To The Librarian")
        except Borrow.DoesNotExist:
            return HttpResponse('Product not found', status=404)
        except Exception:
            return HttpResponse('Internal Error', status=500)
    else:
        return HttpResponse('Method not allowed', status=405)
    return redirect("home")


@login_required
def search(request):
    if request.GET:
        search_term = request.GET['search_term']
        search_results = Book.objects.filter(
            Q(name__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(book_category__category_name__icontains=search_term)
        )

        context = {
            'search_term': search_term,
            'books': search_results.filter()
        }
        return render(request, 'search.html', context)

    else:
        return redirect('home')


class RecordKeeping(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = 'custom_admin_site/record.html'
    context_object_name = 'borrowed_list'


# this function works well when i call it.

def fine(request, commit=True):
    form = FineForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        to_email = form.cleaned_data.get("to_email")
        amount = form.cleaned_data.get("amount")
        message = form.cleaned_data.get("message")
        subject = 'You are Fined'
        from_email = EMAIL_HOST_USER
        formatted_message = f'{message + "Payable amount:" + str(amount)}'
        reciever = [instance.to_email.email]
        send_mail(subject=subject, message=formatted_message, from_email=from_email,
                  recipient_list=reciever, fail_silently=False)
        form.save()
        messages.success(request, "Email Sent Succesfully")

    context = {
        "form": form,
    }

    return render(request, "custom_admin_site/fine.html", context)


class PaymentView(LoginRequiredMixin, ListView):
    model = Fine
    template_name = 'custom_admin_site/fine_paid.html'
    context_object_name = 'fines'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        return context


# just checking
# @background(schedule=10)
# def hello():
#     subject = "Hello"
#     message = "Checking ... function...Boss"
#     from_email = EMAIL_HOST_USER

#     send_mail(subject=subject, message=message, from_email=from_email,
#               recipient_list=['itsaiub@gmail.com', ], fail_silently=False)
#     print("email sent")

#     print("Hello Ratul!")


# def background_task_view(request):
#      hello()
#     return HttpResponse("Hello World")
