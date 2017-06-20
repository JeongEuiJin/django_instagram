from django.core.exceptions import PermissionDenied

from post.models import Post , Comment


def post_owner(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_pk'])
        if request.user == post.author:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def comment_owner(f):
    def wrap(request, *args, **kwargs):
        post = Comment.objects.get(pk=kwargs['post_pk'])
        if request.user == comment.author:
            return f(request, *args, **kwargs)
        raise PermissionDenied
    return wrap