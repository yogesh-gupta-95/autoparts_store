from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review, CarMake, CarModel


def home(request):
    categories  = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(is_available=True, category__id=category_id)
        selected = Category.objects.get(id=category_id)
    else:
        products = Product.objects.filter(is_available=True)
        selected = None
    new_arrivals = Product.objects.filter(is_available=True).order_by('-created_at')[:4]
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'selected': selected,
        'new_arrivals': new_arrivals,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')
    related = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(pk=pk)[:4]
    if request.method == 'POST' and request.user.is_authenticated:
        rating  = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            return redirect('product_detail', pk=pk)
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related': related,
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
def update_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    action = request.GET.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
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
            # Reduce stock
            product = item.product
            product.stock -= item.quantity
            if product.stock < 0:
                product.stock = 0
            if product.stock == 0:
                product.is_available = False
            product.save()

        cart.items.all().delete()
        return redirect('order_success')
    return redirect('checkout')


@login_required(login_url='/users/login/')
def order_success(request):
    order = Order.objects.filter(user=request.user).last()
    return render(request, 'store/order_success.html', {'order': order})


@login_required(login_url='/users/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required(login_url='/users/login/')
def order_tracking(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_tracking.html', {'order': order})


def search(request):
    query    = request.GET.get('q', '')
    products = Product.objects.filter(
        name__icontains=query,
        is_available=True
    ) if query else []
    return render(request, 'store/search.html', {
        'products': products,
        'query': query
    })


def browse_by_car(request):
    makes      = CarMake.objects.all()
    make_id    = request.GET.get('make')
    model_id   = request.GET.get('model')
    products   = []
    car_models = []
    selected_make  = None
    selected_model = None
    if make_id:
        selected_make = CarMake.objects.get(id=make_id)
        car_models    = CarModel.objects.filter(make__id=make_id)
    if model_id:
        selected_model = CarModel.objects.get(id=model_id)
        products = Product.objects.filter(
            compatible_cars__car_model__id=model_id,
            is_available=True
        )
    return render(request, 'store/browse_by_car.html', {
        'makes':          makes,
        'car_models':     car_models,
        'products':       products,
        'selected_make':  selected_make,
        'selected_model': selected_model,
    })


@login_required(login_url='/users/login/')
def sales_report(request):
    total_orders   = Order.objects.count()
    total_revenue  = Order.objects.aggregate(Sum('total'))['total__sum'] or 0
    paid_orders    = Order.objects.filter(status='paid').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    delivered      = Order.objects.filter(status='delivered').count()
    recent_orders  = Order.objects.order_by('-created_at')[:10]
    top_products   = OrderItem.objects.values(
        'product__name'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]
    return render(request, 'store/sales_report.html', {
        'total_orders':   total_orders,
        'total_revenue':  total_revenue,
        'paid_orders':    paid_orders,
        'shipped_orders': shipped_orders,
        'delivered':      delivered,
        'recent_orders':  recent_orders,
        'top_products':   top_products,
    })