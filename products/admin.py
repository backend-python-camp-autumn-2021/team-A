from django.contrib import admin
from .models import (Product, Cart, CartItems, Tag,
                    Attribute, Brand, Category, 
                    Transaction, Feedback, )


admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Cart)
admin.site.register(Transaction)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Tag)

# admin.site.register(Product)
