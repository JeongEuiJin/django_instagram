import re
from audioop import reverse

from django.conf import settings
from django.db import models

from .others import Tag
from .post import Post

__all__ = (
    'Comment',
    'CommentLike',
)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='like_comments',
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()
        super().save(*args, **kwargs)

    def make_html_content_and_add_tags(self):

        p = re.compile(r'(#\w+)')

        tag_name_list = re.findall(p, self.content)

        ori_content = self.content

        for tag_name in tag_name_list:

            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))

            change_tag = '<a href="{url}" class="hash-tag">{tag_name}</a>'.format(
                url=reverse('post:hashtag_post_list', args=[tag_name.replace('#', '')]),
                tag_name=tag_name

            )
            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)

            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)

        self.html_content = ori_content


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)
