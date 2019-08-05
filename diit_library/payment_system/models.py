from django.db import models
from accounts.models import User
from all_books.models import Borrow
from django.db.models.signals import pre_save
from diit_library.utils import unique_slug_generator
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    bKash_ac = models.IntegerField(max_length=11)
    transaction_id = models.CharField(max_length=15)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def title(self):
        return('transaction')


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# Connecting Payment Model with the 'unique_slug_generator' function
pre_save.connect(slug_generator, sender=Payment)
