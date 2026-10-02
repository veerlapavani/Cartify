
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum

from .models import (
    Product,
    Category,
    Brand,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    search = request.GET.get('search')

    if search:
        products = products.filter(name__icontains=search)

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Account created successfully. Please login.'
            )

            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {
        'form': form
    })


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(
            request,
            'This product is currently out of stock.'
        )
        return redirect('product_detail', product_id=product.id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        if cart_item.quantity >= product.stock:
            messages.error(
                request,
                f'Only {product.stock} items available in stock.'
            )
            return redirect('cart')

        cart_item.quantity += 1
        cart_item.save()

    messages.success(
        request,
        f'{product.name} added to cart.'
    )

    return redirect('cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.select_related('product').all()

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(request, 'store/cart.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })


@login_required
@require_POST
def update_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        messages.error(request, 'Invalid quantity.')
        return redirect('cart')

    if quantity <= 0:
        item.delete()
        messages.success(request, 'Item removed from cart.')
        return redirect('cart')

    if quantity > item.product.stock:
        messages.error(
            request,
            f'Only {item.product.stock} items available in stock.'
        )
        return redirect('cart')

    item.quantity = quantity
    item.save()

    messages.success(request, 'Cart updated successfully.')

    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    messages.success(request, 'Item removed from cart.')

    return redirect('cart')


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.select_related('product').all()

    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })


@login_required
@require_POST
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)

    items = list(
        cart.items.select_related('product').all()
    )

    if not items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    for item in items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f'Not enough stock for {item.product.name}. '
                f'Available stock: {item.product.stock}.'
            )
            return redirect('cart')

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='Pending'
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save(update_fields=['stock'])

        CartItem.objects.filter(cart=cart).delete()

    messages.success(
        request,
        f'Order #{order.id} placed successfully!'
    )

    return redirect('order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(request, 'store/order_success.html', {
        'order': order
    })


@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related('items__product')
        .order_by('-created_at')
    )

    return render(request, 'store/my_orders.html', {
        'orders': orders
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user
    )

    return render(request, 'store/order_detail.html', {
        'order': order
    })

@staff_member_required
def admin_analytics(request):
    from django.db.models.functions import TruncMonth

    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_brands = Brand.objects.count()
    total_users = User.objects.count()
    total_orders = Order.objects.count()

    total_revenue = (
        Order.objects
        .exclude(status='Cancelled')
        .aggregate(total=Sum('total_amount'))['total']
        or 0
    )

    pending_orders = Order.objects.filter(status='Pending').count()
    confirmed_orders = Order.objects.filter(status='Confirmed').count()
    shipped_orders = Order.objects.filter(status='Shipped').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    cancelled_orders = Order.objects.filter(status='Cancelled').count()

    monthly_data = (
        Order.objects
        .exclude(status='Cancelled')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_amount'))
        .order_by('month')
    )

    monthly_revenue = [
        {
            'month': item['month'].strftime('%b %Y'),
            'revenue': float(item['revenue'] or 0),
        }
        for item in monthly_data
    ]

    recent_orders = (
        Order.objects
        .select_related('user')
        .order_by('-created_at')[:10]
    )

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_brands': total_brands,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'recent_orders': recent_orders,
        'monthly_revenue': monthly_revenue,
    }

    return render(
        request,
        'store/admin_analytics.html',
        context
    )

