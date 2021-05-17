import os
from pathlib import Path
import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Supplier, Customer
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.utils.functional import SimpleLazyObject

from dotenv import load_dotenv, find_dotenv
import requests

from .forms import CreateCommentForm
from .models import Category, Tag, Brand, Product, CartItems, Cart, Feedback

env_file = Path(find_dotenv(usecwd=True))
load_dotenv(verbose=True, dotenv_path=env_file)


class Gruoping:
    '''
    you can inherit this class if you want to have
    filter and search functionality in your view.
    '''   
    def get_query_set(self, query_set):
        '''
        filter queryset base on given query.
        filter is base on this keywords --> brand, cat, tag
        '''
                
        if 'cat' in self.request.GET:
            query_set = query_set.filter(
                category__pk=self.request.GET.get('cat')
                )
        elif 'brand' in self.request.GET:
            query_set = query_set.filter(brand__pk=self.request.GET.get('brand'))
        elif 'tag' in self.request.GET:
            query_set = query_set.filter(tag__pk=self.request.GET.get('tag'))
        return query_set
 

class ProductListView(ListView, Gruoping):
    paginate_by = 9
    model = Product
    template_name = 'product-list.html'

    def get_queryset(self):
        '''
        add filter and searches base on q, tag, brand, category.
        and sorting base on price, name, date fields
        '''
        self.ordering = self.request.GET.get('sort', None)
        queryset = super().get_queryset()
        queryset = super().get_query_set(queryset)  # add gruping query set
        # search q in name, description fields
        if 'q' in self.request.GET:
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET.get('q'))|
                Q(description__icontains=self.request.GET.get('q'))
                )
        return queryset

    
class CartItemView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            products = Product.objects.all()
            items = []
            sub_price = 0
            for item in request.cart: # [[pk, qty], ...]
                # item --> [pk, qty]
                product = products.get(pk=item[0])
                quantity = item[1]
                item_total_price = product.price * int(quantity)
                sub_price += item_total_price
                items.append((product, quantity, item_total_price))
            context = {
                'items': items,
                'sub_total':sub_price
                }
        elif request.user.user_type.name == 'customer':
            items = []
            for item in request.cart.cartitems.all():
                items.append((item.product, item.quantity, item.get_price))
            context = {
                'items': items,
                'sub_total': request.cart.get_total_price
            }
        else:
            messages.warning(request,
                'Suppliers and admins do not have cart!!!')
            context = {}
        return render(request, 'cart.html', context)
        

class AddToCart(View):
    '''add product to cart items for requested user '''
    def post(self,request, pk):
        '''
        there is three condition:
        1. anonymouse users can add to cart
        2. customers can add to cart
        3. quantity must be higher than 0
        '''
        # check for quantity
        if int(request.POST['quantity']) <= 0:
            messages.warning(request, 'You must select at least one product')
            return redirect(reverse_lazy('shop:home'))

        if not request.user.is_authenticated:
            # check if user is anonymous
            self.add_to_cart_anonymous(request, pk)
        elif request.user.user_type.name == 'customer':
            # check if user is customer 
            self.add_to_cart_users(request, pk)
        else:
            # if user is not one of them
            messages.warning(request,
                'Suppliers and admins can not buy any shit!!!')

        return redirect(reverse_lazy('shop:home'))

    def add_to_cart_users(self, request, pk):
        '''
        if request user is authenticated, the product will be added
         to the cartitems in his/her account
        '''
        cartitem = CartItems.objects.filter(
            cart=Cart.objects.get_or_create(customer=request.user, state='O')[0],
            product=Product.objects.get(pk=pk)
            )
        if cartitem:
            # if there is an cartitem for this product
            # only quantity will be upgrade
            cartitem[0].quantity += int(request.POST['quantity'])
            cartitem[0].save()
        else:
            # if there is no cartitem for this product
            # create a new one
            CartItems.objects.create(
            cart=Cart.objects.get_or_create(customer=request.user, state='O')[0],
            product=Product.objects.get(pk=pk),
            quantity=request.POST['quantity'],
            )
    
    def add_to_cart_anonymous(self, request, pk):
        """
        if user is not authenticated, the product will be add to request's session
        """
        if 'cart' not in request.session:
            request.session['cart'] = []
        qty = request.POST['quantity']
        for i in request.session['cart']: # [[pk, qty], ..]
            # if there is a item with that product
            # only upgrade the quantity
            if i[0] == pk: # i --> [pk, qty]
                i[1] += int(qty)
                request.session.save()
                return True
        # if there wasn't any item for that product
        # create a new one
        request.session['cart'] += [(pk, int(qty))]
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        '''
        add comment form to context
        if user is customer.
        '''
        context = super().get_context_data(**kwargs)
        try: # If the user is anonymous, an error occurs in line 216
            if self.request.user.user_type.name == 'customer':
                feed = Feedback.objects.filter(
                    customer=self.request.user,
                    product=super().get_object())
                # check if user has a cooment already or not.
                # if yes return the update comment form
                # if no return a new comment form
                if feed.exists():
                    form = CreateCommentForm(instance=feed.get())
                else:
                    form = CreateCommentForm()
                result = {
                    'form': form
                }
                context.update(result)
        except:
            pass
        return context


class CreateCommentView(View):

    def post(self, request):
        product = Product.objects.get(pk=request.POST['product'])
        feed = Feedback.objects.filter(
            customer=request.user,
            product=product)
        # check if user has a cooment already or not.
        # if yes update the comment
        # if no create a new comment
        if feed.exists(): 
            form = CreateCommentForm(request.POST, instance=feed.get())
        else:
            form = CreateCommentForm(request.POST)
        
        if form.is_valid():
            form.instance.customer = request.user
            form.instance.product = product
            form.save()   
            return redirect(request.META.get('HTTP_REFERER'))
        messages.warning(request, "Comment was'nt valid") 
        return redirect(request.META.get('HTTP_REFERER'))

def plus_cart(request, pk):
    if request.user.is_authenticated:
        cartitem = CartItems.objects.get(product__pk=pk)
        cartitem.quantity += 1
        cartitem.save()
    else:
        for i in request.session['cart']: # [[pk, qty], ...]
            if i[0] == pk: # i --> [pk, qty]
                i[1] += 1
                request.session.save()
                break
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse_lazy('shop:cart'))

def minus_cart(request, pk):
    if request.user.is_authenticated:
        cartitem = CartItems.objects.get(product__pk=pk)
        cartitem.quantity -= 1
        if cartitem.quantity <= 0:
            messages.warning(request, 'you can not go under zero')
        else:
            cartitem.save()
    else:
        for i in request.session['cart']: # [[pk, qty], ...]
            if i[0] == pk: # i --> [pk, qty]
                i[1] -= 1
                if i[1] <= 0:
                    messages.warning(request, 'you can not go under zero')
                    break
                request.session.save()
                break
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse_lazy('shop:cart'))

def remove_from_cart(request, pk):
    if request.user.is_authenticated:
        cartitem = CartItems.objects.get(product__pk=pk)
        if request.user == cartitem.cart.customer: # chech for more security
            cartitem.delete()
    else:  # for anonymous users
        for i in request.session['cart']: # [[pk, qty], ...]
            if i[0] == pk: # i --> [pk, qty]
                request.session['cart'].remove(i)
                request.session.save()
                break
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse_lazy('shop:cart'))

def send_sms(request):
    api = kavenegar.KavenegarAPI(os.environ.get('KAVENEGAR_APIKEY'))
    params = { 'sender' : '1000596446', 'receptor': '09214661058', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
    response = api.sms_send(params)
    return redirect(reverse_lazy('shop:home'))


class CheckOutView(View):
    def get(self, request):
        return render(request, 'checkout.html')

    def post(self, request):
        payload = {
            'order_id': 1010,
            'amount': 10000,
            'name': f'{request.POST.get("name")} {request.POST.get("lastname")}',
            'phone': '02193123',
            'mail': "email@mmm.com",
            'desc': request.POST.get('description'),
            'callback': str(reverse_lazy('shop:checkout_callback')),
        }
        headers = {
            'X-SANDBOX': '1',
            'X-API-KEY': '07b2d66e-3235-4551-ba68-7e4fafacfcab',
            'Content-Type': 'application/json'
        }
        url = 'https://api.idpay.ir/v1.1/payment'
        print(type(payload))
        # json.dumps(payload)
        print(requests.post(url=url, data=json.dumps(payload), headers=headers))
        print(type(requests.post(url=url, data=json.dumps(payload), headers=headers)))

        return requests.post(url=url, data=json.dumps(payload), headers=headers)

class CheckOutCallBackView(View):
    def post(self, request):
        print(request.POST)
