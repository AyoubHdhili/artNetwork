from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
]