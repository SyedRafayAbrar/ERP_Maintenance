from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .. import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from .. import models
from ..responseGenerator import ResponseGenerator
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def login(request):
    # user = get_object_or_404(User, username=request.data['username'])
    user = User.objects.filter(username=request.data['username']).last()
    if user == None:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error="User Not Found").generate_response()
    if not user.check_password(request.data['password']):
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error="Password incorrect").generate_response()
    token, created = Token.objects.get_or_create(user=user)
    roleUser = models.Roles_Users.objects.filter(user=user).last()
    Role_UserSerializer = serializers.Display_Role_UserSerializer(roleUser)
    resp = {"id":user.id,"user_name": user.username, "email": user.email, "token":token.key, "user_role":Role_UserSerializer.data}
    return ResponseGenerator(status=status.HTTP_200_OK, data=resp).generate_response()
    # return Response({'token': token.key, 'user': serializer.data})

@api_view(['POST'])
def logOut(request):
    user = User.objects.filter(id=request.data['user_id']).last()
    print(user)
    if user == None:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error="User Not Found").generate_response()
    
    token = Token.objects.get(user=user)
    if token == None:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error="Token Not Found").generate_response()
    token.delete()
    return ResponseGenerator(status=status.HTTP_200_OK).generate_response()

@api_view(['POST'])
def signUp(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        resp = {"id":user.id,"user_name": user.username, "email": user.email, "token":token.key}
        return ResponseGenerator(status=status.HTTP_200_OK,data=resp).generate_response()
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()
             
    return Response({})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


@api_view(['POST'])
def addRole(request):
    serializer = serializers.RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()
    
    
@api_view(['GET'])
def getRoles(request):
    data = models.Roles.objects.all()
    serializer = serializers.RoleSerializer(data, many=True)
    return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()

@api_view(['POST'])
def assignRoles(request):
    serializer = serializers.Role_UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()

@api_view(['POST'])
def createInviteCode(request):
    serializer = serializers.Invite_Code_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()
    
@api_view(['POST'])
def assignInviteCode(request):
    serializer = serializers.Assign_Invite_Code_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()

@api_view(['POST'])
def assignUserToAdmin(request):
    userId = request.data['user_id']
    code = request.data['invitation_code']
    getInvitationCode = models.Invite_Code.objects.filter(unique_identifier=code).first()
    if getInvitationCode == None:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,
                                 data={},
                                 error="Code does not exist").generate_response()
    else:
        adminCodeModel = models.Invite_Code_User.objects.filter(invite_code = getInvitationCode.id).first()
        serializerObj = {"_admin":adminCodeModel.user.id, "_customer": userId}
        obj = {"user": userId, "role": 4}
        roleSerializer = serializers.Role_Post_UserSerializer(data=obj)
        serializer = serializers.Assign_Admin_Customer_Serializer(data=serializerObj)
        if serializer.is_valid() and roleSerializer.is_valid():
            serializer.save()
            roleSerializer.save()
            return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
        else:
            return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()

@api_view(['POST'])
def addResidenceStatus(request):
    serializer = serializers.Residence_Status_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def assignResidenceStatus(request):
    serializer = serializers.Customer_Residence_Status_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ResponseGenerator(status=status.HTTP_200_OK, data=serializer.data).generate_response()
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=serializer.errors).generate_response()


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadImage(request):
    userId = request.user.id
    imageModel = {'image': request.data['image'], 'name': request.data['name']}
    imageSerializer = serializers.Image_Serializer(data=imageModel)
    if imageSerializer.is_valid():
        imageSerializer.save()
        latestIMage = models.ImagesModel.objects.all().last()
        userModel = {'image': latestIMage.id, 'user': userId}
        imageUserSerializer = serializers.Image_User_Post_Serializer(data=userModel)
        if imageUserSerializer.is_valid():
            imageUserSerializer.save()
            imageLastmodel = models.Image_User.objects.last()
            imageLastmodelSer = serializers.Image_User_Serializer(imageLastmodel)
            return ResponseGenerator(status=status.HTTP_200_OK, data=imageLastmodelSer.data).generate_response()    
        else:
            return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=imageUserSerializer.errors).generate_response()
        
        
    else:
        return ResponseGenerator(status=status.HTTP_400_BAD_REQUEST,data={},error=imageUserSerializer.errors).generate_response()
    

