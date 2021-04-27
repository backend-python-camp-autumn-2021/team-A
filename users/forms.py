from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Supplier, Customer

class RegisterSupplierForm(UserCreationForm):
    '''
    using UserCreationForm for our model.
    '''
    class Meta(UserCreationForm.Meta):
        model = Supplier
        # You should Override fields base on your Customize model
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'company_name', 'bank_account']


class RegisterCustomerForm(UserCreationForm):
    '''
    using UserCreationForm for our model.
    '''
    class Meta(UserCreationForm.Meta):
        model = Customer
        # You should Override fields base on your Customize model
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'gender']


class SupplierProfileForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'gender']
