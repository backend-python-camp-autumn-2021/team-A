from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from products.api.serializers import (
    ProductListSerializer, ProductCreateSerializer,
    BrandSerializer, CategorySerializer, AttributeSerializer,
    TagSerializer, ProductImageSerializer)
from products.models import Product, Brand, Tag, Attribute, ProductImage, Category
from users.models import Supplier

# class ProductReadonlyViewSet(ReadOnlyModelViewSet):
#     serializer_class = ProductListSerializer
#     queryset = Product.objects.all()


class ProductViewSet(ModelViewSet):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if request.method not in ['GET', 'POST']:
            if self.get_object().supplier != request.user:
                raise PermissionDenied('only owner can Edit it')
        return super().dispatch(request, *args, **kwargs)


class BrandViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, Supplier):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('only Suppliers can access Brands') 


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, Supplier):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('only Suppliers can access Tags')


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, Supplier):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('only Suppliers can access Categories')



class AttributeViewSet(ModelViewSet):
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, Supplier):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('only Suppliers can access Attributes')

