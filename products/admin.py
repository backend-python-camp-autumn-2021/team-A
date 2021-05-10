from django.contrib import admin
from .models import (Product, Cart, CartItems, Tag,
                    Attribute, Brand, Category, 
                    Factor, Feedback, )


class HandProductModelAdmin(admin.ModelAdmin):

    exclude = ['supplier']

    def save_model(self, request, obj, form, change):
        if not form.fields.get('supplier', None):
            obj.supplier = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(supplier=request.user)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier != request.user:
            return False
        return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier != request.user:
            return False
        return True

admin.site.register(Product, HandProductModelAdmin)
admin.site.register(Attribute)
admin.site.register(Cart)
admin.site.register(Factor)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Feedback)
admin.site.register(CartItems)
