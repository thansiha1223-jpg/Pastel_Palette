
from rest_framework import serializers
from django.db import transaction
from decimal import Decimal
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity']


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'items',
            'total_amount',
            'status',
            'created_at'
        ]
        read_only_fields = [
            'user',
            'total_amount',
            'status',
            'created_at'
        ]

    def create(self, validated_data):

        items_data = validated_data.pop('items')

        if not items_data:
            raise serializers.ValidationError(
                "An order must contain at least one item."
            )

        # Combine duplicate products
        products = {}

        for item in items_data:
            product = item['product']
            quantity = item['quantity']

            if quantity <= 0:
                raise serializers.ValidationError(
                    "Quantity must be greater than zero."
                )

            if product.id in products:
                products[product.id]['quantity'] += quantity
            else:
                products[product.id] = {
                    'product': product,
                    'quantity': quantity
                }

        # Start database transaction
        with transaction.atomic():

            order = Order.objects.create(
                user=self.context['request'].user,
                total_amount=Decimal('0.00')
            )

            total_amount = Decimal('0.00')

            for item in products.values():

                product = Product.objects.select_for_update().get(
                    id=item['product'].id
                )

                quantity = item['quantity']

                if product.stock < quantity:
                    raise serializers.ValidationError(
                        f"Insufficient stock for {product.name}."
                    )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

                product.stock -= quantity
                product.save(update_fields=['stock'])

                total_amount += product.price * quantity

            order.total_amount = total_amount
            order.save(update_fields=['total_amount'])

        return order




