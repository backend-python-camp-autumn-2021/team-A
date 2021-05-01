from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Customer, Supplier, UserTypes
from django.views.generic import CreateView, UpdateView
from .forms import (RegisterSupplierForm, RegisterCustomerForm, PasswordResetForm,
    CustomerProfileForm, SupplierProfileForm,
    SupplierProfileForm, CustomerProfileForm,
    SetPasswordForm)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    )
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import send_mail
from django.conf import settings

import redis
from .models import User
import secrets


class AuthenticationView(LoginView):
    template_name = 'login.html'
    

def logout_page(request):
    print(request.user.user_type)
    logout(request)
    return HttpResponse('logout successfully')


class RegisterSupplierView(CreateView):
    model = Supplier
    form_class = RegisterSupplierForm
        print('i am savin this mother fucker')
        customer_type = UserTypes.objects.get(name='customer')
        form.instance.user_type = customer_type
        return super().form_valid(form)


class RegisterCustomerView(CreateView):
    model = Customer
    template_name = 'signup.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        supplier_type = UserTypes.objects.get(name='supplier')
        form.instance.user_type = supplier_type
        return super().form_valid(form)


class ChangePassword(PasswordChangeView):
    template_name = 'change-password.html'
    success_url = reverse_lazy('shop:home')
    form_class = PasswordChangeForm


class UpdateSupplierView(UpdateView):
    model = Supplier
    template_name = 'update-profile.html'
    form_class = SupplierProfileForm
    success_url = reverse_lazy('shop:home')


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = 'update-profile.html'
    form_class = CustomerProfileForm
    success_url = reverse_lazy('shop:home')


class PasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'password-reset-form.html', {'form': form})
    
    def post(self,request):
        email = request.POST.get('email')
        r = redis.Redis(host='localhost', port=6379, db=0)
        token = secrets.token_urlsafe(16)
        r.set(token, email, ex=120)
        send_mail(
            'Reset Password',
            f'http://localhost:8000/reset-password/{r.get(email)}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        r.close()
        return render(request, 'password-reset-done.html')


class PasswordResetVerifyView(View):
    def get(self, request, token):
        r = redis.Redis(host='localhost', port=6379, db=0)
        mail = r.get(token)
        form = SetPasswordForm()

        context = {
            'form': form,
            'mail': mail
        }
        return render(request, 'password-reset-verify.html', context)
        

    def post(self, request, token):
        pas1 = request.POST.get('password1')
        pas2 = request.POST.get('password2')
        mail = request.POST.get('mail')
        user = User.objects.get(email = mail)
        if pas1 == pas2:
            user.set_password(pas1)
            return redirect(reverse_lazy('shop:home'))
        return redirect(reverse_lazy('user:set_password'))



