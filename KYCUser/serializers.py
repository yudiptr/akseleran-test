from rest_framework import serializers
from .models import KYCUsers

class KYCUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCUsers
        fields = '__all__'



class AdminViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCUsers
        fields = ['name', 'user_id', 'phone_number', 'email', 'address', 'city', 'zip_code', 'email_before_update', 'phone_number_before_update']
