import os
import secrets
from pathlib import Path

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    )
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import send_mail
from django.conf import settings

import redis
from dotenv import load_dotenv, find_dotenv

from .forms import (RegisterSupplierForm, RegisterCustomerForm, PasswordResetForm,
    CustomerProfileForm, SupplierProfileForm,
    SupplierProfileForm, CustomerProfileForm,
    SetPasswordForm, CustomAuthenticationForm)
from .models import User
from .models import Customer, Supplier

env_file = Path(find_dotenv(usecwd=True))
load_dotenv(verbose=True, dotenv_path=env_file)


class AuthenticationView(LoginView):
    template_name = 'authentication/login.html'
    form_class = CustomAuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('shop:home')


def logout_page(request):
    logout(request)
    return redirect(reverse_lazy('user:login'))


class RegisterSupplierView(CreateView):
    form_class = RegisterSupplierForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('user:login')


class RegisterCustomerView(CreateView):
    form_class = RegisterCustomerForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('user:login')


class ChangePassword(PasswordChangeView):
    template_name = 'authentication/change-password.html'
    success_url = reverse_lazy('shop:home')
    form_class = PasswordChangeForm


class UpdateSupplierView(UpdateView):
    model = Supplier
    template_name = 'authentication/update-profile.html'
    form_class = SupplierProfileForm
    success_url = reverse_lazy('shop:home')


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = 'authentication/update-profile.html'
    form_class = CustomerProfileForm
    success_url = reverse_lazy('shop:home')


class PasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'authentication/password-reset-form.html', {'form': form})
    
    def post(self,request):
        email = request.POST.get('email')
        r = redis.Redis(host='localhost', port=6379, db=0)
        token = secrets.token_urlsafe(16)
        r.set(token, email, ex=60*5)
        if settings.DEBUG:
            link = f'http://localhost:8000{reverse_lazy("user:set_password", kwargs={"token":token})}/',
        else:
            link = f'http://{os.environ.get("HOST_NAME")}:8000{reverse_lazy("user:set_password", kwargs={"token":token})}/',
        
        send_mail(
            'Reset Password',
            settings.EMAIL_HOST_USER,
            link
            [email],
            fail_silently=False,
        )
        r.close()
        return render(request, 'authentication/password-reset-done.html')


class PasswordResetVerifyView(View):
    def get(self, request, token):
        r = redis.Redis(host='localhost', port=6379, db=0)
        mail = r.get(token)
        form = SetPasswordForm()

        context = {
            'form': form,
            'mail': mail
        }
        return render(request, 'authentication/password-reset-verify.html', context)
        
    def post(self, request, token):
        pas1 = request.POST.get('password1')
        pas2 = request.POST.get('password2')
        mail = request.POST.get('mail')
        user = User.objects.get(email = mail)
        if pas1 == pas2:
            user.set_password(pas1)
            return redirect(reverse_lazy('shop:home'))
        return redirect(reverse_lazy('user:set_password'))
