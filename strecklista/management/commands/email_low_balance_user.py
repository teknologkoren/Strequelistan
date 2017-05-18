from django.core.management.base import BaseCommand, CommandError
from EmailUser.models import MyUser

from django.core.mail import EmailMessage

class Command(BaseCommand):
    help = 'Send a email to specified user with their current balance'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):

        uid = options['user_id'][0]

        self.stdout.write(self.style.SUCCESS('will send a email to user with id: %i' % (uid)))

        user = MyUser.objects.filter(id=uid).first();

        if(user):

            email_body = """
Hej kära törstiga du!

Ditt QM-saldo är för nuvarande: %d kr, det är kanske dags att fylla på?

Om du vill öka ditt saldo kan du sätta in pengar på PG 20 74-3 och markera med Streck/Saldo och ditt namn

Vänliga hälsningar
QM""" %(user.balance)
            email_subject = "Hälsning från QM"

            EmailMessage(email_subject, email_body, "strecklistan@gmail.com", [user.email]).send()
            self.stdout.write(self.style.SUCCESS('Sent mail to "%s"' % user.get_full_name()))
        else:
            raise CommandError('User with id: "%i" does not exist' % uid)


