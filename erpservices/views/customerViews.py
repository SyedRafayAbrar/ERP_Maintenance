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
from .views import uploadImage
from ..helper import adapt_drf_request_to_django


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
    
    userInfo = models.UserInformation.objects.get(user_id=user.id)
    userInfoSerialzer = serializers.User_Info_Serializer(userInfo)
    
    appartment_serializer = serializers.Appartment_Serializer(appartment.appartment, many=False)
    if token:
        response = {"id":user.id,"user_name": user.username, "email": user.email, "residence_status":residence.residence_status.status_name, "appartment_info":appartment_serializer.data, "user_info":userInfoSerialzer.data}
        return ResponseGenerator(status=status.HTTP_200_OK, data=response).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error="user not found").generate_response()

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getMyAppartments(request):
    
    userId = request.user.id
        
    if 'appartment_id' not in request.data: 
        apartments = models.Appartment_Customer.objects.filter(user_id=userId)
        apparmtmentArray = [apartment_customer.appartment for apartment_customer in apartments]
        # apparmtmentUserArray = [apartment_customer.user for apartment_customer in apartments]
        responseModel = []
        for appartment in apparmtmentArray:
            customerResidence = models.Appartment_Residence_Status.objects.get(appartment=appartment)
            appartmentSerialiser = serializers.Appartment_Serializer(appartment)
            appartmentResident = models.AppartmentResident.objects.get(appartment=appartment)
            userInfo = models.UserInformation.objects.get(user=appartmentResident.user)
            userInfoSerial = serializers.User_Info_Serializer(userInfo)
            responseModel.append({'appartment': appartmentSerialiser.data, 'residence_status': customerResidence.residence_status.status_name, 'resident_info': userInfoSerial.data})
                
        return  ResponseGenerator(status=status.HTTP_200_OK, data=responseModel).generate_response()
        
        
    appartmentId = request.data.get('appartment_id', None)
    customer_appartments = models.Appartment_Customer.objects.filter(appartment_id=appartmentId).exclude(user_id = userId).values_list('appartment', flat=True)
    # print(list(customer_appartments.count))
    serial = serializers.Appartment_Serializer(customer_appartments, many=True)
    return  ResponseGenerator(status=status.HTTP_200_OK, data=serial.data).generate_response()
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def assignUserInfoToUser(request):
    userId = request.user.id
    serializer = serializers.User_Info_Serializer(data={'user': userId})
    if serializer.is_valid():
        serializer.save()
        return  ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
    else:
        return  ResponseGenerator(status=status.HTTP_200_OK, data={}, error=serializer.error_messages).generate_response()
    
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUserInfo(request):
    userId = request.user.id
    userInfoModel = models.UserInformation.objects.get(user_id=userId)
    
    if 'image' in request.data:
            imageModel = {'image': request.data['image'], 'name': 'profile_image'}
            imageSerializer = serializers.Image_Serializer(data=imageModel)
            if imageSerializer.is_valid():
                imageSerializer.save()
                latestIMage = models.ImagesModel.objects.all().last()
                userModel = {'image': latestIMage.id, 'user': userId}
                imageUserSerializer = serializers.Image_User_Post_Serializer(data=userModel)
                if imageUserSerializer.is_valid():
                    imageUserSerializer.save()
                    imageLastmodel = models.Image_User.objects.last()
                    userInfoModel.profileImage = imageLastmodel
                    userInfoModel.save()
                    return ResponseGenerator(status=status.HTTP_200_OK, data={"message": "User Updated Successfully"}).generate_response()
    else:
    
        if 'contact_number' in request.data:
            userInfoModel.contact_number = request.data['contact_number']
        if 'family_members_count' in request.data:
            userInfoModel.family_members_count = request.data['family_members_count']
    
    userInfoModel.save()
    
    return ResponseGenerator(status=status.HTTP_200_OK, data={"message": "User Updated Successfully"}).generate_response()
    