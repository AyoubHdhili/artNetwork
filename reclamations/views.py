# reclamation/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reclamation
from .forms import ReclamationForm

# Create a new reclamation
def create_reclamation(request):
    if request.method == 'POST':
        form = ReclamationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reclamation_list')
    else:
        form = ReclamationForm()
    return render(request, 'reclamations/create.html', {'form': form})

# List all reclamations
def reclamation_list(request):
    reclamations = Reclamation.objects.all()
    return render(request, 'reclamation/list.html', {'reclamations': reclamations})

# View a single reclamation
def reclamation_detail(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk)
    return render(request, 'reclamation/detail.html', {'reclamation': reclamation})

# Update an existing reclamation
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

# Delete a reclamation
def delete_reclamation(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk)
    if request.method == 'POST':
        reclamation.delete()
        return redirect('reclamation_list')
    return render(request, 'reclamation/delete.html', {'reclamation': reclamation})
