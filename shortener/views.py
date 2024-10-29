import logging
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import URL
from .serializers import URLSerializer
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

class URLCreateView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

class URLRedirectView(generics.RetrieveAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    lookup_field = 'shortened_url'
    
    def create(self, request, *args, **kwargs):
        logger.info("Received data: %s", request.data)
        return super().create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            url_obj = self.get_object()
            return redirect(url_obj.original_url)
        except URL.DoesNotExist:
            logger.error("URL not found: %s", kwargs['shortened_url'])
            return Response({"error": "URL not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
            return Response({"error": "An internal server error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

