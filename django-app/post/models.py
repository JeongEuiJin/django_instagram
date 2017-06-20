"""
member application생성
    settings.AUTH_USER_MODEL모델 구현
        username, nickname
이후 해당 settings.AUTH_USER_MODEL모델을 Post나 Comment에서 author나 user항목으로 참조
"""
import re
from audioop import reverse

from django.conf import settings
from django.db import models


class Post(models.Model):
    # Django가 제공하는 기본 settings.AUTH_USER_MODEL와 연결되도록 수정
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    my_comment = models.OneToOneField('Comment', related_name='+', blank=True, null=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        through='PostLike',
    )

    class Meta:
        ordering = ['-pk', ]

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은 user를 author로 가지며
        # content를 content필드내용으로 넣는 Comment객체 생성
        return self.comment_set.create(author=user, content=content)

    def add_tag(self, tag_name):
        # tags에 tag매개변수로 전달된 값(str)을
        # name으로 갖는 Tag객체를 (이미 존재하면)가져오고 없으면 생성하여
        # 자신의 tags에 추가
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if not self.tags.filter(id=tag.id).exists():
            self.tags.add(tag)

    @property
    def like_count(self):
        # 자신을 like하고 있는 user수 리턴
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


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


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)
