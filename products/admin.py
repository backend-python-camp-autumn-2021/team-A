from django.contrib import admin
from .models import (Product, Cart, CartItems, Tag,
                    Attribute, Brand, Category, 
                    Factor, Feedback, )


admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Cart)
admin.site.register(Factor)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Feedback)


# admin.site.register(Product)
