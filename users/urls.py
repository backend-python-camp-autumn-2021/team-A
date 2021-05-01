from django.urls import path
from . import views

app_name = 'user'
urlpatterns =[
    path('login/', views.AuthenticationView.as_view(), name='login'),
    path('register-customer/', views.RegisterCustomerView.as_view(), name='register_customer'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.ResetPassword.as_view(), name='reset_password'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    # path('profile/', views.CustomerProfileView.as_view(), name='profile'),



    path('logout/', views.logout_page, name='logout'),

]