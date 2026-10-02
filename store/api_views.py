
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


# 1. List all products
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.select_related(
        "category", "brand"
    ).all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


# 2. View one product
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related(
        "category", "brand"
    ).all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


# 3. Create a product (admin only)
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


# 4. Update a product (admin only)
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


# 5. Delete a product (admin only)
class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


# 6. View logged-in user's orders
class MyOrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )


# 7. View one order
class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items__product")

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)


# 8. View all orders (admin only)
class AdminOrderListAPIView(generics.ListAPIView):
    queryset = (
        Order.objects.select_related("user")
        .prefetch_related("items__product")
        .order_by("-created_at")
    )
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]