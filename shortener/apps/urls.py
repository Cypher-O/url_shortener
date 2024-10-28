# urlshortener/apps/shortener/urls.py

from django.urls import path
from .views import URLCreateView, URLRedirectView

urlpatterns = [
    path('shorten/', URLCreateView.as_view(), name='url-create'),
    path('<str:shortened_url>/', URLRedirectView.as_view(), name='url-redirect'),
]