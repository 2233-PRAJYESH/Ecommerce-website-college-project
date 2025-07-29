from .import views
from django.urls import path

app_name = 'chat'

urlpatterns = [
    # URLs to handle 1-1 chats
    path('', views.index, name='chat'),
    path('<str:room_name>/', views.room, name='room'),

    # URLs to handle group chats
    path('group/chat/', views.group_chat, name='group_chat'),
    path('group/chat/<str:group_name>/', views.group_chat, name='group_chat'),
    path('api/creategroup/', views.create_group),
]