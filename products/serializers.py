from rest_framework import serializers
from products.models import Category, Company, Product, Reviews


class CompanySerializer(serializers.ModelSerializer):
    """CompanySerializer: Simple Serializer with fields as name."""

    class Meta:
        model = Company
        fields = ["name"]


class CategorySerializer(serializers.ModelSerializer):
    """CategorySerializer: Simple Serializer with fields as name."""

    class Meta:
        model = Category
        fields = ["name"]


class ReviewsSerializer(serializers.ModelSerializer):
    """ReviewsSerializer: Simple serializer with username as foregin key."""

    username = serializers.CharField(source="user.username")

    class Meta:
        model = Reviews
        fields = ["username", "review_text", "rating"]


class ProductSerializer(serializers.ModelSerializer):
    """ProductSerializer: So here we have the products serializer."""

    reviews = ReviewsSerializer(many=True, read_only=True)
    """ serializers.PrimaryKeyRelatedField is used to represent a relationship between
    two models using primary key."""
    category_name = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    company_name = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), write_only=True
    )
    """serializers.StringRelatedField() will give us access to the foreign key and print whatever is written in the __str__ magic method."""
    company = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "stock",
            "price",
            "reviews",
            "category",
            "company",
            "category_name",
            "company_name",
        ]

    """ field_validator """

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    """
    The create() method is being overridden first both the category and company names
    are being popped and than the validated_data along with the category and company 
    is being created using Model.objects.create() method
    """

    def create(self, validated_data):
        category = validated_data.pop("category_name")
        company = validated_data.pop("company_name")
        return Product.objects.create(
            **validated_data, category=category, company=company
        )
