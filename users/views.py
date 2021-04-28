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
from django.contrib import messages


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
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Password Changed')
            return HttpResponse('Password Changed')
        else:
            form = PasswordChangeForm(request.user)
            messages.error(request, 'Password Not Changed')
            return render(request, 'change_password.html', {'form': form})
        

class ResetPassword(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ProfileView(View):
    def get(self, request):
        user_type = request.user.user_type.name
        if user_type == 'customer':
            user = Customer.objects.get(user_ptr_id=request.user.id)
            form = CustomerProfileForm(instance=user)
        elif user_type == 'supplier':
            user = Supplier.objects.get(user_ptr_id=request.user.id)
            form = SupplierProfileForm(instance=user)
        return render(request, 'profile.html', {'form': form, 'user': user.id, 'type': user_type})
    def post(self, request):
        user_type = request.POST['type']
        user_id = request.POST['user']
        if user_type == 'customer':
            user = Customer.objects.get(id=user_id)
            form = CustomerProfileForm(request.POST, instance=user)
        elif user_type == 'supplier':
            user = Supplier.objects.get(id=user_id)
            form = SupplierProfileForm(request.POST,instance=user)
        
        if form.is_valid():
            form.save()
            return HttpResponse('Updated')
        return HttpResponse('Not Valid')



