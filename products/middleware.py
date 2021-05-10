from django.utils.deprecation import MiddlewareMixin
from .models import Customer, Supplier, Cart, CartItems, Product
from django.shortcuts import get_object_or_404


class AddUserMiddleWare(MiddlewareMixin):
    
    def process_request(self, request):
        if hasattr(request.user, 'user_type'):
            if request.user.user_type.name == 'customer':
                user = Customer.objects.get(pk=request.user.pk)
                request.user = user
                request.cart = Cart.objects.get_or_create(customer=request.user, state="O")[0]
                if request.session['cart']:
                    for item in request.session['cart']:
                        product = Product.objects.get(pk=item[0])
                        cartitem =  CartItems.objects.get_or_create(
                            cart=request.cart,
                            product=product
                            )[0]
                        cartitem.quantity += item[1]
                        cartitem.save()
                request.session['cart'] = []
            
            elif request.user.user_type.name == 'supplier':
                user = Supplier.objects.get(pk=request.user.pk)
                request.user = user
                request.cart = None 
        else:
            if 'cart' not in request.session:
                request.session['cart'] = []
            request.cart = request.session['cart']   
               

