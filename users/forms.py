from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Supplier, Customer, UserTypes

class RegisterSupplierForm(UserCreationForm):
    '''
    using UserCreationForm for our model.
    '''
    class Meta(UserCreationForm.Meta):
        model = Supplier
        # You should Override fields base on your Customize model
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'company_name', 'bank_account']

        def save(self, *args, **kargs):
            '''
            assign user_type to supplier type before saving
            '''
            supplier_type = UserTypes.objects.get_or_create(name='supplier')[0]
            self.instance.user_type = supplier_type
            return super().save(*args, **kargs)


class RegisterCustomerForm(UserCreationForm):
    '''
    using UserCreationForm for our model.
    '''
    class Meta(UserCreationForm.Meta):
        model = Customer
        # You should Override fields base on your Customize model
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'gender']

    def save(self, *args, **kargs):
        '''
        assign user_type to customer type before saving
        '''
        customer_type = UserTypes.objects.get_or_create(name='customer')[0]
        self.instance.user_type = customer_type
        return super().save(*args, **kargs)


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

