from django.shortcuts import render

# urlshortener/apps/shortener/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import URL
from .serializers import URLSerializer

class URLCreateView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

class URLRedirectView(generics.RetrieveAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    lookup_field = 'shortened_url'

    def get(self, request, *args, **kwargs):
        url_obj = self.get_object()
        return Response({"redirect_url": url_obj.original_url}, status=status.HTTP_302_FOUND)