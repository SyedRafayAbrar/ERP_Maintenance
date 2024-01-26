from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .. import serializers
from rest_framework import status
from .. import models
from ..responseGenerator import ResponseGenerator
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserModel(request):
    user = get_object_or_404(User, id=request.data['user_id'])
    if not user:
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    residence = models.Customer_Residence_Status.objects.filter(user_id=user.id).last()
    appartment = models.Appartment_Customer.objects.filter(user_id=user.id).last()
    appartment_serializer = serializers.Appartment_Serializer(appartment.appartment, many=False)
    if token:
        response = {"user_name": user.username, "email": user.email, "residence_status":residence.residence_status.status_name, "appartment_info":appartment_serializer.data}
        return ResponseGenerator(status=status.HTTP_200_OK, data=response).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error="user not found").generate_response()

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getMyTenants(request):
    if 'user_id' in request.data:
        userId = request.data.get('user_id', None)
        appartmentId = request.data.get('appartment_id', None)
        customer_appartments = models.Appartment_Customer.objects.filter(appartment_id=appartmentId).exclude(user_id = userId).values_list('appartment', flat=True)
        print(list(customer_appartments))
        serial = serializers.Appartment_Serializer(customer_appartments, many=True)
        return  ResponseGenerator(status=status.HTTP_200_OK, data=serial.data).generate_response()