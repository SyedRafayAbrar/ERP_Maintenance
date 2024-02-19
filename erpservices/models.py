from django.db import models
from django.contrib.auth.models import User
import secrets
import string
from django.utils import timezone
# Create your models here.

class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100); 
    role_display_name = models.CharField(max_length=100, default = ''); 
    
    class Meta:
        db_table = "roles"
        
class Roles_Users(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "roles_users"
        
class Admin_Customer(models.Model):
    id = models.AutoField(primary_key=True)
    _admin = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='admin_customer_admin_set')
    _customer = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='admin_customer_customer_set')
    
    class Meta:
        db_table = "admin_customer"

class PaymentsType(models.Model):
    id = models.AutoField(primary_key=True)
    uName = models.CharField(max_length=100)
    
    class Meta:
        db_table = "payment_type"
        
class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    payment_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=None)
    payment_type = models.ForeignKey(PaymentsType, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = "payments"
        
class Invite_Code(models.Model):
    
    def generate_random_string():
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    id = models.AutoField(primary_key=True)
    unique_identifier = models.CharField(max_length=5, default=generate_random_string)
    
    class Meta:
        db_table = "invite_code"
        
class Invite_Code_User(models.Model):
    
    id = models.AutoField(primary_key=True)
    invite_code = models.ForeignKey(Invite_Code, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "invite_code_user"
        
class Appartment_Info(models.Model):
    
    id = models.AutoField(primary_key=True)
    unit_no = models.CharField(max_length=100)
    block_no = models.CharField(max_length=100)
    remaining_address = models.CharField(max_length=100, default="")
    
    class Meta:
        db_table = "appartment_info"


class Appartment_Customer(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    appartment = models.ForeignKey(Appartment_Info, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "appartment_customer"

class Notification_Type(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "notification_type"
        
class NotificationModel(models.Model):
    
    id = models.AutoField(primary_key=True)
    notification_message = models.CharField(max_length=100)
    notification_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='created_by_set')
    notification_type = models.ForeignKey(Notification_Type, on_delete=models.CASCADE, default=None)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='receiver_set', null=True, blank=True)
    
    class Meta:
        db_table = "notification"
        
class Residence_Status(models.Model):
    id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "residence_status"

class Customer_Residence_Status(models.Model):
    id = models.AutoField(primary_key=True)
    residence_status = models.ForeignKey(Residence_Status, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "customer_residence_status"
        
class Appartment_Residence_Status(models.Model):
    id = models.AutoField(primary_key=True)
    residence_status = models.ForeignKey(Residence_Status, on_delete=models.CASCADE, default=None)
    appartment = models.ForeignKey(Appartment_Info, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "appartment_residence_status"
        
class AppartmentResident(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    appartment = models.ForeignKey(Appartment_Info, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "appartment_resident"

class Complaints_Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    subject_desc = models.CharField(max_length=100, null=True, blank=True, default= None)
    
    class Meta:
        db_table = "complaints_subject"
        
        
class Complaints_Status_Types(models.Model):
    id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "complaints_status_types"
        
class Complaints(models.Model):
    id = models.AutoField(primary_key=True)
    complaints_subject = models.CharField(max_length=100)
    complaints_body = models.CharField(max_length=100, null=True)
    complaints_current_status = models.ForeignKey(Complaints_Status_Types, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "complaints"
        

class Complaints_User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    complaints = models.ForeignKey(Complaints, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "complaints_user"
        
class Complaints_Status(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.ForeignKey(Complaints_Status_Types, on_delete=models.CASCADE, default=None)
    complaints = models.ForeignKey(Complaints, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "complaints_status"
        
class ImagesModel(models.Model):
    # Your existing fields...
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
    # New image field
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    class Meta:
        db_table = "images_model"
        

class Image_User(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ForeignKey(ImagesModel, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    class Meta:
        db_table = "image_user"
        

class UserInformation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    contact_number = models.CharField(max_length=100, default = None, blank = True, null = True)
    family_members_count = models.IntegerField( default = None,blank = True, null = True)
    profileImage = models.ForeignKey(Image_User, on_delete=models.CASCADE, default=None, blank = True, null = True)
    
    class Meta:
        db_table = "user_information"