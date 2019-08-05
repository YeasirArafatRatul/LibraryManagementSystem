from .models import Book
from accounts.models import UserProfile, User
from .models import Borrow, BorrowItem
# from .forms import ConfirmationForm

import datetime
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 12
    template_name = 'all_books/home.html'  # books/home.html
    context_object_name = 'books'


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


class PaymentView(View):

    def get(self, *args, **kwargs):
        return render(self.request, "payment.html")


@login_required
def confirm(request, pk):
    if request.method == 'POST':
        try:
            borrow = Borrow.objects.get(
                pk=pk, borrower=request.user, is_borrowed=False)
            borrow.is_borrowed = True
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


# class ConfirmView(View):
#     def get(self, *args, **kwargs):
#         return render(self.request, "all_books/borrow_list.html")

#     def post(self, *args, **kwargs):
#         borrow = Borrow.objects.get(
#             borrower=self.request.user, is_borrowed=False)
#         borrow.is_borrowed = True
#         borrow.borrow_date = datetime.now()
#         borrow.return_date = borrow.borrow_date + datetime.timedelta(days=7)
#         borrow.save()
#         return redirect('home')


@login_required
def search(request):
    if request.GET:
        search_term = request.GET['search_term']
        search_results = Book.objects.filter(
            Q(name__icontains=search_term) |
            Q(author__icontains=search_term)
        )

        context = {
            'search_term': search_term,
            'books': search_results.filter()
        }
        return render(request, 'search.html', context)

    else:
        return redirect('home')
