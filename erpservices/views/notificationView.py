from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .. import serializers
from rest_framework import status
from .. import models
from ..responseGenerator import ResponseGenerator


@api_view(['GET'])
def getAllNotifications(request):
    data = models.NotificationModel.objects.all()
    serializer = serializers.Notification_Serializer(data, many=True)
    return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()

@api_view(['POST'])
def addNotifications(request):
    serializer = serializers.Notification_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()
    

@api_view(['POST'])
def addNotificationType(request):
    serializer = serializers.Notification_Type_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()