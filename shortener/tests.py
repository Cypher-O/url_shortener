from django.test import TestCase

# urlshortener/apps/shortener/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import URL

class URLShortenerTests(APITestCase):
    def test_create_url(self):
        data = {'original_url': 'http://example.com'}
        response = self.client.post(reverse('url-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_redirect_url(self):
        url = URL.objects.create(original_url='http://example.com')
        response = self.client.get(reverse('url-redirect', kwargs={'shortened_url': url.shortened_url}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)