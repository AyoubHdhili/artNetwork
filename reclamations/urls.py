# reclamation/urls.py
from django.urls import path
from . import views
from .views import UserReclamationListView

urlpatterns = [
    path('', views.reclamation_list, name='reclamation_list'),
    path('create/', views.create_reclamation, name='create_reclamation'),
    path('<int:pk>/', views.reclamation_detail, name='reclamation_detail'),
    path('my-reclamations/', UserReclamationListView.as_view(), name='user-reclamations'),
    path('support/',views.reclamation_list, name='support'),
    path('respond/<int:pk>/', views.respond_reclamation, name='respond_reclamation'),
    path('delete/<int:pk>/',  views.delete_reclamation, name='delete_reclamation'),


]
