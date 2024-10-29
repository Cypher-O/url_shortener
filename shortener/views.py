from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework import status
from django.http import HttpResponseRedirect
from .models import URL
from .serializers import URLSerializer
from .utils import APIResponse
import logging

logger = logging.getLogger(__name__)

class URLCreateView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new shortened URL. Data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            url_object = serializer.save()
            response_data = serializer.data
            short_url = request.build_absolute_uri(f'/{url_object.shortened_url}/')
            response_data['short_url'] = short_url
            logger.info(f"Created shortened URL: {short_url}")
            return APIResponse.success(
                data=response_data,
                message="URL shortened successfully",
                status_code=status.HTTP_201_CREATED
            )
        return APIResponse.error(
            message="Invalid URL provided",
            code=2,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class URLRedirectView(generics.GenericAPIView):
    queryset = URL.objects.all()
    
    def get(self, request, shortened_url):
        logger.info(f"Received redirect request for: {shortened_url}")
        try:
            url_obj = URL.objects.get(shortened_url=shortened_url)
            original_url = url_obj.original_url
            
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'http://' + original_url
            
            logger.info(f"Redirecting to: {original_url}")
            return HttpResponseRedirect(original_url)
            
        except URL.DoesNotExist:
            logger.warning(f"URL not found: {shortened_url}")
            return APIResponse.error(
                message="Shortened URL not found",
                code=3,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Redirect error: {str(e)}")
            return APIResponse.error(
                message="An error occurred during redirect",
                code=4,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class URLListView(generics.ListAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(
            data=serializer.data,
            message="URLs retrieved successfully"
        )

def url_shortener_view(request):
    return render(request, 'shortener/url_form.html')
