# urls.py

from django.urls import path
from . import views

urlpatterns = [
   #path('chat/', views.chat_view , name='chat_view'),
    path('whatsapp', views.verify_token , name='whatsapp'),
    path('receive', views.receive_message , name='receive'),
]
