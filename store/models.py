from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    name        = models.CharField(max_length=300)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    image       = models.ImageField(upload_to='products/')
    brand       = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name