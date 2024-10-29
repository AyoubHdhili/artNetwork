from django.urls import path
from .views import *

urlpatterns = [
    path('privatechat/<int:user_id>/', private_chat, name='private_chat'),
    path('user-status/', user_status, name='user_status'),
    path('chatgroup/edit/<int:group_id>/', edit_chatgroup, name='edit_chatgroup'),
    path('chatgroup/delete/<int:group_id>/', delete_chatgroup, name='delete_chatgroup'),
    path('new-groupchat/', create_groupchat, name="new-groupchat"),
    path('group-chat/<int:group_id>/', group_chat_view, name='group_chat'),
    path('translate-message/<int:message_id>/', translate_message, name='translate_message'),
    path('<str:chatroom_name>/', chat_view, name='chat'),
]
