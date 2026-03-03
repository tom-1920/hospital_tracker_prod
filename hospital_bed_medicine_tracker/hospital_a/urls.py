from django.urls import path
from .views import update_availability, clear_sos
from . import views

urlpatterns = [
    path('', update_availability, name='hospital_a_update'),
    path('clear-sos/', clear_sos, name='hospital_a_clear_sos'),
    path('check-sos/', views.check_sos, name='check_sos')
    
]
