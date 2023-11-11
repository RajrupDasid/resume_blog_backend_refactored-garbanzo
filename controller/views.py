from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Blog
from .serializers import BlogViewSerializer, BlogDetailSerializer, ContactSerializer, SearchSerializer, CategorySerializer, AnalyticsSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_api_key.permissions import HasAPIKey
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from analytics.models import Analytics

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
    def get(self, request, category, slug, *args, **kwargs):
        slug = get_object_or_404(Blog, category=category, slug=slug)
        serializer = BlogDetailSerializer(slug)
        return Response(serializer.data)

    def post(self, request):
        return Response({'error': 'Something went wrong. Please try again.'}, status=400)


class Contact(APIView):
    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Contact hasbeen save into database successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Error you need to fillup the form'}, status=status.HTTP_400_BAD_REQUEST)


class SearchView(APIView):
    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request, search_query, *args, **kwargs):
        search = Blog.objects.filter(
            Q(title__iexact=search_query) | Q(content__icontains=search_query) | Q(category__icontains=search_query))
        serializer = SearchSerializer(search, many=True)
        return Response(serializer.data)


class CategoryView(APIView):
    permission_classes = [HasAPIKey]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, category, *args, **kwargs):
        fetchcategory = Blog.objects.filter(category=category)
        serializer = CategorySerializer(fetchcategory, many=True)
        response = serializer.data
        return Response(response)


class PostClickCounter(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, *args, **kwargs):
        data = request.data

        # Assuming you have a post ID in the request data
        post_id = data.get('postid')

        if not post_id:
            return Response({'error': 'Post ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the corresponding Analytics instance or create a new one
        analytics_instance, created = Analytics.objects.get_or_create(
            post_id=post_id)

        # Update the analytics data based on your requirements
        analytics_instance.post_clicks += 1  # Increment the post click count

        # Assuming you have more analytics data in the request, update it accordingly

        # Save the changes
        analytics_instance.save()

        serializer = AnalyticsSerializer(analytics_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
