from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import URL
from .serializers import URLSerializer
import logging
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

class URLCreateView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            url_object = serializer.save()
            response_data = serializer.data
            response_data['short_url'] = request.build_absolute_uri(f'/{url_object.shortened_url}/')
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class URLRedirectView(generics.GenericAPIView):
    queryset = URL.objects.all()
    
    def get(self, request, shortened_url):
        logger.info(f"Received redirect request for shortened_url: {shortened_url}")
        try:
            url_obj = URL.objects.get(shortened_url=shortened_url)
            original_url = url_obj.original_url
            
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'http://' + original_url
                
            logger.info(f"Redirecting to: {original_url}")
            return HttpResponseRedirect(original_url)
            
        except URL.DoesNotExist:
            logger.error(f"URL not found for shortened_url: {shortened_url}")
            return Response(
                {"error": "Shortened URL not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error during redirect: {str(e)}")
            return Response(
                {"error": "An error occurred during redirect"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )