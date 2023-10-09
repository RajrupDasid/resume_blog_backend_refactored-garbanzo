from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Blog
from .serializers import BlogViewSerializer, BlogDetailSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_api_key.permissions import HasAPIKey
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class IndexAPIView(APIView):
    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        all_views = Blog.objects.all().order_by('-created')
        serializer = BlogViewSerializer(all_views, many=True)
        response = serializer.data
        return Response(response)

    def post(self, request):
        return Response({'error': 'Something went wrong. Please try again.'}, status=400)


class BlogDetailView(APIView):
    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, slug, *args, **kwargs):
        slug = get_object_or_404(Blog, slug=slug)
        serializer = BlogDetailSerializer(slug)
        return Response(serializer.data)

    def post(self, request):
        return Response({'error': 'Something went wrong. Please try again.'}, status=400)
