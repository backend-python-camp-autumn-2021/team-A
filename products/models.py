from django.db import models
from users.models import Customer, Supplier


class Brand(models.Model):
    brand_name = models.CharField(max_length=255)

    def __str__(self):
        return self.brand_name

    @property
    def get_product_number(self):
        count = self.products.count()
        return count


class Category(models.Model):
    cat_name = models.CharField(max_length=255)
    subcategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='parent_cat')

    def __str__(self):
        return self.cat_name


class Tag(models.Model):
    tag = models.CharField(max_length=150)

    def __str__(self):
        return self.tag


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    tag = models.ManyToManyField(Tag, related_name='products')
    attribute = models.ManyToManyField(Attribute, related_name='products')
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to='product_img')
    quantity = models.IntegerField(default=1)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_img')
    produc = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.produc.name


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart') 
    STATE_CHOICES = (
        ('O', 'Open'),
        ('P', 'Paid'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancle'),
    )
    state = models.CharField(max_length=1,  choices=STATE_CHOICES)
    
    def get_price(self):
        pass

    def get_number_of_carts(self):
        pass

    def get_number_of_products(self):
        pass

    def __str__(self):
        return self.customer.name


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name


class Factor(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='factor')
    details = models.TextField()
    pay_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pay_date


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks') 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedbacks')   
    text = models.TextField('Feed Back Text')
    rate = models.FloatField(default=1)

    def __str__(self):
        return self.customer
