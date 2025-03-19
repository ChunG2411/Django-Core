from django.core.mail import send_mail
from django.conf import settings

from backend.celery import app


@app.task
def send_email_task(email, code_char):
    send_mail(
        "Verify Code",
        "Please enter this code to verify page: {}".format(code_char),
        settings.EMAIL_HOST_USER,
        [f'{email}']
    )
    print(1)