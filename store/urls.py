
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, api_views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Product pages
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    # Cart
    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),
    path('cart/', views.cart_view, name='cart'),
    path(
        'cart/update/<int:item_id>/',
        views.update_cart,
        name='update_cart'
    ),
    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),
    path('my-orders/', views.my_orders, name='my_orders'),
    path(
        'order/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    # Authentication
    path('register/', views.register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='store/login.html'
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Admin analytics
    path(
        'admin-analytics/',
        views.admin_analytics,
        name='admin_analytics'
    ),

    # Product APIs
    path(
        'api/products/',
        api_views.ProductListAPIView.as_view(),
        name='api_product_list'
    ),
    path(
        'api/products/create/',
        api_views.ProductCreateAPIView.as_view(),
        name='api_product_create'
    ),
    path(
        'api/products/<int:pk>/update/',
        api_views.ProductUpdateAPIView.as_view(),
        name='api_product_update'
    ),
    path(
        'api/products/<int:pk>/delete/',
        api_views.ProductDeleteAPIView.as_view(),
        name='api_product_delete'
    ),
    path(
        'api/products/<int:pk>/',
        api_views.ProductDetailAPIView.as_view(),
        name='api_product_detail'
    ),

    # Order APIs
    path(
        'api/my-orders/',
        api_views.MyOrderListAPIView.as_view(),
        name='api_my_orders'
    ),
    path(
        'api/orders/<int:pk>/',
        api_views.OrderDetailAPIView.as_view(),
        name='api_order_detail'
    ),
    path(
        'api/admin/orders/',
        api_views.AdminOrderListAPIView.as_view(),
        name='api_admin_orders'
    ),
]