from django.urls import path, reverse_lazy
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .api import views as apiviews
from . import views

# router = DefaultRouter()
# router.register(r'supplier', apiviews.SupplierViewSet)

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
    path('set-password/<token>/', views.PasswordResetVerifyView.as_view(), name='set_password'),
    # api
    path('signup-supplier/', apiviews.RegisterSupllierApiView.as_view(), name='sugnup_supplier'),
    path('signup-customer/', apiviews.RegisterCustomerApiView.as_view(), name='sugnup_customer'),
    path('change-password-api/', apiviews.ChangePassowrd.as_view(), name='change_passwordr_api'),
    path('reset-password-api/', apiviews.ResetPasswordApiView.as_view(), name='reset_passwordr_api'),
    path('set-password-api/<token>/', apiviews.SetPasswordApiView.as_view(), name='set_password_api'),


    path('profile/', apiviews.SupplierView.as_view(), name='sugnup_supplier'),
    path('login-api/', obtain_auth_token, name='login_api')
]


# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])