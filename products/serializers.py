from rest_framework import serializers
from products.models import Category, Company, Product


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ProductSerializer(serializers.ModelSerializer):
    """There are two ways to display the name of the foreign table"""

    """ 
    1. Is to use nested serializer
    """
    category_name = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    company_name = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), write_only=True
    )
    """ 
    2. Second is to just use serializers.StringRelatedField() This will use the __str__ methoSecond is to just use serializers.StringRelatedField() This will use the __str__ method.
    """
    company = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "stock",
            "price",
            "category",
            "company",
            "category_name",
            "company_name",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def create(self, validated_data):
        category = validated_data.pop("category_name")
        company = validated_data.pop("company_name")
        product = Product.objects.create(
            **validated_data, category=category, company=company
        )
        return product
