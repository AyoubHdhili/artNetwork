from django.urls import path
from . import views

urlpatterns = [

    path('index', views.index, name='index'),
    path('', views.post_list, name='post_list'), 
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('new/', views.post_create, name='post_create'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/edit/', views.post_update, name='post_update'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('categories/', views.category_list, name='category_list'),
]
