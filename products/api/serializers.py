from rest_framework import serializers

from products import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['cat_name', 'subcategory']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['tag']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute
        fields = ['name', 'value']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ['brand_name']


class ProductCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    tag = TagSerializer()
    attribute = AttributeSerializer()
    
    class Meta:
        model = models.Product
        fields = [ 'name', 'price', 'quantity', 'image', 'description', 'category', 'tag', 'attribute', 'brand',]

    def create(self, validated_data):
        user = self.context['request'].user
        product = models.Product.objects.create(
            supplier = user,
            **validated_data
        )
        return product


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Product
        fields = ['url','category', 'tag', 'attribute', 'name', 'price', 'image', 'published_date', 'brand']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image', 'produc']


# class FeedBackSerializer(serializers.ModelSerializer):
    # class Me

# class ProductDetailSerializer(serializers.ModelSerializer):
