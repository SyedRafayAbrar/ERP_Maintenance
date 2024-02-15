from django.urls import re_path
from .views import views,appartmentView, notificationView, customerViews, complaintsView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path('add_appartment', appartmentView.addAppartment),
    re_path('delete_appartment', appartmentView.deleteAppartment),
    re_path('update_appartment', appartmentView.updateAppartment),
    re_path('get_appartment', appartmentView.getAppartments),
    re_path('add_status', appartmentView.addStatusAppartment),
]