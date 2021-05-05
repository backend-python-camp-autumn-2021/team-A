from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:pk>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('create-comment/', views.CreateCommentView.as_view(), name='create_comment'),


]