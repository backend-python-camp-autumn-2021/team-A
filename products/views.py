from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Supplier, Customer


class HomePageView(LoginRequiredMixin, View):
    login_url = 'user:login'
    def get(self, request):
        return render(request, 'home.html', {})