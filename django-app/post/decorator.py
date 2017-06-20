from django.core.exceptions import PermissionDenied

from post.models import Post


def post_owner(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_pk'])
        if request.user == post.author:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap