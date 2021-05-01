from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.views import View
from .models import Customer, Supplier
from django.views.generic import CreateView, UpdateView
from .forms import RegisterSupplierForm, RegisterCustomerForm, CustomerProfileForm, SupplierProfileForm
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    PasswordResetForm )
from django.urls import reverse_lazy, reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .models import User,Customer, Supplier

class AuthenticationView(View):
    def get(self, request):
        form = AuthenticationForm
        return render(request, 'login.html', context={'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('shop:home'))
        return HttpResponse('Not Authenticated')


def logout_page(request):
    logout(request)
    return HttpResponse('logout successfully')


class RegisterSupplierView(CreateView):
    model = Supplier
    form_class = RegisterSupplierForm
    template_name = 'register_suplier.html'
    success_url = reverse_lazy('users:login')


class RegisterCustomerView(CreateView):
    model = Customer
    form_class = RegisterCustomerView
    template_name = 'register_customer.html'
    success_url = reverse_lazy('users:login')


def change_password(request):
    '''
    In case the user wanted to change their password.
    '''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('shop:home'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

class ResetPassword(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class CustomerProfileView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass

class SupplierProfileView(View):
        def get(self, request):
            pass
        def post(self, request):
            pass

