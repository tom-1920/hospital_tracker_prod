from django.urls import path
from .views import update_availability, clear_sos
from . import views

urlpatterns = [
    path('', update_availability, name='hospital_c_update'),
    path('clear-sos/', clear_sos, name='hospital_c_clear_sos'),
]
