from datetime import timedelta, time, datetime
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
import os
from account.models import LeaveRequest


today = timezone.now()
tomorrow = today + timedelta(1)
today_start = make_aware(datetime.combine(today, time()))
today_end = make_aware(datetime.combine(tomorrow, time()))


class Command(BaseCommand):
    help = "Send Today's Orders Report to Admins"

    def handle(self, *args, **options):
        orders = LeaveRequest.objects.filter(EmailSent=False)
        if orders:
            for order in orders:
                user = order.student.email
                order.EmailSent = True
                order.save(force_update=True)
                email = EmailMessage(
                    subject="Regarding your Leave Request Proposal",
                    body=f"""
                        Hello! Your Leave Requested has been approved!

                        Details of your Leave:
                        
                        Start Date: {order.start_date}
                        Return Date: {order.end_date}
                        Address During Leave: {order.Address}
                        Reason for Leave : {order.ReasonForLeave} 


                        Thank you!
                         
                    """,
                    from_email="pp7405124@gmail.com",
                    to=[str(user), "bh1admin@iiitm.ac.in"],
                )
                email.send()
