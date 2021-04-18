from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



class Address(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    adrs = models.CharField(max_length=100)

    @property
    def full_address(self):
        full = self.country + self.city + self.street + self.rest
        return full

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(validators=[RegexValidator('[0-9]{10}')])
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_enabled = models.BooleanField()
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        self.user= self.user.lower()
        return super().save(*args, **kwargs)


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_account = models.CharField('bank account', validators=[RegexValidator(
        regex='^[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}$', message='Length has to be more than 8 character', code='nomatch')], max_length=255)
    company_name = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.user.username= self.user.username.lower()
        return super().save(*args, **kwargs)



