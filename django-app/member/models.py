import re

import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models

from utils.fields import CustomImageField

class UserManager(DefaultUserManager):
    def get_or_create_facebook_user(self, user_info):
        username = '{}_{}_{}'.format(
            User.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id']
        )
        user, user_created = User.objects.get_or_create(
            username=username,
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={
                'last_name': user_info.get('last_name', ''),
                'first_name': user_info.get('first_name', ''),
                'email': user_info.get('email', ''),
            }
        )
        if user_created and user_info.get('picture'):
            url_picture = user_info['picture']['data']['url']
            p = re.compile(r'.*\.([^?]+)')
            file_ext = re.search(p, url_picture).group(1)
            file_name = '{}.{}'.format(
                user.pk,
                file_ext
            )
            temp_file = NamedTemporaryFile()
            response = requests.get(url_picture)
            temp_file.write(response.content)
            user.img_profile.save(file_name, File(temp_file))
        return user


class User(AbstractUser):
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO,'Django'),
        (USER_TYPE_FACEBOOK,'Facebook')
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)
    nickname = models.CharField(max_length=24, null=True, unique=True)
    img_profile = CustomImageField(
        upload_to='user',
        blank=True,
        default_static_image='images/profile.png',
    )
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )

    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username

    def follow(self, user):
        if not isinstance(user, User):
            raise ValueError('"user" argument must <User> class')
        # Relation.get_or_create(from_user=self,to_user=user)

        self.follow_relations.get_or_create(
            to_user=user
        )

    def unfollow(self, user):
        Relation.objects.filter(
            from_user=self,
            to_user=user
        ).delete()

    def is_follow(self, user):
        return self.follow_relations.filter(to_user=user).exists()

    def is_follower(self, user):
        return self.follower_relations.filter(to_user=user).exists()

    def follow_toggle(self, user):
        relation, relation_created = self.follow_relations.get_or_create(to_user=user)
        if not relation_created:
            relation.delete()
        else:
            return relation

    @property
    def following(self):
        relations = self.follow_relations.all()
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.follower_relations.all()
        return User.objects.filter(pk__in=relations.values('from_user'))


class Relation(models.Model):
    from_user = models.ForeignKey(User, related_name='follow_relations')
    to_user = models.ForeignKey(User, related_name='follower_relations')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'reation form({}) to ({})'.format(
            self.from_user,
            self.to_user,
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )
