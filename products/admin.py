from django.contrib import admin
from .models import (Product, Cart, CartItems, Tag,
                    Attribute, Brand, Category, ProductList, 
                    Transaction, Feedback)


admin.site.register(Product)
admin.site.register(ProductList)
admin.site.register(Attribute)
admin.site.register(Cart)
admin.site.register(Transaction)
# admin.site.register(Product)
