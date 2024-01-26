

from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .. import serializers
from rest_framework import status
from .. import models
from ..responseGenerator import ResponseGenerator

@api_view(['GET'])
def getAppartments(request):
    data = models.Appartment_Info.objects.all()
    serializer = serializers.Appartment_Serializer(data, many=True)
    return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def addAppartment(request):
    unit_no = request.data['unit_no']
    block_no = request.data['block_no']
    remaining_address = request.data['remaining_address']
    user = request.data['user_id']
    app_serializer = serializers.Appartment_Serializer(data={"unit_no": unit_no, "block_no": block_no, "remaining_address": remaining_address})
    if app_serializer.is_valid():
        app_serializer.save()
        appartment = models.Appartment_Info.objects.all().last()
        appSer = serializers.Appartment_User_Serializer(data={"user": user, "appartment": appartment.id})
        if appSer.is_valid():
            appSer.save()
            
            return ResponseGenerator(status=status.HTTP_200_OK, data={"message": "Appartment added successfully"}).generate_response()
        else:
            return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=appSer.errors).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=app_serializer.errors).generate_response()
    
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteAppartment(request):
    
    appt_id = request.data['appartment_id']
    appartment = models.Appartment_Info.objects.filter(id = appt_id).first()
    if appartment != None:
        appartment.delete()
        return ResponseGenerator(status=status.HTTP_200_OK, data={"message": "Appartment Deleted successfully"}).generate_response()
    else:
        return ResponseGenerator(status=status.HTTP_404_NOT_FOUND,data={},error="No Appartment found").generate_response()

    
@api_view(['PUT'])  # You can also use ['PATCH'] depending on your use case
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateAppartment(request):
    appt_id = request.data['appartment_id']
    try:
        Appartment_Info = models.Appartment_Info.objects.get(id=appt_id)
    except Appartment_Info.DoesNotExist:
        return ResponseGenerator(status=status.HTTP_404_NOT_FOUND, data={}, error="No Appartment found").generate_response()

    # Assuming you have fields like 'name' and 'description' in your model
    if 'unit_no' in request.data:
        Appartment_Info.unit_no = request.data['unit_no']
    if 'block_no' in request.data:
        Appartment_Info.block_no = request.data['block_no']
    if 'remaining_address' in request.data:
        Appartment_Info.remaining_address = request.data['remaining_address']

    # Add more fields as needed

    Appartment_Info.save()

    return ResponseGenerator(status=status.HTTP_200_OK, data={"message": "Appartment updated successfully"}).generate_response()