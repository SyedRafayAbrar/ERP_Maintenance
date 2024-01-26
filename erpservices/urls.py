from django.urls import re_path
from .views import views,appartmentView, notificationView, customerViews, complaintsView

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signUp),
    re_path('logout', views.logOut),
    re_path('test_token', views.test_token),
    re_path('get_roles', views.getRoles),
    re_path('add_role', views.addRole),
    re_path('assign_role', views.assignRoles),
    re_path('add_invite_code', views.createInviteCode),
    re_path('assign_invite_code', views.assignInviteCode),
    re_path('assign_user_admin', views.assignUserToAdmin),
    
    re_path('add_appartment', appartmentView.addAppartment),
    re_path('delete_appartment', appartmentView.deleteAppartment),
    re_path('update_appartment', appartmentView.updateAppartment),
    re_path('get_appartment', appartmentView.getAppartments),
    
    re_path('add_residence_status', views.addResidenceStatus),
    re_path('assign_residence_status', views.assignResidenceStatus),
    re_path('get_my_tenants', customerViews.getMyTenants),
    
    re_path('get_user_model', customerViews.getUserModel),
    
    re_path('add_notification_type', notificationView.addNotificationType),
    re_path('add_notification', notificationView.addNotifications),
    
    re_path('update_complaints_status', complaintsView.updateComplaintStatus),
    re_path('get_complaints', complaintsView.getAllComplaints),
    re_path('add_complaint_subject', complaintsView.addComplaintsSubject),
    re_path('add_complaints', complaintsView.addComplaints),
    re_path('add_complaint_status_type', complaintsView.addComplaintStatusType),
    re_path('add_complaint_status', complaintsView.addComplaintStatus),
    re_path('delete_complaint', complaintsView.deleteComplaint),
    re_path('delete_all_complaints', complaintsView.deleteAllComplaint),
]