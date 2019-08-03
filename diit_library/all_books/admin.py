from django.contrib import admin
from .models import Book, BookNumber, Category
from .models import Borrow, BorrowItem
# Register your models here.


class BorrowAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'ref_code', 'borrow_date',
                    'return_date', 'is_borrowed')
    list_filter = ('borrower', 'items', 'ref_code',
                   'borrow_date', 'return_date')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'quantity')
    list_filter = ('name', 'author', 'book_category')


class BookNumberAdmin(admin.ModelAdmin):
    list_display = ('book_code', 'book_family')


admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(BookNumber, BookNumberAdmin)


admin.site.register(Borrow, BorrowAdmin)
admin.site.register(BorrowItem)
