from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product

# Create your views here.
class CartView(generics.RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )
        return cart


class AddToCartView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if quantity < 1:
            return Response(
                {'error': 'Quantity must be at least 1'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            {'message': 'Product added to cart'},
            status=status.HTTP_200_OK
        )


class UpdateCartItemView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        try:
            cart_item = CartItem.objects.get(
                id=pk,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get('quantity')

        if quantity is None or quantity < 1:
            return Response(
                {'error': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if cart_item.product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response(
            {'message': 'Cart updated successfully'},
            status=status.HTTP_200_OK
        )


class RemoveCartItemView(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        )