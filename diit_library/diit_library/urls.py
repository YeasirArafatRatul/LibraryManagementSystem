from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from all_books.views import HomeView, BorrowSummuryView, PaymentView, confirm, search, RecordKeeping, send_mail, fine
from slideshow.views import slides, SlideShowView
from payment_system.views import finepayment
from all_books.tasks import fine_users
from background_task.models import Task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('books/', include('all_books.urls')),
    path('borrow-list/', BorrowSummuryView.as_view(), name='borrow-list'),
    path('fine/payment/<payment-option>',
         finepayment, name='fine-payment'),
    path('confirm-request/<int:pk>/',
         confirm, name='confirm-request'),
    path('search/', search, name="search"),
    path('slide/', slides, name='slide'),
    path('slideshow/', SlideShowView.as_view(), name='slideshow'),
    path('admin/records/', RecordKeeping.as_view(), name='records'),
    path('admin/records/fine', fine, name='fine'),
    path('admin/records/fine_paid', PaymentView.as_view(), name='fine-list'),
    path('background/', background_task_view, name="background_task")


]
fine_users(repeat=Task.DAILY)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'DIIT Library'
admin.site.index_title = 'Library Management System'
admin.site.site_title = 'Admin'
