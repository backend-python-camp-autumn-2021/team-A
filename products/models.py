from django.db import models
from users.models import Customer, Supplier


class Brand(models.Model):
    brand_name = models.CharField(max_length=255)

class Category(models.Model):
    cat_name = models.CharField(max_length=255)
    subcategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Tag(models.Model):
    tag = models.CharField(max_length=150)


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=150)


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default="General", on_delete=models.SET_DEFAULT)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    tag = models.ManyToManyField(Tag)
    attribute = models.ManyToManyField(Attribute)
    image = models.ImageField()


class ProductList(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def get_available(self):
        return bool(self.quantity)

    def reduce_product(self, N):
        if self.quantity - N < 0:
            return False
        else:
            self.quantity -= N

    def increase_product(self, N):
        self.quantity += N


class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Cart(models.Model):
    STATE_CHOICES = (
        ('O', 'Open'),
        ('P', 'Paid'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancle'),
    )
    state = models.CharField(max_length=1,  choices=STATE_CHOICES)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE) 
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def get_price(self):
        pass

    def get_quantity(self):
        pass


class Transaction(models.Model):
    details = models.TextField()
    pay_date = models.DateTimeField()
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)   
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    text = models.TextField('متن نظر')
    rate = models.FloatField(default=1)

    def __str__(self):
        return self.customer


