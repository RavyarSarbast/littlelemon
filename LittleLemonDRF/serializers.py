from rest_framework import serializers
from .models import MenuItem, Cart, Order
from django.contrib.auth.models import User,Group

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory']
        extra_kwargs = {
            'price': {'min_value': 2},
            'inventory':{'min_value':0}
        }
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','user','item','quantity']
        extra_kwargs = {
            'quantity':{'min_value':1}
        }
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','item','quantity']
        extra_kwargs = {
            'quantity':{'min_value':1}
        }
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','email']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
