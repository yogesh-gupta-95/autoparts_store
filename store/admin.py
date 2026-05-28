from django.contrib import admin
from .models import Category, Product, Review, CarMake, CarModel, ProductCompatibility

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = ['name', 'category', 'price', 'stock', 'is_available']
    list_filter    = ['category', 'is_available']
    search_fields  = ['name', 'brand']
    list_editable  = ['price', 'stock', 'is_available']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'name', 'year']
    list_filter  = ['make']

@admin.register(ProductCompatibility)
class ProductCompatibilityAdmin(admin.ModelAdmin):
    list_display = ['product', 'car_model']