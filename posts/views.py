from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Post
from .forms import PostForm 
from comments.forms import CommentForm 


from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'index.html')
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    form = CommentForm()  
    return render(request, 'posts/post_list.html', {'posts': posts, 'form': form})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the logged-in user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:  # Check if the user is the author
        return redirect('post_list')  # Redirect if not the author
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')  
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_update.html', {'post': post, 'form': form})