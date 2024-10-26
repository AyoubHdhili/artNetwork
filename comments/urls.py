# urls.py
from django.urls import path
from . import views

urlpatterns = [
      path('add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
   path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]