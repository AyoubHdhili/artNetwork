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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Reclamation, Response
from .forms import ReclamationForm, ResponseForm
from transformers import pipeline

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
    # Set your Hugging Face token
    os.environ["HUGGINGFACE_TOKEN"] = "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"
    
    # Initialize the pipeline
    pipe = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct")
    
    # Generate response suggestion
    suggestion = pipe(description, max_length=50, num_return_sequences=1)
    return suggestion[0]['generated_text']
