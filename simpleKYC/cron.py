from django_cron import CronJobBase, Schedule
import os
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMessage, get_connection
import logging
from KYCUser.models import KYCUsers


logger = logging.getLogger(__name__)

class EmailUsersCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Run every days
    # RUN_EVERY_MINS = 60 * 24  # Run every days

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'simpleKYC.email_users_cron_job'  # A unique code for this cron job

    def do(self):
        users = KYCUsers.objects.filter(isVerified=False)
        for user in users:
            subject = "Verify Your Data RIGHT NOW"
            recipient_list = [user.email]
            from_email = "delivered@resend.dev"
            message = "<strong>Hey, Verify your data ASAP!</strong>"

            with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password="re_WUx1Ck6V_HmUwBDqTLwurpsgXzybjuTQy",
                use_tls=True,
                ) as connection:
                    r = EmailMessage(
                        subject=subject,
                        body=message,
                        to=recipient_list,
                        from_email=from_email,
                        connection=connection).send()
            
        logger.info("EmailUsersCronJob completed")
