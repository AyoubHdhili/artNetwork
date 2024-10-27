from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventAddForm, EventUpdateForm
from django.contrib import messages
from django.conf import settings
from Participation.models import Participation 
from django.http import JsonResponse
import requests
import base64
import os
from django.core.files.storage import default_storage
from django.utils import timezone

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
    current_date = timezone.now().date()
    reserved_event_ids = set(
        Participation.objects.filter(user=request.user).values_list('event_id', flat=True)
    )
    
    for event in events:
        event.is_reserved = event.id in reserved_event_ids
        event.is_owner = event.creator.id == request.user.id

    return render(request, 'event_list.html', {
        'events': events,
        'MEDIA_URL': settings.MEDIA_URL ,
        'current_date': current_date 
    })


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_owner = event.creator.id == request.user.id  

    
    participation = Participation.objects.filter(user=request.user, event=event).first()
    
    is_reserved = participation is not None
    participation_id = participation.id if participation else None
    
    creator = event.creator  
    participant_count = event.participations.count()
    
    return render(request, 'event_detail.html', {
        'event': event,
        'creator': creator, 
        'is_owner': is_owner,
        'is_reserved': is_reserved,
        'participation_id': participation_id,
        'participant_count': participant_count,
        'MEDIA_URL': settings.MEDIA_URL
    })

@login_required
def generate_image(request):
    if request.method == 'POST':
      
        prompt = request.POST.get('prompt')
        if not prompt:
            return JsonResponse({'error': 'Prompt text is required'}, status=400)

        headers = {
            'Authorization': f'Bearer {settings.HUGGING_FACE_API_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'inputs': prompt,
        }

       
        response = requests.post(settings.STABLE_DIFFUSION_URL, headers=headers, json=data)

        if response.status_code == 200:
           
            image_data = response.content  
            image_url = "data:image/png;base64," + base64.b64encode(image_data).decode()

            return JsonResponse({'image_url': image_url})
        else:
            return JsonResponse({'error': 'Error generating image'}, status=response.status_code)

    return render(request, 'generate_image.html')


