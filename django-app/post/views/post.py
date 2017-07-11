from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_POST

from post.decorators import post_owner
from post.forms import CommentForm
from post.models import Tag

from ..forms import PostForm
from ..models import Post

User = get_user_model()

__all__ = (
    'post_list',
    'post_detail',
    'post_create',
    'post_modify',
    'post_delete',
    'post_like_toggle',
    'hashtag_post_list',
)


def post_list_original(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'post/post_list.html', context)


def post_list(request):
    all_posts = Post.objects.all()
    p = Paginator(all_posts, 3)
    page_num = request.GET.get('page')
    try:
        posts = p.page(page_num)

    except PageNotAnInteger:
        posts = p.page(1)
    except EmptyPage:
        posts = p.page(p.num_pages)

    context = {
        'posts': posts,
        # 'comment_form': CommentForm(),
        'comment_form': CommentForm(auto_id=False),
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)
    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
    }
    rendered_string = template.render(context=context, request=request)
    return HttpResponse(rendered_string)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(author=request.user)
            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


@post_owner
@login_required
def post_modify(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_modify.html', context)


@post_owner
@login_required
def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post:post_list')
    else:
        context = {
            'post': post,
        }
        return render(request, 'post/post_delete.html', context)


@require_POST
@login_required
def post_like_toggle(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post_like, post_like_created = post.postlike_set.get_or_create(
        user=request.user
    )
    if not post_like_created:
        post_like.delete()
    return redirect('post:post_detail', post_pk=post.pk)


def hashtag_post_list(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(my_comment__tags=tag)
    posts_count = posts.count()

    context = {
        'tag': tag,
        'posts': posts,
        'posts_count': posts_count,
    }
    return render(request, 'post/hashtag_post_list.html', context)
