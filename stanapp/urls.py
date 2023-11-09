from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.visualize_data, name='visualize_data'),
    path('predict_range/', csrf_exempt(views.predict_range), name='predict_range'),
    path('customdata/', csrf_exempt(views.empty_view), name='custom_data'),
]
