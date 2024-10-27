# reclamation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.reclamation_list, name='reclamation_list'),
    path('create/', views.create_reclamation, name='create_reclamation'),
    path('<int:pk>/', views.reclamation_detail, name='reclamation_detail'),
    path('<int:pk>/update/', views.update_reclamation, name='update_reclamation'),
    path('<int:pk>/delete/', views.delete_reclamation, name='delete_reclamation'),
]
