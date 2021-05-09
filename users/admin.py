from django.contrib import admin
from .models import Supplier, Address, Customer, UserTypes
from .forms import RegisterCustomerForm, RegisterSupplierForm
from users.models import UserTypes


class CustomerAdmin(admin.ModelAdmin):
    form = RegisterCustomerForm


class SupplierAdmin(admin.ModelAdmin):
    form = RegisterSupplierForm

    def save_model(self, request, obj, form, change):
        supplier_type = UserTypes.objects.get_or_create(name='supplier')[0]
        form.instance.user_type = supplier_type
        return super().save_model(request, obj, form, change)


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address)
admin.site.register(UserTypes)

