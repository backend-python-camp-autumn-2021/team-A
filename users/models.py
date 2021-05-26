from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
    )
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token



class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username , email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser=True
        user.is_admin = True
        user.save(using=self._db)
        return user
        


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles', default='default_pic.png')

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    # This Fields and Properties are all required
    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_supplier(self):
        return False

    @property
    def is_customer(self):
        return False

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        return self.email


@receiver(signal=post_save, sender=User)
def add_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Supplier(User):
    bank_account = models.CharField('bank account', validators=[RegexValidator(
        regex='^[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}$',
        message='Length has to be more than 8 character', code='nomatch')], max_length=20)
    company_name = models.CharField(max_length=500)

    def __str__(self):
        return f'Supplier {self.username}'
    
    @property
    def is_supplier(self):
        return True


class Customer(User):
    phone = models.CharField(max_length=12,
        validators=[RegexValidator(regex='[0-9]{10}')])
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __str__(self):
        return f'Customer {self.username}'
    
    @property
    def is_customer(self):
        return True


class Address(models.Model):
    '''
    abstractin address field becouse Customers can have more than one address
    '''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    adrs = models.CharField(max_length=100)

    @property
    def full_address(self):
        '''
        return full address
        '''
        full = self.country + self.city + self.street + self.rest
        return full
