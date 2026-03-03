from django.urls import path
from . import views

app_name = 'central_tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sos/<int:hospital_id>/', views.send_sos, name='send_sos'),
    path(
        'hospital/<int:hospital_id>/',
        views.hospital_detail,
        name='hospital_detail'
    ),
]
