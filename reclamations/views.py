# reclamation/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reclamation, Response
from .forms import ReclamationForm, ResponseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View
import os
from transformers import pipeline
from django.conf import settings
import requests  

class UserReclamationListView(LoginRequiredMixin, ListView):
    model = Reclamation
    template_name = 'reclamations/user_reclamations.html'
    context_object_name = 'reclamations'

    def get_queryset(self):
        return Reclamation.objects.filter(author=self.request.user).order_by('-created_at')

@login_required
def create_reclamation(request):
    if request.method == 'POST':
        form = ReclamationForm(request.POST)
        if form.is_valid():
            reclamation = form.save(commit=False)
            reclamation.author = request.user
            reclamation.save()
            return redirect('user-reclamations')
    else:
        form = ReclamationForm()
    return render(request, 'reclamations/create.html', {'form': form})

def reclamation_list(request):
    reclamations = Reclamation.objects.all()
    return render(request, 'reclamations/support_index.html', {'reclamations': reclamations})

def reclamation_detail(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk)
    return render(request, 'reclamation/detail.html', {'reclamation': reclamation})

def update_reclamation(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk)
    if request.method == 'POST':
        form = ReclamationForm(request.POST, instance=reclamation)
        if form.is_valid():
            form.save()
            return redirect('reclamation_list')
    else:
        form = ReclamationForm(instance=reclamation)
    return render(request, 'reclamation/update.html', {'form': form})

def delete_reclamation(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk)
    reclamation.delete()
    return redirect('reclamation_list')


def respond_reclamation(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk)
    responses = Response.objects.filter(reclamation=reclamation)

    suggestion = None
    if request.method == 'POST':
        if "generate_response" in request.POST:
            # Generate the suggested response
            suggestion = generate_response_suggestion(reclamation.description)
        elif "submit_response" in request.POST:
            # Handle actual response submission
            content = request.POST.get("content")
            if content:
                Response.objects.create(reclamation=reclamation, content=content)
                reclamation.status = 'solved'
                reclamation.save()
                messages.success(request, "Response submitted successfully.")
                return redirect('respond_reclamation', pk=reclamation.pk)
            else:
                messages.error(request, "Content cannot be empty.")

    return render(request, 'reclamations/respond.html', {
        'reclamation': reclamation,
        'suggestion': suggestion,
        'responses': responses
    })

def generate_response_suggestion(description):
    # Hugging Face API URL for gpt-neo-2.7B text generation
    model_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    
    # Headers with Hugging Face API token
    headers = {
        "Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}"
    }
    prompt = "provide answer for this question : "+ description
    # Payload for the API request
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 50,
            "num_return_sequences": 1,
            "temperature": 0.7,  # Adjust for creativity
            "top_p": 0.9  # Adjust for diversity
        }
    }

    try:
        # Make the API request
        response = requests.post(model_url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            if result and isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'No suggestion available.')
        else:
            # Log or print error details for debugging
            print(f"Error {response.status_code}: {response.json()}")

    except requests.exceptions.RequestException as e:
        # Handle request exceptions and print error
        print(f"Request failed: {e}")

    return "Unable to generate response suggestion."