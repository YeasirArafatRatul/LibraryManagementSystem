from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from accounts.models import UserProfile, User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    name = models.CharField(max_length=20)
    author = models.CharField(max_length=30)
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


"""
def unique_slug_generator(instance, new_slug):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.name)

	Klass = instance.__class__
	qs_exists = Klass.objects.filter(slug=slug).exists()
	if qs_exists:
		new_slug=f"{category_name}-{name}-{author}"
		return unique_slug_generator(instance,new_slug=new_slug)
	return slug
"""


class BookNumber(models.Model):
    book_family = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_code = models.CharField(
        max_length=10, null=False, blank=False, unique=True)

    def __str__(self):
        return self.book_code


# Borrow functionalities
class Payment(models.Model):
    pass


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
    ref_code = models.CharField(max_length=15, null=True, blank=True)
    # add many items to one order
    items = models.ManyToManyField(BorrowItem)
    # if we delete an order than it doesn't delete the profile
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    is_borrowed = models.BooleanField(default=False)
    fine = models.ForeignKey(
        Payment, null=True, on_delete=models.SET_NULL, blank=True)
    borrow_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-borrow_date"]
        verbose_name_plural = 'Final Borrow Requests'

    def __str__(self):
        return f'{self.borrower.email} (id {self.borrower.id_card_number})'

    def get_book_items(self):
        return self.items.all()
