from django.db import models
from EmailUser.models import MyUser
import string
import random
from django.core.mail import send_mail
# Create your models here.

class PasswordResetEmail(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def random_string(self, size=20, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


    def email_user(self):
        send_mail(
            "Password reset",
            "enter %s in the form at streque.se/reset_password or use this link: streque.se/reset_password?key=%s" %(self.key, self.key),
            "strecklistan@gmail.com",
            [self.user.email],
            fail_silently=False,
        )

    def email_new_user(self):
        send_mail(
            "Password reset",
            "Welcome to Strequelistan! To activate your account, enter %s in the form at streque.se/reset_password or use this link: streque.se/reset_password?key=%s" % (
            self.key, self.key),
            "strecklistan@gmail.com",
            [self.user.email],
            fail_silently=False,
        )

    def reset_password(self, password):
        self.user.set_password(password)
        self.user.save()
        self.used = True
        self.save()
