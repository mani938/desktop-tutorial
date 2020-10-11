
from rest_framework import serializers
from app24.models import ProductModel
class ProductSerializer(serializers.Serializer):

    name=serializers.CharField(max_length=100)
    price=serializers.FloatField()
    quantity=serializers.IntegerField()

    def create(self, validated_data):
        try:
             return ProductModel.objects.create(**validated_data)
        except:
            raise serializers.ValidationError("Invalid Data")