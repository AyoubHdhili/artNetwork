# comments/views.py
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .models import Comment,Reply
from .forms import CommentForm
from posts.models import Post  # Import Post model from posts app to reference it in this file
from django.http import JsonResponse

import random
from transformers import AutoProcessor, BlipForConditionalGeneration  
import torch
from PIL import Image
from io import BytesIO
import logging

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Return a JSON response with the new comment details
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,  # Include the ID of the new comment
                'author': comment.author.fullname,
                'content': comment.content,
                'created_at': comment.created_at.isoformat()
            })
        else:
            # If the form is invalid, return an error message
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # If the request method is not POST, you can return a different response
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403) 

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            # Return a JSON response indicating success
            return JsonResponse({
                'success': True,
                'content': comment.content,
                'created_at': comment.created_at.isoformat()
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # For GET requests, send the existing comment data to the form
    form = CommentForm(instance=comment)
    return render(request, 'comments/edit_comment.html', {'form': form, 'comment': comment})

logger = logging.getLogger(__name__)
@login_required
def get_ai_suggestions(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    # Call the AI API (e.g., OpenAI) with a general comment suggestion prompt
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",  # Use the chat completions endpoint for GPT-4
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
            json={
                "model": "gpt-3.5-turbo",  # Use the new model name
                "messages": [
                    {"role": "user", "content": "Suggest some engaging comments for a social media post."}
                ],
                "max_tokens": 50,  # Limit the length of the generated comments
                "n": 3,  # Generate 3 different suggestions
                "temperature": 0.7  # Control the creativity of the responses
            }
        )

        # Log the response status and content for debugging
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content)

        # Check if the response is successful
        if response.status_code == 200:
            suggestions = response.json().get("choices", [])
            suggestions_text = [choice['message']['content'].strip() for choice in suggestions]

            # Handle empty suggestions case
            if not suggestions_text:
                return JsonResponse({"suggestions": ["No suggestions available"]})

            return JsonResponse({"suggestions": suggestions_text})

        elif response.status_code == 429:  # Handle quota exceeded
            return JsonResponse({'error': 'Quota exceeded. Please try again later.'}, status=429)

        else:
            return JsonResponse({'error': 'AI API error', 'details': response.json()}, status=response.status_code)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_ai_suggestions2(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    # If AI API is not working, generate random comments
    random_comments = [
        "This is a great photo!",
        "I love the colors in this picture.",
        "This is so inspiring!",
        "What a beautiful shot!",
        "I'm amazed by the details in this image.",
        "This picture makes me feel happy.",
        "This is a perfect capture of the moment.",
        "I can't stop looking at this photo.",
        "This is a work of art.",
        "I wish I could be there."
    ]

    random_comment = random.choice(random_comments)

    return JsonResponse({"suggestions": [random_comment]})
@login_required
def add_reply(request, comment_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = get_object_or_404(Comment, id=comment_id)
        reply = Reply.objects.create(comment=comment, author=request.user, content=content)
        return JsonResponse({
            'id': reply.id,
            'author': reply.author.fullname,
            'content': reply.content,
            'created_at': reply.created_at.strftime('%d %b %Y %H:%M'),
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def edit_reply(request, reply_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        reply = get_object_or_404(Reply, id=reply_id)
        reply.content = content
        reply.save()
        return JsonResponse({'status': 'success'})

@login_required
def delete_reply(request, reply_id):
    if request.method == 'POST':
        reply = get_object_or_404(Reply, id=reply_id)
        reply.delete()
        return JsonResponse({'status': 'success'})
    

API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Change to a Hugging Face text model
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    # Return the JSON response instead of binary content
    return response.json()

def generate_comment(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        style = request.POST.get('style')  # Optional style parameter for prompt modification

        if prompt:
            try:
                # Send the prompt to the API
                response_data = query({"inputs": f"{prompt} in a {style} style" if style else prompt})
                
                # Extract generated text
                generated_comment = response_data[0]['generated_text'] if response_data else "No comment generated"

                # Render the result with the generated comment
                return render(request, 'result.html', {
                    'prompt': prompt,
                    'style': style,
                    'generated_comment': generated_comment,
                })
            except Exception as e:
                return render(request, 'generate_comment.html', {
                    'error': str(e),
                })

    return render(request, 'generate_comment.html')


def query_huggingface(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    return response.json()

@require_GET
def get_ai_suggestions3(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    # Prepare the absolute image URL
    image_url = post.image.url if post.image else None
    if image_url:
        image_url = request.build_absolute_uri(image_url)  # Build absolute URI

    if not image_url:
        return JsonResponse({"suggestions": ["No image available."]})

    # Download the image
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad responses
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        return JsonResponse({"error": f"Error loading image: {str(e)}"}, status=500)

    # Process the image and generate a caption
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)

    return JsonResponse({"suggestions": [caption]})

@require_GET
def get_ai_comment_suggestions(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    # Prepare the absolute image URL
    image_url = post.image.url if post.image else None
    if image_url:
        image_url = request.build_absolute_uri(image_url)  # Build absolute URI

    if not image_url:
        return JsonResponse({"suggestions": ["No image available."]})

    # Download the image
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad responses
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        return JsonResponse({"error": f"Error loading image: {str(e)}"}, status=500)

    # Process the image and generate a caption
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)

    # Get comment suggestions based on the caption
    comment_response = requests.post('YOUR_COMMENT_GENERATION_AI_URL', json={'caption': caption})
    
    if comment_response.status_code == 200:
        comment_suggestions = comment_response.json().get('suggestions', [])
    else:
        comment_suggestions = ["Could not generate comment suggestions."]

    return JsonResponse({"suggestions": comment_suggestions})