from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from category.models import Category 

# Adding index view for completeness
def index(request):
    return render(request, 'posts/index.html')

def post_list(request):
    # Get all categories to display in the filter
    categories = Category.objects.all()

    # Get selected category from the GET parameters
    selected_category = request.GET.get('category')

    # Filter posts by the selected category if it exists, otherwise show all posts
    if selected_category:
        posts = Post.objects.filter(category__id=selected_category).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category
    })


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def post_create(request):
    categories = Category.objects.all()  # Fetch all categories
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the logged-in user
            post.category_id = request.POST.get('category')  # Set the selected category
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form, 'categories': categories})  # Pass categories to the template


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:  # Check if the user is the author
        return redirect('post_list')  # Redirect if not the author
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')  
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_update.html', {'post': post, 'form': form, 'categories': categories})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at').select_related('category')  
    return render(request, 'posts/myPosts.html', {'posts': posts})

def category_list(request):
    categories = Category.objects.prefetch_related('posts').all()
    return render(request, 'categories/category_list.html', {'categories': categories})

