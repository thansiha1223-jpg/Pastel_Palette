
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    # Field-level validation
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Product name cannot be empty."
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Stock cannot be negative."
            )
        return value

    # Object-level validation
    def validate(self, data):
        name = data.get('name', getattr(self.instance, 'name', ''))

        if name and name.strip().lower() == 'test':
            raise serializers.ValidationError(
                "Test is not allowed as a product name."
            )

        return data

    class Meta:
        model = Product
        fields = '__all__'
