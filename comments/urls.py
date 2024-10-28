# urls.py
from django.urls import path
from . import views

urlpatterns = [
      path('add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
   path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('suggestions2/<int:post_id>/', views.get_ai_suggestions2, name='get_suggestions2'),
        path('suggestions/<int:post_id>/', views.get_ai_suggestions3, name='get_suggestions'),
           path('replies/add/<int:comment_id>/', views.add_reply, name='add_reply'),
               path('replies/<int:reply_id>/edit/', views.edit_reply, name='edit_reply'),
    path('replies/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
      path('generatecomment/<int:post_id>/', views.get_ai_comment_suggestions, name='get_suggestions5'),

       
      
]