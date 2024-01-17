from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from account.models import User

# Create your views here.

def home(request):
    form = PostForm()
    posts = Post.objects.all()
    if 'post' in request.POST:
        user = request.user
        try:
            User.objects.get(username=user.username)
        except User.DoesNotExist:
            messages.error(request, 'Login before creating a post')
            return redirect('home')
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post added successfuly')
            return redirect('home')
    context = {
        'posts':posts,
        'form':form,
    }
    return render(request, 'blog/index.html', context)

@login_required(login_url='login')
def deletePost(request, ref):
    if request.method == 'POST':
        Post.objects.filter(id=ref).delete()
        messages.success(request, 'Done')
        return redirect('home')
    return render(request, 'blog/delete.html')

@login_required(login_url='login')
def updatePost(request, ref):
    post = Post.objects.get(id=ref)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Done')
            return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'blog/update-post.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')