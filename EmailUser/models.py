from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from imagekit.models import ProcessedImageField
from imagekit.processors import Transpose

from time import mktime

from datetime import datetime, timedelta

import strecklista.models

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = email.lower()

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    nickname = models.CharField(max_length=50,blank=True)

    avatar = ProcessedImageField(
        upload_to='protected/avatars/',
        processors=[Transpose()],
        options={'quality': 60},
        null=True,
        blank=True,
    )

    balance = models.DecimalField(decimal_places=2, max_digits=20, default=0)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    phone_number = models.CharField(validators=[phone_regex],null=True, blank=True, max_length=20) # validators should be a list

    group = models.ForeignKey('strecklista.Group', on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    active_singer = models.BooleanField(default=True)

    weight = models.DecimalField(default=70, decimal_places=2, max_digits=10)

    y_chromosome = models.NullBooleanField()

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name"]

    def display_name(self):
        if self.nickname:
            return self.nickname
        else:
            return "%s %s" %(self.first_name, self.last_name)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def blood_alcohol(self):
        """Returns the blood alcohol content in permille."""
        time_threshold = datetime.now() - timedelta(days=7)
        transactions = strecklista.models.Transaction.objects.filter(user = self.id, returned=False, admintransaction=False, timestamp__gte=time_threshold).all().order_by('timestamp')

        standard_drink = 0.012  #1 standard glass (12g pure ethanol) in kg
        blood_alcohol = 0.0
        burn_constant = 0.000001667 #how many kg of alcohol is consumed each second

        body_weight_constant = 0.65 #how much of the body weight is able to absorb alcohol
        if self.y_chromosome == False:
          body_weight_constant = 0.55  # female
        if self.y_chromosome == True:
          body_weight_constant = 0.7 #male

        last_drink = 0 #the time of the last drink

        for transaction in transactions:
            #update the timestamps
            transaction_time = mktime(transaction.timestamp.timetuple())
            timediff = transaction_time-last_drink
            last_drink = transaction_time

            #remove alcohol from previous round
            blood_alcohol = blood_alcohol - burn_constant*timediff

            #reset blood alcohol level to 0 to prevent negative results
            if blood_alcohol < 0:
                blood_alcohol = 0

            #add the alcohol from this round
            blood_alcohol = blood_alcohol + standard_drink

        #remove the alcohol burned since the last drink
        now = mktime(datetime.utcnow().timetuple())
        timediff = now - last_drink
        blood_alcohol = blood_alcohol-timediff*burn_constant
        #Set as 0 if negative
        if(blood_alcohol < 0):
            blood_alcohol = 0

        promille = round((blood_alcohol/(float(self.weight)*body_weight_constant))*1000, 3)

        return promille
