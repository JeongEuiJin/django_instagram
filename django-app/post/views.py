from django.http import HttpResponse
from django.shortcuts import render

from post.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts

    }
    return render(request, 'post/post_list.html', context)
