from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.event_list, name="event_list"),
    path('add/', views.create_event, name='addevent'),
    path('update/<int:event_id>/', views.update_event, name='updateevent'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('detail/<int:event_id>/', views.event_detail, name='event_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)