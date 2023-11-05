from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualize_data, name='visualize_data'),
]
