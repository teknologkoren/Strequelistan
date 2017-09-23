from django.core.validators import RegexValidator
from django.db import models
import decimal
from django.core.mail import send_mail

from EmailUser.models import MyUser

# Create your models here.

class RegisterRequest(models.Model):
    email = models.EmailField(
      verbose_name='email address',
      max_length=255,
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    message = models.TextField(max_length=500, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
       return "Register_request: {} {}".format(self.first_name, self.last_name)
    def __str__(self):
       return "Register_request: {} {}".format(self.first_name, self.last_name)


    def registerUser(self):
      user = MyUser()
      user.first_name = self.first_name
      user.last_name = self.last_name
      user.email = self.email

      user.group = Group.objects.all().order_by('sortingWeight').first()

      return user.save()

class Group(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=500, default="", blank=True)
    sortingWeight = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    def __unicode__(self):
       return 'Group: ' + self.name
    def __str__(self):
        return 'Group: {}'.format(self.name)


class ProductCategory(models.Model):
    class Meta:
        verbose_name_plural = "Product categories"

    name = models.TextField(max_length=50)
    description = models.TextField(max_length=500, default="", blank=True)
    sortingWeight = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    def __unicode__(self):
       return 'Product: ' + self.name
    def __str__(self):
        return 'Product: {}'.format(self.name)

class PriceLimit(models.Model):
    class Meta:
        ordering = ['-limit']
    name = models.TextField(max_length=50, default="Unnamed price limit")
    limit = models.DecimalField(max_digits=20, decimal_places=2)
    multiplier = models.DecimalField(max_digits=20, decimal_places=4, default=1)
    def __unicode__(self):
       return 'Price limit: ' + self.name
    def __str__(self):
        return 'Price limit: {}'.format(self.name)


class PriceGroup(models.Model):
    name = models.TextField(max_length=50)
    sortingWeight = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    defaultPrice = models.DecimalField(max_digits=10, decimal_places=2)

    priceLimits = models.ManyToManyField(PriceLimit)

    def calculatePrice(self, balance):
        multiplier = 1.0
        limits = reversed(sorted(self.priceLimits.all(), key=lambda priceLimit: priceLimit.limit))
        for i in limits:

            if (balance > i.limit):
                break
            elif balance < i.limit:
                multiplier = i.multiplier
        calculatedPrice = self.defaultPrice * decimal.Decimal(multiplier)
        return calculatedPrice

    def __unicode__(self):
       return 'Group: ' + self.name
    def __str__(self):
        return 'Group: {}'.format(self.name)



class Product(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=500, default="", blank=True)
    sortingWeight = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    priceGroup = models.ForeignKey(PriceGroup, on_delete=models.CASCADE)
    productCategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):
       return 'Product: ' + self.name
    def __str__(self):
        return 'Product: {}'.format(self.name)


class Quote(models.Model):
    text = models.TextField(max_length=4098)
    who = models.TextField(max_length=250)
    timestamp = models.DateField(auto_now_add=True, blank=True)
    submittedBy = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    def __str__(self):
        return 'Quote: {}'.format(self.text)
    def __unicode__(self):
       return 'Quote: ' + self.text

class Transaction(models.Model):
    class Meta:
        ordering = ('-timestamp',)

    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    returned = models.BooleanField(default=False)
    admintransaction = models.BooleanField(default=False)
    def __str__(self):
        return 'Transaction: {} {} : {}kr : {}'.format(self.user.first_name, self.user.last_name,
                                                    self.amount, self.timestamp)
    def __unicode__(self):
        return 'Transaction: {}  {} : {}kr: {}'.format(self.user.first_name, self.user.last_name,
                                                    self.amount, self.timestamp)
    def ret(self):
        if self.returned is False:

            self.user.balance += self.amount
            self.user.save()
            self.returned = True
            self.save()


class Suggestion(models.Model):

    class Meta:
        ordering = ('-timestamp',)

    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.TextField(blank=False, max_length=250)
    description = models.TextField(blank=True, max_length=500)
    price = models.TextField(blank=True, max_length=50)
    link = models.URLField(blank=True)


    def __str__(self):
      return 'Suggestion: {}'.format(self.name)

    def __unicode__(self):
      return 'Suggestion: {}'.format(self.name)

class SuggestionVote(models.Model):
    class Meta:
        ordering = ('-timestamp',)

    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    Suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    approve = models.BooleanField()