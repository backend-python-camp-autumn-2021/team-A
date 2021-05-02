from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Supplier, Customer
from .models import Category, Tag, Brand


class Gruoping(View):
    '''
    we literally need the some grouping in many pages.
    if you want your own custome gruoing you can custom handele_context method.
    '''
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

 


class HomePageView(LoginRequiredMixin, Gruoping):
    login_url = 'user:login'
    def get(self, request):
        context = self.handle_context()
        return render(request, 'product-list.html', context)
