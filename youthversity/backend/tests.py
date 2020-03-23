import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.resolvers import URLResolver

from .models import Post, Subject
from .models import User as BeUser


class TestPageLoads(TestCase):
    def setUp(self):
        AuthUser = get_user_model()
        auth_user = AuthUser.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        be_user = BeUser(name='username', auth_user=auth_user)
        be_user.save()

        p = Post(
            subject=Subject.objects.get(name='Physik'),
            title='title',
            visibility='world',
            content='content',
            author=be_user,
            edited=False,
            type='text',
        )
        p.save()

    def test_page_calls(self):
        errors = {}

        from .urls import urlpatterns
        patterns = []
        for pattern_or_resolv in urlpatterns:
            if isinstance(pattern_or_resolv, URLResolver):
                patterns += pattern_or_resolv.url_patterns
            else:
                patterns.append(pattern_or_resolv)

        for p in patterns:
            try:
                link = '/' + str(p.pattern)
                link = link.replace('<int:id>', '1')
                print("NOW TESTING '{}'".format(link))
                self.assertTrue(self.client.login(
                    username='temporary', password='temporary'))
                response = self.client.get(link, follow=True)
                self.assertEqual(response.status_code, 200)
            except Exception as e:
                errors[link] = e

        if errors:
            print(json.dumps(errors, indent=2, default=str))
        self.assertTrue(not errors)
