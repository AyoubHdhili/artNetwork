from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('reserver/<int:event_id>/', views.create_reservation, name='create_reservation'),
    path('cancel_reservation/<int:participation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('user_participations/', views.user_participations, name='user_participations'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)