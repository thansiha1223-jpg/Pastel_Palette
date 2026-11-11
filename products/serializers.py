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

    # Object-level validation
    def validate(self, data):
        name = data.get(
            'name',
            self.instance.name if self.instance else None
        )

        category = data.get(
            'category',
            self.instance.category if self.instance else None
        )

        if name and category:
            products = Product.objects.filter(
                name__iexact=name,
                category=category
            )

            if self.instance:
                products = products.exclude(
                    pk=self.instance.pk
                )

            if products.exists():
                raise serializers.ValidationError(
                    "This product already exists in this category."
                )

        return data

    class Meta:
        model = Product
        fields = '__all__'