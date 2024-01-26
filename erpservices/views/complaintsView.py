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


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllComplaints(request):
    status_id = request.query_params.get('status_id', 0)
    if status_id != 0:
        data = models.Complaints.objects.filter(complaints_current_status_id=status_id)
        serializer = serializers.Complaints_Serializer(data, many=True)
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
    else:
        data = models.Complaints.objects.all()
        serializer = serializers.Complaints_Serializer(data, many=True)
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response() 

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllComplaintsTypes(request):
    data = models.Complaints.objects.all()
    serializer = serializers.Complaints_Status_Type_Serializer(data, many=True)
    return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllComplaintsStatus(request):
    data = models.Complaints.objects.all()
    serializer = serializers.Complaints_Status_Serializer(data, many=True)
    return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getComplaintsSubject(request):
    data = models.Complaints_Subject.objects.all()
    serializer = serializers.Complaints_Subject_Serializer(data, many=True)
    return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def addComplaintsSubject(request):
    serializer = serializers.Complaints_Subject_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def addComplaints(request):
    serializer = serializers.Complaints_Serializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        complaints = models.Complaints.objects.all().last()
        compStatusSerializer = serializers.Complaints_Status_Serializer(data={"status":1, "complaints":complaints.id})
        if compStatusSerializer.is_valid():
            compStatusSerializer.save()
            return ResponseGenerator(status=status.HTTP_200_OK, data=compStatusSerializer.data).generate_response()
        else:
            return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={"error": "compStatusSerializer error"},error=compStatusSerializer.errors).generate_response()    
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={"eeee"},error=serializer.errors).generate_response()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def addComplaintStatusType(request):
    serializer = serializers.Complaints_Status_Type_Serializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def addComplaintStatus(request):
    serializer = serializers.Complaints_Status_Serializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()

@api_view(['POST'])
def updateComplaintStatus(request):
    # data = models.Complaints.objects.all()
    # serializer = serializers.Complaints_Status_Serializer(data, many=True)
    if 'complaint_id' in request.query_params:
        complaint_id = request.query_params['complaint_id']
        Complaint_Info = models.Complaints.objects.get(id=complaint_id)
        if 'status_id' in request.data:
            type = models.Complaints_Status_Types.objects.get(id=request.data['status_id'])
            Complaint_Info.complaints_current_status = type
            Complaint_Info.save()
            
            complaintStatus =  serializers.Complaints_Status_Serializer(data= {"status":type.id, "complaints": complaint_id})
            if complaintStatus.is_valid():
                complaintStatus.save()
            
            return ResponseGenerator(status=status.HTTP_200_OK, data={"message":"status updated"}).generate_response()
        else:
            return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST, data={}, error="invalid status").generate_response()
    else:
        return ResponseGenerator(status=status.HTTP_200_OK, data={"params":"No"}).generate_response()
    

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteComplaint(request):
    try:
        if 'complaint_ids' in request.data:
            complaint_ids = request.data.get('complaint_ids', [])  # Assuming complaint_ids is an array in your request data

        # Use __in to filter complaints based on the list of IDs
            complaints = models.Complaints.objects.filter(id__in=complaint_ids)

            if complaints.exists():
                complaints.delete()
                return ResponseGenerator(status=status.HTTP_200_OK, data={"message":"Complaints Deleted successfully"}).generate_response()
            else:
                return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST, data={}, error="invalid status").generate_response()
        
        if 'complaint_id' in request.data:
            complaint_id = request.data['complaint_id']
            complaint = models.Complaints.objects.get(id = complaint_id)
            if complaint != None:
                complaint.delete()
                return ResponseGenerator(status=status.HTTP_200_OK, data={"message": "Complaint Deleted successfully"}).generate_response()
            else:
                return ResponseGenerator(status=status.HTTP_404_NOT_FOUND,data={},error="No Appartment found").generate_response()
    except Exception as e:
        return ResponseGenerator(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={},error=str(e)).generate_response()
    