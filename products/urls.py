from django.urls import path
from . import views
from .api import views as apiviews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', apiviews.ProductViewSet)

app_name = 'shop'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:pk>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('create-comment/', views.CreateCommentView.as_view(), name='create_comment'),
    path('cart/', views.CartItemView.as_view(), name='cart'),
    path('plus-cart/<int:pk>/', views.plus_cart, name='plus_cart'),
    path('minus-cart/<int:pk>/', views.minus_cart, name='minus_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('send-sms/', views.send_sms, name='send_sms'),
    #api

    ] + router.urls