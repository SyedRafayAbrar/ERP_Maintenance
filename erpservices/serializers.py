from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Roles
        fields = "__all__"
        
class Role_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Roles_Users
        fields = "__all__"
        depth = 1

class Role_Post_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Roles_Users
        fields = "__all__"
        
class Display_Role_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Roles_Users
        fields = ["id",'role']
        depth = 1   
        
class  Invite_Code_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Invite_Code
        fields = "__all__"                


class  Assign_Invite_Code_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Invite_Code_User
        fields = "__all__"                


class  Assign_Admin_Customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin_Customer
        fields = "__all__"
        
class  Appartment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appartment_Info
        fields = "__all__"
        
        
class  Appartment_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appartment_Customer
        fields = "__all__"
        
class  Notification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationModel
        fields = "__all__"
        depth = 1
        
        
class  Notification_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification_Type
        fields = "__all__"
        
class  Residence_Status_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Residence_Status
        fields = "__all__"
        
class  Customer_Residence_Status_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer_Residence_Status
        fields = "__all__"
        
class  Complaints_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaints
        fields = "__all__"
        depth = 1
        
class  Complaints_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaints_User
        fields = "__all__"
        
class  Complaints_Subject_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaints_Subject
        fields = "__all__"
        
class  Complaints_Status_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaints_Status
        fields = "__all__"
        
class  Complaints_Status_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaints_Status_Types
        fields = "__all__"
        
class  Image_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImagesModel
        fields = "__all__"
        
class  Image_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image_User
        fields = ["image"]
        depth = 1
        
class  Image_User_Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image_User
        fields = "__all__"
        
class  User_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInformation
        fields = "__all__"
        
                     
class  Appartment_Residence_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appartment_Residence_Status
        fields = "__all__"
        