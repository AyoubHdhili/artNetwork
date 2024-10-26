from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="created_events"
    )
    max_participants = models.PositiveIntegerField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  

    def __str__(self):
        return self.title

    @property
    def participants_count(self):
        return self.participations.count()
