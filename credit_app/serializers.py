from rest_framework import serializers
from .models import Buyer_credit, Item_purchased, Item
from user.models import CustomUser
from django.contrib.auth.hashers import make_password

class UsercreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer_credit
        fields = '__all__'

    def to_representation(self, instance):
        buyer = instance.buyer
        credits = instance.credit_amount

        return{
            "Credit_Report" : f" Hello {buyer} you have Rs {credits} in your account"
        }

class ItemPurchasedSerializer(serializers.ModelSerializer):  
    
    class Meta:
        model = Item_purchased
        fields = '__all__'

   
        
    def to_representation(self, instance):
        item_name = instance.item.name if instance.item else "Unknown Item"
        item_price = instance.item.price if instance.item else "Unknown Price"
        return{ 
            "item": f"Bought {item_name}",
            "quantity": instance.quantity,
            "purchase_date": instance.purchase_date,
            "buyer": instance.buyer.username,
            "total Cost" : f"Rs: {item_price*instance.quantity}",
            "Remark" : f"{item_name} purchased by {instance.buyer.username} Total cost is Rs: {item_price*instance.quantity} on {instance.purchase_date:%Y-%m-%d}",
        }
        




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
    


