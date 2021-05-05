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
                if redirect_url:
                    return redirect(redirect_url)
                return self.user_required(request)
        else:
            if redirect_url:
                return redirect(redirect_url)
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


class Gruoping(View):
    '''
    you can inherit this class if you want to have grouping
    and filter and search functionality in your view.
    add this line in your get method.
    <context_name> = self.get_query_set(request, query_set=None)
    '''

    def get_context(self, context,**kwargs):
        '''
        add tags and categories and brands to the given context
        '''
        
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['tags'] = Tag.objects.all()[:30]
        return context
    
    def get_query_set(self, query_set):
        '''
        filter queryset base on given query.
        filter is base on this keywords --> brand, cat, tag, q
        q will query on name and description fileds.
        return all products if there was'nt any query.
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
        
 

class HomePageView(ListView, Gruoping):
    paginate_by = 9
    login_url = 'user:login'
    model = Product
    template_name = 'product-list.html'

    def get_context_data(self):
        context = super().get_context_data()
        return super().get_context(context)

    def get_ordering(self):
        return self.request.GET.get('sort', None)

    def get_queryset(self):
        print(self.request.GET.get('sort', None))
        self.ordering = self.request.GET.get('sort', None)
        queryset = super().get_queryset()
        queryset = super().get_query_set(queryset)
        if 'q' in self.request.GET:
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET.get('q'))|
                Q(description__icontains=self.request.GET.get('q'))
                )
        if self.ordering:
            queryset.order_by(self.ordering)
        return queryset

    
class CartItemView(View):
    def get(self, request):
        return render(request, 'cart.html')
    
    def delete(self, request):
        print('hello')


class AddToCart(CustomRequiredMixin):

    '''add product to cart items for requested user '''
    model = Customer
    boolean = True

    def post(self,request, pk):
        # print(request.cart.)

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
        request.session['cart'] += [(pk, qty)]
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feed = Feedback.objects.filter(
            customer=self.request.user,
            product=super().get_object())
        
        if feed.exists():
            form = CreateCommentForm(instance=feed.get())
        else:
            form = CreateCommentForm()
        result = {
            'form': form
        }
        context.update(result)
        print(context)
        return context


class CreateCommentView(CustomRequiredMixin):
    model = Customer
    boolean = True

    def post(self, request):
        user = super().check_user(request)
        print(request.POST['product'])
        product = Product.objects.get(pk=request.POST['product'])
        feed = Feedback.objects.filter(
            customer=user,
            product=product)
        
        if feed.exists():
            form = CreateCommentForm(request.POST, instance=feed.get())
        else:
            form = CreateCommentForm(request.POST)
        if form.is_valid():
            form.instance.customer = user
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

