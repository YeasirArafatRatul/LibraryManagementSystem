from django.urls import path
from .views import DetailsView, BorrowSummuryView
from .views import add_to_cart, remove_from_cart


urlpatterns = [
    path('<slug>/', DetailsView.as_view(), name='book-detail'),
    path('<slug>/borrow/', add_to_cart, name='add-to-cart'),
    path('<slug>/remove/', remove_from_cart, name='remove-from-cart'),

]
