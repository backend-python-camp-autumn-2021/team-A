from django.contrib import admin
from .models import Supplier, Address, Customer

admin.site.register(Supplier)
admin.site.register(Address)
admin.site.register(Customer)
