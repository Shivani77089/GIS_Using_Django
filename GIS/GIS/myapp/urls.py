from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('get_new_notifications/', views.get_new_notifications, name='get_new_notifications'),
    ]




