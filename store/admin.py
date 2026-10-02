
from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'brand',
        'price',
        'stock',
        'created_at',
    )
    list_filter = ('category', 'brand')
    search_fields = (
        'name',
        'description',
        'brand__name',
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    list_filter = ('product',)
    search_fields = (
        'product__name',
        'cart__user__username',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    list_editable = ('status',)
    readonly_fields = (
        'user',
        'total_amount',
        'created_at',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
    )
    search_fields = (
        'product__name',
        'order__user__username',
    )
    readonly_fields = (
        'order',
        'product',
        'quantity',
        'price',
    )