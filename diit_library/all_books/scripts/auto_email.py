from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail  # I think this is right.
from all_books.models import Borrow
from diit_library.settings import EMAIL_HOST_USER


def run():
    for borrower in Borrow.objects.filter(return_date=date.today() - relativedelta(days=1)):

        for objects in borrower.registered_player_set():
            def fine(request, commit=True):
                instance = Borrow.object.filter(id=id)
                to_email = ""
                amount = ""
                message = ""
                subject = 'You are Fined'
                from_email = EMAIL_HOST_USER
                formatted_message = f'{message + "Payable amount:" + str(amount)}'
                reciever = [instance.to_email.email]
                send_mail(subject=subject, message=formatted_message, from_email=from_email,
                          recipient_list=reciever, fail_silently=False)
                instance.save()
