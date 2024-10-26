# comments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from posts.models import Post  # Import Post model from posts app to reference it in this file
from django.http import JsonResponse


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