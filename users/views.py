from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Customer, Supplier
from django.views.generic import CreateView, UpdateView, FormView
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


class ChangePassword(FormView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('shop:home')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        ### add user request to form because it's needed
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        ### default form_valid() won't call form.save()
        form.save()
        return HttpResponseRedirect(self.get_success_url())
        

class ResetPassword(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ProfileView(View):
    def get(self, request):
        user_type = request.user.user_type.name # get user_type
        
        if user_type == 'customer':
            ### query for getting customer user
            user = Customer.objects.get(user_ptr_id=request.user.id)
            ### generate customer form with giving instance user
            form = CustomerProfileForm(instance=user)
        elif user_type == 'supplier':
            user = Supplier.objects.get(user_ptr_id=request.user.id)
            form = SupplierProfileForm(instance=user)
        
        ### send user.id and user_type to prevent checking again
        context = {
            'form': form,
            'user': user.id, 
            'type': user_type
            }

        return render(request, 'profile.html', context)
    
    def post(self, request):
        if request.POST['type'] == 'customer':
            # get user with the user.id came from get
            user = Customer.objects.get(id=request.POST['user']) 
            # generating customer form for the request.user with data given 
            form = CustomerProfileForm(request.POST, instance=user)
        elif request.POST['type'] == 'supplier':
            user = Supplier.objects.get(id=request.POST['user'])
            form = SupplierProfileForm(request.POST,instance=user)
        
        if form.is_valid():
            form.save()
            return HttpResponse('Updated')
            
        return HttpResponse('Not Valid')



