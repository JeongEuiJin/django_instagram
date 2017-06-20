from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_POST

from post.decorator import post_owner
from post.forms import CommentForm
from post.forms import PostForm
from ..models import Post, Tag

User = get_user_model()

__all__ = (
    'post_list',
    'post_create',
    'post_delete',
    'post_detail',
    'post_modify',
    'hashtag_post_list',
)
def post_list(request):
    # 모든 Post목록을 'posts'라는 key로 context에 담아 return render처리
    # post/post_list.html을 template으로 사용하도록 한다

    # 각 포스트에 대해 최대 4개까지의 댓글을 보여주도록 템플릿에 설정

    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # return redirect('post:post_list')
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)
    template = loader.get_template('post/post_detail.html')

    context = {
        'post': post,
    }

    rendered_string = template.render(context=context, request=request)

    return HttpResponse(rendered_string)


@post_owner
@login_required
def post_create(request):
    # POST요청을 받아 Post객체를 생성 후 post_list페이지로 redirect
    if request.method == 'POST':
        #     user = User.objects.first()
        #     post = Post.objects.create(
        #         author=user,
        #         photo=request.FILES['photo'],
        #     )
        #     comment_string = request.POST.get('comment', '')
        #     if comment_string:
        #         post.comment_set.create(
        #             author=user,
        #             content=comment_string,
        #         )
        #
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(
                # commit=False,
                author=request.user
            )
            # post.author = request.user
            # post.save()

            # comment_string = form.cleaned_data['comment']
            # if comment_string:
            #     post.comment_set.create(
            #         author=post.author,
            #         content=comment_string,
            #     )

            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm()
        context = {
            'form': form,
        }

        return render(request, 'post/post_create.html', context)


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


def post_delete(request, post_pk):
    # post_pk에 해당하는 Post에 대한 delete요청만을 받음
    # 처리완료후에는 post_list페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':

        post.delete()
        return redirect('post:post_list')
    else:
        context = {
            'post': post,
        }
        return render(request, 'post/post_delete.html', context)

def hashtag_post_list(request,tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(comment__tags=tag).distinct()
    posts_count = post.count()

    context = {
        'tag':tag,
        'posts':posts,
        'posts_count':posts_count,

    }
    return render(request, 'post/hashtag_post_list.html',context)
