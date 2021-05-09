from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Supplier, Customer
from .models import Category, Tag, Brand, Product, CartItems, Cart, Feedback
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import CreateCommentForm
from django.utils.functional import SimpleLazyObject


class CustomRequiredMixin(View):
    register_url = None
    login_url = None
    redirect_url = None
    model = None
    boolean = False

    def dispatch(self, request, *args, **kwargs):
        if self.boolean:
            return super().dispatch(request, *args, **kwargs)
        if not self.model:
            raise Exception('You have to Specify model') 
        if request.user.is_authenticated:
            try:
                self.user = self.model.objects.get(pk=request.user.pk)
            except:
                if self.redirect_url:
                    return redirect(self.redirect_url)
                return self.user_required(request)
        else:
            if self.redirect_url:
                return redirect(self.redirect_url)
            return self.login_required(request)
        
        return super().dispatch(request, *args, **kwargs)
    
    def check_user(self, request):
        if not self.model:
            raise Exception('You have to Specify model') 
        if request.user.is_authenticated:
            try:
                self.user = self.model.objects.get(pk=request.user.pk)
                return self.user
            except:
                return False
        else:
            return False

    def user_required(self, request):
        messages.error(request, f'You have to be {str(self.model)} to access this page.')
        if not self.register_url:
            return HttpResponse('You have to login as supplier')
        return redirect(reverse_lazy(self.register_url))

    def login_required(self, request):
        messages.error(request, 'You have to login to system to access this page.')
        if not self.login_url:
            if not settings.LOGIN_URL:
                return HttpResponse('You have to login to system')
            else:
                return redirect(reverse_lazy(settings.LOGIN_URLlogin_url, kwargs={'next': request.META.get('HTTP_REFERER', None) or '/'}))
        else:
            return redirect(reverse_lazy(self.login_url) + f'?next={request.META.get("HTTP_REFERER", None) or "/"}')


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
    login_url = 'user:login'
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
        try:
            if request.user.user_type:
                items = []
                for item in request.cart.cartitems.all():
                    items.append((item.product, item.quantity, item.get_price))
                context = {
                    'items': items
                }
        except:
            products = Product.objects.all()
            items = []
            for item in request.cart:
                product = products.get(pk=item[0])
                quantity = item[1]
                item_total_price = product.price * int(quantity)
                items.append((product, quantity, item_total_price))
            context = {
                'items': items
                }
        return render(request, 'cart.html', context)
        

class AddToCart(CustomRequiredMixin):

    '''add product to cart items for requested user '''
    model = Customer
    boolean = True

    def post(self,request, pk):

        '''authenticating user'''
        self.user = self.check_user(request)
        if self.user:
            self.add_to_cart_users(request, pk)
        else:
            self.add_to_cart_anonymous(request, pk)

        return redirect(reverse_lazy('shop:home'))

    def add_to_cart_users(self, request, pk):
        '''
        if request user is authenticated, the product will be added
         to the cartitems in his/her account
        '''
        cartitem = CartItems.objects.filter(cart=Cart.objects.get_or_create(customer=self.user, state='O')[0],
            product=Product.objects.get(pk=pk))
        if cartitem:
            cartitem[0].quantity += int(request.POST['quantity'])
            cartitem[0].save()
        else:
            CartItems.objects.create(
            cart=Cart.objects.get_or_create(customer=self.user, state='O')[0],
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
        for i in request.session['cart']:
            if i[0] == pk:
                index = request.session['cart'].index(i)
                qty = request.session['cart'][index][1] +int(qty)
                request.session['cart'].pop(index)
                break
        request.session['cart'] += [(pk, int(qty))]
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            feed = Feedback.objects.filter(
                customer=self.request.user,
                product=super().get_object()
                )
            if feed.exists():
                form = CreateCommentForm(instance=feed.get())
            else:
                form = CreateCommentForm()
            result = {
                'form': form
            }
            context.update(result)
        return context


class CreateCommentView(CustomRequiredMixin):
    model = Customer
    
    redirect_url = reverse_lazy("user:login")
    register_url = reverse_lazy("user:register_customer")

    def post(self, request):
        product = Product.objects.get(pk=request.POST['product'])
        feed = Feedback.objects.filter(
            customer=request.user,
            product=product)
        
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
    cartitem = CartItems.objects.get(pk=pk)
    cartitem.quantity += 1
    cartitem.save()
    return redirect(request.META.get('HTTP_REFERER'))


def minus_cart(request, pk):
    cartitem = CartItems.objects.get(pk=pk)
    cartitem.quantity -= 1
    cartitem.save()
    return redirect(request.META.get('HTTP_REFERER'))

def remove_from_cart(request, pk):
    cartitem = CartItems.objects.get(pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))
