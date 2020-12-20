from django.test import TestCase
from .models import Post
from account.models import User
from django.utils.timezone import localtime


class PostTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(email='mohsn@gmail.com', full_name='mohsn', password='mohsn')
        post1 = Post.objects.create(title='post1', slug='post1', content='Weather is good', author=user,
                                    publish_time=localtime())
        post1.create_setting()
        post2 = Post.objects.create(title='post2', slug='post2', content='I love music', author=user,
                                    publish_time=localtime())
        post2.create_setting(comment=False, author=False)
        post3 = Post.objects.create(title='post3', slug='post3', content='Today will be better', author=user,
                                    publish_time=localtime())
        post3.create_setting(comment=False, author=True, allow_discussion=True)

    def test_post(self):
        post1 = Post.objects.get(slug='post1')
        post2 = Post.objects.get(title='post2')
        post3 = Post.objects.get(content='Today will be better')
        self.assertEqual(post1.setting.author, True)
        self.assertEqual(post2.setting.comment, False)
        self.assertEqual(post3.get_comments(), [])
        self.assertEqual(post1.category, None)
        self.assertEqual(post2.draft, True)
