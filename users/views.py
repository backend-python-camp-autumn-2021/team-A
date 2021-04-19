from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse


def login_page(request):
    if request.method == 'GET':
        destination = request.META.get('HTTP_REFERER')
        return render(request, 'login.html', {'destination':destination})
    elif request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        destination = request.POST.get('destination')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if destination:
                return redirect(destination)
            return HttpResponse('login successfully')
        else:
            return HttpResponse('You are not authenticated')
            


def logout_page(request):
    destination = request.META.get('HTTP_REFERER')
    logout(request)
    if destination:
        return redirect(destination)
    return HttpResponse('logout successfully')