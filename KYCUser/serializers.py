from rest_framework import serializers
from .models import KYCUsers

class KYCUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCUsers
        fields = '__all__'
