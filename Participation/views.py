from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from events.models import Event
from .models import Participation
from django.utils import timezone
from django.contrib import messages
from django.utils import timezone

@login_required
def create_reservation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if event.max_participants <= 0:
        messages.error(request, "No available places for this event.")
        return redirect('event_list')
    
    event.max_participants -= 1
    event.save()

    participation = Participation()
    participation.event = event
    participation.user = request.user  
    participation.participation_date = timezone.now()
    participation.save()

    messages.success(request, "Reservation successfully created.")
    return redirect('event_list')

@login_required
def cancel_reservation(request, participation_id):
    
    participation = get_object_or_404(Participation, id=participation_id)
    event = participation.event
    event.max_participants += 1
    event.save()
    participation.delete()
    
    return redirect('event_list')
@login_required
def user_participations(request):
    current_date = timezone.now().date()
    participations = Participation.objects.filter(user=request.user).select_related('event__creator')

    return render(request, 'user_participations.html', {
        'participations': participations,
        'current_date': current_date 
    })
