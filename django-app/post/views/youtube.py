import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST


from post.models import Post, Comment
from post.models.youtube import Video
from utils.youtube import youtube

__all__ = (
    'youtube_search',
    'post_create_with_video',
)


def youtube_search_origin(request, q=None):
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    q = request.GET.get('q')
    if q:
        search_params = {
            'part': 'snippet',
            'key': 'AIzaSyAokgs8K0D61OeXwJaFnf3L_PFrMSabF80',
            'maxResult': '10',
            'type': 'video',
            'q': q,

        }

        response = requests.get(url_api_search, params=search_params)

        data = response.json()

        for item in data['items']:
            Video.objects.create_from_search_result(item)

        videos = Video.objects.filter(title__contains=q)
        videos = Video.objects.filter(Q(title_contains=q) | Q(description__contains=q))
        videos = Video.objects.all()
        for cur_q in q.split(' '):
            videos.filter(title__contains=cur_q)

        # regex
        # and
        re_pattern = ''.join(['(?=.*{})'.format(item) for item in q.split()])
        # or
        re_pattern = '|'.join(['({})'.format(item) for item in q.split()])
        videos = Video.objecst.filter(
            Q(title__iregex=r'{}'.format(re_pattern)),
            Q(description_iregex=r'{}'.format(re_pattern))
        )

        context = {
            'videos': videos,
            're_pattern': re_pattern,
        }


    else:
        context = {}

    return render(request, 'post/youtube_search.html', context)


def youtube_search(request, q=None):
    context = dict()
    q = request.GET.get('q')
    if q:

        data = youtube.search(q)
        for item in data['items']:
            Video.objects.create_from_search_result(item)
        re_pattern = ''.join(['(?=.*{}'.format(item) for item in q.split()])
        videos = Video.objects.filter(
            Q(title__iregex=re_pattern) |
            Q(description__iregex=re_pattern)
        )
        context['videos'] = videos

    return render(request, 'post/youtube_search.html', context)


@require_POST
@login_required
def post_create_with_video(request):
    video_pk = request.POST['video_pk']
    video = get_object_or_404(Video, pk=video_pk)

    post = Post.objects.create(
        author=request.user,
        video=video,
    )
    post.my_comment = Comment.objcets.create(
        content=video.title,
    )
