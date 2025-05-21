from rest_framework import serializers
from .models import Buyer_credit, Item_purchased, Item
from user.models import CustomUser
from django.contrib.auth.hashers import make_password

class UsercreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer_credit
        fields = '__all__'


class ItemPurchasedSerializer(serializers.ModelSerializer):  
    Bill = serializers.SerializerMethodField()
    class Meta:
        model = Item_purchased
        exclude = ['buyer']

    def get_Bill(self, obj):
        item_name = obj.item.name if obj.item else "Unknown Item"
        item_price = obj.item.price if obj.item else "Unknown Price"
        return f"{item_name} purchased by {obj.buyer.username} Total cost is {item_price} on {obj.purchase_date:%Y-%m-%d}"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = CustomUser
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta: 
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'user_type']

    def create(self, validated_data):   
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)


