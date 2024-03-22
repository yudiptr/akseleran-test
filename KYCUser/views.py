from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import KYCUsers
from .serializers import KYCUserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class KYCUserViewSet(viewsets.ModelViewSet):
    queryset = KYCUsers.objects.all()
    serializer_class = KYCUserSerializer

    @action(detail=False, methods=['get'])
    def filter_by_user_id(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter is required'}, status=400)

        queryset = KYCUsers.objects.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['put'])
    def update_by_user_id(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id field is required'}, status=400)
        
        user = get_object_or_404(KYCUsers, user_id=user_id)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    