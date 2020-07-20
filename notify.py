import smtplib
from os import environ
from app.models import Task


class Notify:
    """
    Notify class sends an email of all the uncompleted tasks.
    Future functionality: time/deadline functionality or importance (no mail, 1x/day, 2x/day, ...). Maybe also add some logs.

    """
    def __init__(self):
        self.tasks = Task.query.filter_by(is_done=False).all()
        self.EMAIL_USER = environ.get("EMAIL_USER")
        self.EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD")

        if self.EMAIL_USER is None or self.EMAIL_PASSWORD is None:
            print("Email user and password env variables are not set. Exiting...")
            exit()

    def _build_email(self):
        """
        Build up the email (subject and body) based on the uncompleted tasks.
        """
        subject = f"RMNDR: {len(self.tasks)} tasks"
        body = "\n".join([t.text for t in self.tasks])
        return f"Subject: {subject}\n\n{body}"

    def send_email(self):
        """
        Login to a SMTP server, build up the email and send the email.
        """
        if len(self.tasks) <= 0:
            print("There are no uncompleted tasks at this moment.")
        else:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as client:
                # login to smtp server
                client.login(self.EMAIL_USER, self.EMAIL_PASSWORD)

                email = self._build_email()

                # send email
                client.sendmail(from_addr=self.EMAIL_USER, to_addrs=self.EMAIL_USER, msg=email)


notifier = Notify()
notifier.send_email()
