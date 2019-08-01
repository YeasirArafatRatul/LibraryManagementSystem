from django import template
from all_books.models import Borrow

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        query_set = Borrow.objects.filter(borrower=user, is_borrowed=False)

        if query_set.exists():
            return query_set[0].items.count()
    return 0
