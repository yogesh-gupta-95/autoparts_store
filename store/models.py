from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    name         = models.CharField(max_length=300)
    description  = models.TextField()
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    stock        = models.PositiveIntegerField(default=0)
    image        = models.ImageField(upload_to='products/')
    brand        = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('paid',      'Paid'),
        ('shipped',   'Shipped'),
        ('delivered', 'Delivered'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total      = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.price * self.quantity