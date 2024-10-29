from django.urls import path, re_path
from .views import URLCreateView, URLRedirectView
from django.http import HttpResponse

urlpatterns = [
    path('shorten/', URLCreateView.as_view(), name='url-create'),
    path('<str:shortened_url>/', URLRedirectView.as_view(), name='url-redirect'),
    re_path(r'^.*$', lambda request: HttpResponse("Caught a request, but no matching URL pattern."), name='catch-all'),
]