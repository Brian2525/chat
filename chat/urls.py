from django.urls import path
from .import views

urlpatterns = [
    path('', views.visitor_info, name='visitor_info'),
    path('chat/', views.chat, name='chat'),
]