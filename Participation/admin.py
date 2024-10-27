from django.contrib import admin
from .models import Event,Participation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'max_participants', 'creator')
    list_filter = ('start_date', 'max_participants')
    search_fields = ('title', 'description')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'participation_date')
    list_filter = ('participation_date',)
    search_fields = ('user__username', 'event__title')