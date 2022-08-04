from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Post, User
from django.contrib.auth.decorators import login_required
from .forms import PostForm


def index(request):
    template = 'posts/index.html'
    page_obj = get_page(Post.objects.all(), request)
    context = {'page_obj': page_obj}
    return render(request, template, context, page_obj)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    page_obj = (get_page(group.posts.all(), request))
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context, page_obj)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    page_obj = (get_page(posts, request))
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, template, context, page_obj)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    form = PostForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts:post_detail'
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        form = PostForm(
            request.POST or None,
            instance=post)
        if form.is_valid():
            form.save()
            return redirect(template, post_id=post_id)
        context = {
            'form': form,
            'is_edit': True,
            'post_id': post_id,
        }
        return render(request, 'posts/post_create.html', context)
    return redirect(template, post_id)


def get_page(posts, request):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
