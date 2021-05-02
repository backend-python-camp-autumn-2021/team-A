from django.urls import path, reverse_lazy
from . import views


app_name = 'user'
urlpatterns =[
    path('login/', views.AuthenticationView.as_view(), name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register-customer/', views.RegisterCustomerView.as_view(), name='register_customer'),
    path('register-supplier/', views.RegisterSupplierView.as_view(), name='register_supplier'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('update-supplier/<int:pk>/', views.UpdateSupplierView.as_view(), name='update_supplier'),
    path('update-customer/<int:pk>/', views.UpdateCustomerView.as_view(), name='update_customer'),
    
    path('reset-password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('set-password/', views.PasswordResetVerifyView.as_view(), name='set_password'),
    




]