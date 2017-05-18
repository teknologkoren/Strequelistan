from django.core.management.base import BaseCommand, CommandError
from EmailUser.models import MyUser
from django.core.mail import EmailMessage

class Command(BaseCommand):
    help = 'Emails all users with less than 0 kr on their account'



    def handle(self, *args, **options):

        userlist = MyUser.objects.all();

        for user in userlist:
            if user.balance < 0:
                email_subject = "Hälsning från QM"
                email_body = """
Hej kära törstiga du!

Ditt QM-saldo är för nuvarande: %d kr

Om du tycker att det är lågt kan det vara dags att fylla på, om du tycker att det är högt får vi ta ett snack.

Om du vill åtgärda underskottet, sätt in pengar på PG 20 74-3 och markera med Streck/Saldo och ditt namn

Vänliga hälsningar
QM""" %(user.balance)

                EmailMessage(email_subject, email_body, "strecklistan@gmail.com", [user.email]).send()
                self.stdout.write(self.style.SUCCESS('Sent mail to "%s"' % user.get_full_name()))