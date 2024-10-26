from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventAddForm, EventUpdateForm
from django.contrib import messages
from django.conf import settings
from Participation.models import Participation 

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventAddForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user  
            event.save()
            messages.success(request, "L'événement a été créé avec succès.")
            return redirect('event_list') 
    else:
        form = EventAddForm()
    
    return render(request, 'add_event.html', {
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL  
    })

@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventUpdateForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "L'événement a été mis à jour avec succès.")
            return redirect('event_detail', event_id=event.id) 
    else:
        form = EventUpdateForm(instance=event)

    return render(request, 'update_event.html', {
        'form': form,
        'event': event,
        'MEDIA_URL': settings.MEDIA_URL  
    })

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, "L'événement a été supprimé avec succès.")
        return redirect('event_list') 
    
    return redirect('event_list') 

@login_required
def event_list(request):
    events = Event.objects.select_related('creator').all()  
    return render(request, 'event_list.html', {
        'events': events,
        'MEDIA_URL': settings.MEDIA_URL  
    })

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_owner = event.creator.id == request.user.id  

   
    creator = event.creator  
    participant_count = event.participations.count()
    return render(request, 'event_detail.html', {
        'event': event,
        'creator': creator, 
        'is_owner': is_owner,
        'participant_count': participant_count,
        'MEDIA_URL': settings.MEDIA_URL
    })
