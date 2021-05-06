from django.utils.deprecation import MiddlewareMixin
from .models import Customer, Supplier, Cart


class AddUserMiddleWare(MiddlewareMixin):
    
    def process_request(self, request):
        if not hasattr(request, 'cart'):
            if hasattr(request.user, 'user_type'):
                if request.user.user_type:
                    if request.user.user_type.name == 'customer':
                        user = Customer.objects.get(pk=request.user.pk)
                        request.user = user
                        request.cart = Cart.objects.get_or_create(customer=request.user, state="O")[0]
                    elif request.user.user_type.name == 'supplier':
                        user = Supplier.objects.get(pk=request.user.pk)
                        request.user = user
                        request.cart = None 
            else:
                if 'cart' not in request.session:
                    request.session['cart'] = []
                request.cart = request.session['cart']              

