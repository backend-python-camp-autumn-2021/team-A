from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Supplier, Customer
from .models import Category, Tag, Brand, Product, CartItems, Cart
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView, DetailView


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
            if redirect:
                return redirect(redirect_url)
            return self.login_required(request)
        
        return super().dispatch(request, *args, **kwargs)
    
    
    def check_user(self, request):
        print('in check usssssssssssssssssssssser')
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


class Gruoping(ListView):
    '''
    you can inherit this class if you want to have grouping
    and filter and search functionality in your view.
    add this line in your get method.
    <context_name> = self.get_query_set(request, query_set=None)
    '''


    def get_context_data(self, context=None,**kwargs):
        '''
        add tags and categories and brands to the given context
        '''
        print(self.request.session)
        if not context:
            context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['tags'] = Tag.objects.all()[:30]
        return context
    
    def get_queryset(self, query_set=None):
        '''
        filter queryset base on given query.
        filter is base on this keywords --> brand, cat, tag, q
        q will query on name and description fileds.
        return all products if there was'nt any query.
        '''
        print(self.request.session.get('cart'))
        print(self.request.user.user_type)
        print("man injaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaam")
        self.ordering = self.request.GET.get('sort', None)
        
        if not query_set:
            query_set = super().get_queryset()
        
        if 'cat' in self.request.GET:
            query_set = query_set.filter(
                category__pk=self.request.GET.get('cat')
                )
        elif 'brand' in self.request.GET:
            query_set = query_set.filter(brand__pk=self.request.GET.get('brand'))
        elif 'tag' in self.request.GET:
            query_set = query_set.filter(tag__pk=self.request.GET.get('tag'))
        if 'q' in self.request.GET:
            query_set = query_set.filter(
                Q(name__icontains=self.request.GET.get('q'))|
                Q(description__icontains=self.request.GET.get('q'))
                )
        return query_set

        
 

class HomePageView(Gruoping):
    paginate_by = 9
    login_url = 'user:login'
    model = Product
    template_name = 'product-list.html'
    # def get(self, request):
    #     context = self.get_queryset(request)
    #     return render(request, 'product-list.html', context)


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
            print('i am here', self.user)
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
            quantity=request.GET['quantity'],
            )
    
    def add_to_cart_anonymous(self, request, pk):
        """
        if user is not authenticated, the product will be add to request's session
        """
        print('i am anonymouuuuuuus')
        if 'cart' not in request.session:
            print('not iiiiiiiiiiiiiiiiiiiiiiiiiiin')
            request.session['cart'] = []
        print(request.POST['quantity'])
        qty = request.POST['quantity']
        request.session['cart'] += [(pk, qty)]
        # session.save()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'




