from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, CartItem, Order, OrderItem

def home(request):
    products   = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {
        'product': product
    })

@login_required(login_url='/users/login/')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='/users/login/')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required(login_url='/users/login/')
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='/users/login/')
def checkout(request):
    cart  = get_object_or_404(Cart, user=request.user)
    total = cart.get_total()
    return render(request, 'store/checkout.html', {
        'cart': cart,
        'total': total,
    })

@login_required(login_url='/users/login/')
def payment(request):
    if request.method == 'POST':
        cart  = get_object_or_404(Cart, user=request.user)
        total = cart.get_total()

        order = Order.objects.create(
            user=request.user,
            total=total,
            status='paid'
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )

        cart.items.all().delete()
        return redirect('order_success')

    return redirect('checkout')

@login_required(login_url='/users/login/')
def order_success(request):
    order = Order.objects.filter(user=request.user).last()
    return render(request, 'store/order_success.html', {'order': order})