from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Supplier, Customer
from .models import Category, Tag, Brand, Product
from django.db.models import Q


class Gruoping(View):
    '''
    you can inherit this class if you want to have grouping
    and filter and search functionality in your view.
    add this line in your get method.
    <context_name> = self.get_query_set(request, query_set=None)
    '''

    queryset_name = 'query_set'
    
    def handle_context(self, context=None):
        '''
        add tags and categories and brands to the given context
        '''
        if not context:
            context = {}
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['tags'] = Tag.objects.all()[:30]
        return context
    
    def get_query_set(self, request, query_set=None):
        '''
        filter queryset base on given query.
        filter is base on this keywords --> brand, cat, tag, q
        q will query on name and description fileds.
        return all products if there was'nt any query.
        '''
        if not query_set:
            query_set = Product.objects.all()
        if 'cat' in request.GET:
            query_set = query_set.filter(category__pk=request.GET.get('cat'))
        elif 'brand' in request.GET:
            query_set = query_set.filter(brand__pk=request.GET.get('brand'))
        elif 'tag' in request.GET:
            query_set = query_set.filter(tag__pk=request.GET.get('tag'))
        elif 'q' in request.GET:
            query_set = query_set.filter(
                Q(name__icontains=request.GET.get('q'))|
                Q(description__icontains=request.GET.get('q'))
                )
        context = self.handle_context()
        context[self.queryset_name] = query_set
        return context
 


class HomePageView(LoginRequiredMixin, Gruoping):
    login_url = 'user:login'
    def get(self, request):
        context = self.handle_context()
        return render(request, 'product-list.html', context)
