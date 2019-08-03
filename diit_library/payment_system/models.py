from django.db import models
from accounts.models import User
from all_books.models import Borrow

# Create your models here.


class Payment(models.Model):
    fine_code = models.OneToOneField(Borrow, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    bKash_ac = models.IntegerField()
    transaction_id = models.IntegerField()

    def __str__(self):
        return self.fine_code.id
