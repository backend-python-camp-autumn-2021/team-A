from django.contrib import admin
from .models import Supplier, Address, Customer, User
from .forms import RegisterCustomerForm, RegisterSupplierForm


class CustomerAdmin(admin.ModelAdmin):
    form = RegisterCustomerForm


class SupplierAdmin(admin.ModelAdmin):
    form = RegisterSupplierForm


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address)
admin.site.register(User)


