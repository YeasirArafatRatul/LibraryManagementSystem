import datetime
from django.utils import timezone
from .models import Borrow, BorrowItem, Fine
from accounts.models import UserProfile, User
from payment_system.models import Payment
from diit_library.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from background_task import background

# just checking
# @background(schedule=60)
# def fine_users():
#     users_list = Borrow.objects.filter(is_returned=False)
#     for user in users_list:
#         if user.return_date == datetime.date.today()-datetime.timedelta(days=1):
#             subject = "Hello"
#             message = "Checking ... function...Boss"
#             from_email = EMAIL_HOST_USER
#             to_email = [user.email]
#             send_mail(subject=subject, message=message, from_email=from_email,
#                       recipient_list=to_email, fail_silently=False)
#             print("email sent")

#             print("Hello Ratul!")
#         else:
#             print('job done')


