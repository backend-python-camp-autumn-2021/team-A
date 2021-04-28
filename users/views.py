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
    pass


class RegisterCustomerView(CreateView):
    pass


class ChangePassword(View):
    def get(self, request):
        pass

    def post(self, request):
        pass

class ResetPassword(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class CustomerProfileView(View):
    def get(self, request):
        user = Customer.objects.filter(user_ptr_id=request.user.id)
        if user:
            form = CustomerProfileForm(instance=user[0])
        else:
            user = Supplier.objects.filter(user_ptr_id=user)
            form = SupplierProfileForm(instance=request.user)
        return render(request, 'profile.html', {'form': form})
    def post(self, request):
        pass

class SupplierProfileView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass

