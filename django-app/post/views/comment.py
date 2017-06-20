from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

from post.forms import CommentForm
from ..models import Post, Comment

User = get_user_model()

__all__ = (
    'comment_create',
    'comment_delete',
    'comment_modify',
)


@require_POST
@login_required
def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    next = request.GET.get('next')
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    else:
        result = '<br>'.join(['<br>'.join(v) for k, v in form.errors.values()])
        messages.error(request, request)
        # messages.error(request,'comment form invalid')
    if next:
        return redirect(next)
    return redirect('post:post_detail', post_pk=post.pk)


def comment_modify(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    next = request.POST.get('next')
    if request.method == 'POST':
        form = CommentForm(data=request.POST, instance=comment)
        form.save()
        if next:
            return redirect(next)
        return redirect('post:post_detail',post_pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
    }

    return render(request, 'post/comment_modify.html', context)


def comment_delete(request, post_pk, comment_pk):
    # POST요청을 받아 Comment객체를 delete, 이후 post_detail페이지로 redirect
    pass
