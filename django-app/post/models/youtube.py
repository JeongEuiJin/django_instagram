from django.db import models

__all__ = (
    'Video',
    'VideoManager',
)
class VideoManager(models.Manager):
    def create_from_search_result(self,result):
        youtube_id = result['id']['videoId']
        title = result['snippet']['title']
        description = result['snippet']['description']
        url_thumbnail = result['snippet']['thumbnails']['high']
        video, video_create = self.get_or_create(
            youtube_id=youtube_id,
            defaults={
                'title': title,
                'description': description,
                'url_thumbnail': url_thumbnail,
            }
        )
        print('Video ({}) is {}'.format(
            video.title,
            'created' if video_create else 'already exist'
        ))

class Video(models.Model):
    youtube_id = models.CharField(max_length=50,unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url_thumbnail = models.CharField(max_length=200)

    objects = VideoManager()

    def __str__(self):
        return self.title
