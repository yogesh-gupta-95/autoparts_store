from django.shortcuts import render
from .models import Product, Category

def home(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })