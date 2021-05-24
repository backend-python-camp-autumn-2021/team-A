from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib import messages

from .models import Supplier, Customer,User


class CustomAuthenticationForm(AuthenticationForm):
    LOGIN_CHOICES = (
        ('C', 'Customer'),
        ('S', 'Supplier'),
        ('A', 'Admin'),
    )
    login_choices = forms.ChoiceField(choices=LOGIN_CHOICES)
    
    def clean(self):
        super().clean()
        choice = self.cleaned_data.get('login_choices')
        if choice == 'C':
            try:
                Customer.objects.get(username=self.cleaned_data.get('username'))
                self.request.session['type'] = 'customer'
            except Exception as e:
                raise ValidationError(e)
        if choice == 'S':
            try:
                Supplier.objects.get(username=self.cleaned_data.get('username'))
                self.request.session['type'] = 'supplier'
            except Exception as e:
                raise ValidationError(e)
        if choice == 'A':
            self.request.session['type'] = 'admin'
        return self.cleaned_data


class RegisterSupplierForm(UserCreationForm):
    '''
    using UserCreationForm for our model.
    '''
    class Meta(UserCreationForm.Meta):
        model = Supplier
        # You should Override fields base on your Customize model
        fields = [
            'username', 'password1', 'password2', 'first_name',
            'last_name', 'email', 'company_name', 'bank_account',
            'profile_picture']

    def save(self, *args, **kargs):
        '''
        assign user_type to supplier type before saving
        '''
        supplier =  super().save(*args, **kargs)
        supplier.is_admin = True
        group = Group.objects.get(name='Supplier-Permissions')
        supplier.groups.add(group)
        supplier.save()
        return supplier


class RegisterCustomerForm(UserCreationForm):
    '''
    using UserCreationForm for our model.
    '''
    class Meta(UserCreationForm.Meta):
        model = Customer
        # You should Override fields base on your Customize model
        fields = [
            'username', 'password1', 'password2', 'first_name',
            'last_name', 'email', 'phone', 'gender', 'profile_picture']


class SupplierProfileForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['username', 'first_name', 'last_name', 'email', 'bank_account', 'company_name']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'gender']

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=40, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=40, widget=forms.PasswordInput())

