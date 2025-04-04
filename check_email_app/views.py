from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

class CheckUserExists(APIView):
    
    def get(self,request):
        User = get_user_model();
        email=request.query_params.get('email')
        if not email:
            return Response({'error': 'Email erforderlich'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'exists':True}, status=status.HTTP_200_OK)
        return Response({'exists':False},status=status.HTTP_200_OK)


