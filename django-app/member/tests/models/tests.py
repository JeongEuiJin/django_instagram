from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

User = get_user_model()


class UserModelTest(TransactionTestCase):
    DUMMY_USERNAME = 'username'
    DUMMY_PASSWORD = 'password'

    @staticmethod
    def make_users(num):
        return [User.objects.create_user(username='username{}'.format(i)) for i in range(num)]
        # users = [User.objects.create_user(username='username : {}'.format(i+1),)for i in range(10)]
        # for i in range(10):
        #     user = User.objects.create_user(username='username : {}'.format(i+1),)
        #     users.append(user)
        # return users

    def test_fields_default_value(self):
        user = User.objects.create_user(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD
        )
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.email, '')
        self.assertEqual(user.user_type, User.USER_TYPE_DJANGO)
        self.assertEqual(user.nickname, None)
        self.assertEqual(user.img_profile, '')
        self.assertEqual(user.relations.count(), 0)

    def test_follow(self):
        def follow_test_helper(source, following, non_following=None):
            for target in following:
                self.assertIn(target, source.following)
                self.assertIn(target, source.followers)
                self.assertTrue(source.is_follow(target))
                self.assertTrue(target.is_follower(source))
            for target in non_following:
                self.assertNotIn(target, source.following)
                self.assertNotIn(source, source.followers)
                self.assertFalse(source.is_follow(target))
                self.assertFalse(source.is_follower(source))

        user1, user2, user3, user4 = self.make_users(4)
        user1.follow(user2)
        user1.follow(user3)
        user1.follow(user4)

        user2.follow(user3)
        user2.follow(user4)

        user3.follow(user4)

        follow_test_helper(
            source=user1,
            following=[user2, user3, user4],
            non_following=[],
        )

        follow_test_helper(
            source=user2,
            following=[user3, user4],
            non_following=[user1],
        )

        follow_test_helper(
            source=user3,
            following=[user4],
            non_following=[user1, user2],
        )

        follow_test_helper(
            source=user4,
            following=[],
            non_following=[user1, user2, user3],
        )

    def teet_unfollow(self):
        user1, user2 = self.make_users(2)
        user1.follow(user2)

        self.assertTrue(user1.is_follow(user2))
        self.assertTrue(user2.is_follower(user1))
        self.assertIn(user1, user2.followers)
        self.assertIn(user2, user1.following)

        user1.unfollow(user2)
        self.assertFalse(user1.is_follow(user2))
        self.assertFalse(user2.is_follower(user1))
        self.assertNotIn(user1, user2.followers)
        self.assertNotIn(user2, user1.followers)

    def test_follow_toggle(self):
        user1, user2 = self.make_users(2)
        user1.follow_toggle(user2)

        self.assertTrue(user1.is_follow(user2))
        self.assertTrue(user2.is_follower(user1))
        self.assertIn(user1, user2.followers)
        self.assertIn(user2, user1.following)

        user1.follow_toggle(user2)
        self.assertFalse(user1.is_follow(user2))
        self.assertFalse(user2.is_follower(user1))
        self.assertNotIn(user1, user2.followers)
        self.assertNotIn(user2, user1.followers)


class UserModelManagerTest(TransactionTestCase):
    def test_get_or_create_facebook_user(self):
        test_last_name = 'test_last_name'
        test_first_name = 'test_first_name'
        test_email = 'test_email@email.com'

        user_info = {
            'id': 'dummy_facebook_id',
            'test_last_name': 'test_last_name',
            'test_first_name': 'test_first_name',
            'test_email': 'test_email@email.com',

        }

        user = User.objects.get_or_create_facebook_user(user_info)

        self.assertEqual(
            user.username,
            '{}_{}_{}'.format(
                User.USER_TYPE_FACEBOOK,
                settings.FACEBOOK_APP_ID,
                user_info['id']
            )
        )
        self.assertEqual(user.user_type, User.USER_TYPE_FACEBOOK)
        self.assertEqual(user.last_name, test_last_name)
        self.assertEqual(user.first_name, test_first_name)
        self.assertEqual(user.email, test_email)
