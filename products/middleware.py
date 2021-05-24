from django.utils.deprecation import MiddlewareMixin
from .models import Customer, Supplier, Cart, CartItems, Product
from django.shortcuts import get_object_or_404


class AddUserMiddleWare(MiddlewareMixin):
    '''
    chaneg request.user to instance of customer or supplier
    base on request.session that has been set in login form
    '''
    def process_request(self, request):
        user_type = request.session.get('type', None)
        if user_type == 'customer':
            pass
            # request.user = Customer.objects.get(pk=request.user.pk)
        elif user_type == 'supplier':
            request.user = Supplier.objects.get(pk=request.user.pk)


class AddCartMiddleWare(MiddlewareMixin):
    '''
    add request.cart for customer andanonymouse users
    '''
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.is_customer:
                # if user is customer, add object of Cart model to request.cart
                request.cart = Cart.objects.get_or_create(customer=request.user, state="O")[0]
                if request.session['cart']:
                    # if user had some items in request.session['cart'],
                    # transfer them to cart table of the logined user
                    for item in request.session['cart']:
                        product = Product.objects.get(pk=item[0])
                        cartitem =  CartItems.objects.get_or_create(
                            cart=request.cart,
                            product=product
                            )[0]
                        cartitem.quantity += item[1]
                        cartitem.save()
                request.session['cart'] = [] # empty request.session['cart']
            elif request.user.is_supplier:
                request.cart = None
        else:
            # if user is anonymouse, add cart to request.session['cart']
            if 'cart' not in request.session:
                request.session['cart'] = []
            request.cart = request.session['cart']
        print(hasattr(request, 'cart'))
