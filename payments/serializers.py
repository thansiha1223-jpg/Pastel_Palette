
from rest_framework import serializers
from .models import Payment
from orders.models import Order


class PaymentSerializer(serializers.ModelSerializer):

    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all()
    )

    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'payment_method',
            'payment_status',
            'amount',
            'created_at'
        ]

        read_only_fields = [
            'payment_status',
            'amount',
            'created_at'
        ]

    def validate_order(self, order):
        user = self.context['request'].user

        if order.user != user:
            raise serializers.ValidationError(
                "You cannot make payment for another user's order."
            )

        if Payment.objects.filter(order=order).exists():
            raise serializers.ValidationError(
                "Payment already exists for this order."
            )

        return order

    def create(self, validated_data):
        order = validated_data['order']

        payment = Payment.objects.create(
            order=order,
            payment_method=validated_data['payment_method'],
            amount=order.total_amount
        )

        return payment
