from django.urls import path, re_path
from .views import URLCreateView, URLRedirectView, URLListView, url_shortener_view
from django.http import HttpResponse

urlpatterns = [
    path('', url_shortener_view, name='url-shortener'),
    path('api/shorten/', URLCreateView.as_view(), name='url-create'),
    path('api/urls/', URLListView.as_view(), name='url-list'),
    path('<str:shortened_url>/', URLRedirectView.as_view(), name='url-redirect'),
    re_path(r'^.*$', lambda request: HttpResponse("Caught a request, but no matching URL pattern."), name='catch-all'),
]
