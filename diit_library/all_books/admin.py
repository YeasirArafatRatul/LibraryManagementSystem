from django.contrib import admin
from .models import Book, BookNumber, Category
from .models import Borrow, BorrowItem, Fine
# Register your models here.


class BorrowAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'slug', 'borrow_date',
                    'return_date', 'is_borrowed')
    list_filter = ('borrower', 'items', 'slug',
                   'borrow_date', 'return_date')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'quantity')
    list_filter = ('name', 'author', 'book_category')


class BookNumberAdmin(admin.ModelAdmin):
    list_display = ('book_code', 'book_family')


class FineAdmin(admin.ModelAdmin):
    list_display = ('to_email', 'amount', 'date')
    list_filter = ('to_email', 'date')


admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(BookNumber, BookNumberAdmin)


admin.site.register(Borrow, BorrowAdmin)
admin.site.register(BorrowItem)
admin.site.register(Fine, FineAdmin)
