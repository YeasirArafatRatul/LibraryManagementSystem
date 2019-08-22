import datetime
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from accounts.models import UserProfile, User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from diit_library.utils import unique_slug_generator

# from book_cart.views import add_to_cart


class Category(models.Model):
    category_name = models.CharField(
        max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class Book(models.Model):
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='books_images', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={"slug": self.slug})

    @property
    def title(self):
        return(name + book_category)


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# Connecting Payment Model with the 'unique_slug_generator' function
pre_save.connect(slug_generator, sender=Book)


class BookNumber(models.Model):
    book_family = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_code = models.CharField(
        max_length=10, null=False, blank=False, unique=True)

    def __str__(self):
        return self.book_code


"""

Borrow functionalities

"""


class BorrowItem(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    borrow_book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    is_added = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_borrowed = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.borrow_book.name} of {self.borrow_book.author}'


class Borrow(models.Model):
    items = models.ManyToManyField(BorrowItem)  # add many items to one order
    # if we delete an order than it doesn't delete the profile
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_borrowed = models.BooleanField(default=False)
    # fine = models.ForeignKey(Payment, null=True, on_delete=models.SET_NULL, blank=True)
    borrow_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(null=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    class Meta:
        ordering = ["-borrow_date"]
        verbose_name_plural = 'Final Borrow Requests'

    def __str__(self):
        return f'{self.borrower.email} (id {self.borrower.id_card_number})'

    def get_book_items(self):
        return self.items.all()

    def get_return_date(self):
        return self.borrow_date + datetime.timedelta(days=7)

    def get_borrow_confirmation(self):
        return reverse('confirm-request', kwargs={"pk": self.pk})

    def get_send_mail(self):
        return reverse('send-mail', kwargs={"pk": self.pk})

    @property
    def title(self):
        return('borrow-request-')


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# Connecting Payment Model with the 'unique_slug_generator' function
pre_save.connect(slug_generator, sender=Borrow)


class Fine(models.Model):
    to_email = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    message = models.TextField(max_length=1000)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Fine List"

    def __str__(self):
        return self.to_email.email
