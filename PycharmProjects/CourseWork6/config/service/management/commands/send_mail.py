from datetime import datetime, timedelta
import pytz
from django.core.mail import send_mail
from django.core.management import BaseCommand
from config import settings
from service.models import Newsletter, Message, Logs
from django.db.models import F
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler


class Command(BaseCommand):
    help = 'Runs APScheduler'

    @staticmethod
    def send_mailing():
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        mailings = Newsletter.objects.filter(first_newsletter__lte=current_datetime).filter(
            status__in=[Newsletter.Status.CREATED])

        for newsletter in mailings:
            status = False
            response = 'Нет ответа'
            try:
                message = newsletter.message
                send_mail(
                    subject=message.title,
                    message=message.text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in newsletter.clients.all()]
                )
                if newsletter.periodicity == Newsletter.Periodicity.DAILY and current_datetime.day >= 1:
                    newsletter.first_newsletter = F('first_newsletter') + timedelta(days=1)
                    newsletter.status = Newsletter.Status.LAUNCHED
                elif newsletter.periodicity == Newsletter.Periodicity.WEEKLY and current_datetime.day >= 7:
                    newsletter.first_newsletter = F('first_newsletter') + timedelta(days=7)
                    newsletter.status = Newsletter.Status.LAUNCHED
                elif newsletter.periodicity == Newsletter.Periodicity.MONTHLY and current_datetime.day >= 30:
                    newsletter.first_newsletter = F('first_newsletter') + timedelta(days=30)
                    newsletter.status = Newsletter.Status.LAUNCHED

                newsletter.save()
                status = True
                response = 'Успешно'

            except smtplib.SMTPResponseException as e:
                status = False
                response = str(e)

            finally:
                Logs.objects.create(
                    newsletter=newsletter,
                    attempt=status,
                    attempt_time=current_datetime,
                    response=response,
                )

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.send_mailing, 'interval', seconds=10)
        scheduler.start()

