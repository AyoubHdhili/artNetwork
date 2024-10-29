from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)
from transformers import T5ForConditionalGeneration, T5Tokenizer

tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")

def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    users = User.objects.all()
    groups = ChatGroup.objects.filter(models.Q(members=request.user) | models.Q(admin=request.user), is_private= False)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    form_edit = ChatGroupEditForm(instance=chat_group)
    
    

    if request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {'message': message, 'user': request.user}
            return render(request, 'chat/chat_message_p.html', context)

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'form_edit': form_edit,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group,
        'users': users,
        'groups': groups
    }
    return render(request, 'chat/chat.html', context)

def private_chat(request, user_id):
    users = User.objects.all()
    other_user = get_object_or_404(User, id=user_id)
    groups = ChatGroup.objects.filter(models.Q(members=request.user) | models.Q(admin=request.user), is_private= False)
    sorted_ids = sorted([request.user.id, other_user.id])
    group_name = f"private_{sorted_ids[0]}_{sorted_ids[1]}"

    chatroom, created = ChatGroup.objects.get_or_create(
        group_name=group_name,
        defaults={'is_private': True},
    )
    if created:
        chatroom.members.add(request.user, other_user)

    chat_messages = chatroom.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'user': other_user,
        'chatroom_name': group_name,
        'users': users,
        'groups': groups,
    }
    return render(request, 'chat/chat.html', context)

def user_status(request):
    users = User.objects.all()
    groups = ChatGroup.objects.filter(models.Q(members=request.user) | models.Q(admin=request.user), is_private= False).distinct()
    return render(request, 'chat/user_status.html', {'users': users, 'groups': groups})

def create_groupchat(request):
    if request.method == 'POST':
        form = ChatGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group chat created successfully!')  # Success message
            return redirect('new-groupchat')
        else:
            messages.error(request, 'There was an error creating the group chat. Please try again.')
    else:
        form = ChatGroupForm()

    return render(request, 'chat/new_groupchat.html', {'form': form})

def group_chat_view(request, group_id):
    chat_group = get_object_or_404(ChatGroup, id=group_id)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chatroom_name': chat_group.group_name,
        'group': chat_group
    }
    return render(request, 'chat/group_chat.html', context)

def edit_chatgroup(request, group_id):
    chat_group = get_object_or_404(ChatGroup, id=group_id)
    
    if request.method == 'POST':
        form = ChatGroupEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            updated_chat_group = form.save()
            updated_chat_group.members.set(form.cleaned_data['members'])
            return redirect('chat', chatroom_name='public-chat')
    else:
        form = ChatGroupEditForm(instance=chat_group)
    
    context = { 
        'chatroom_name': 'public-chat'
    }
    return render(request, 'chat/chat.html', context)


def delete_chatgroup(request, group_id):
    chat_group = get_object_or_404(ChatGroup, id=group_id)

    if request.method == 'POST':
        if request.user == chat_group.admin:
            chat_group.delete()
            messages.success(request, "Group deleted successfully.")
            return redirect('chat', chatroom_name='public-chat')
        else:
            messages.error(request, "You do not have permission to delete this group.")
            return redirect('chat', chatroom_name=chat_group.group_name)

def translate_message(request, message_id):
    if request.method == 'POST':
        message = GroupMessage.objects.get(id=message_id) 
        input_text = f"translate English to French: {message.body}"

        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f'Translated Text: {translated_text}')
        # Store the translated text in a session
        request.session['translated_text'] = translated_text

        html_response = f"""
            <div class="translation">
                <p>Translation: {request.session['translated_text']}</p>
            </div>
            """
    
        return HttpResponse(html_response, content_type="text/html")  # Replace with actual chat room name

    return JsonResponse({'error': 'Invalid request method'}, status=400)