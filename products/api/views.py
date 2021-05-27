from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .serializers import ProductListSerializer, ProductCreateSerializer
from products.models import Product

class ProductReadonlyViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductViewSet(ModelViewSet):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()
