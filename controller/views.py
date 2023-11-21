from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Blog, Comment, Contact
# from .serializers import SearchSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from analytics.models import Analytics
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from decouple import config

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

websitenames = "Webstackpros.net"


@cache_page(CACHE_TTL)
@csrf_protect
def index(request):
    indexname = websitenames
    if request.method == "GET":
        all_blog = Blog.objects.all().order_by('-created')
        paginated_number = 10
        paginator = Paginator(all_blog, paginated_number)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        featured_posts = Blog.objects.filter(featured=True)
        categories = Blog.objects.values('category').annotate(
            total=Count('category')).order_by('category')
        # trending data
        post_ids = Analytics.objects.filter(
            post_clicks__gte=5).exclude(post_id__isnull=True).values('post_id')
        trending_data = Blog.objects.filter(
            _id__in=post_ids).order_by('-created')[:10]
        # trending data ends
        breadcrumbs = [
            {'title': 'Home', 'url': '/'},
        ]
        context = {
            'page_obj': page_obj,
            'featured': featured_posts,
            'breadcrumbs': breadcrumbs,
            'categories': categories,
            'websitename': indexname,
            'trending': trending_data,
        }
        return render(request, 'index.html', context)
    else:
        messages.error(request, "Something went wrong please try again")


@cache_page(CACHE_TTL)
def blogdetailview(request, category, slug):
    indexname = websitenames
    if request.method == "GET":
        blog = get_object_or_404(Blog, category=category, slug=slug)
        previous_post = Blog.objects.filter(
            created__lt=blog.created).order_by('-created').first()
        next_post = Blog.objects.filter(
            created__gt=blog.created).order_by('created').first()
        categories = Blog.objects.values('category').annotate(
            total=Count('category')).order_by('category')
        # trending data
        post_ids = Analytics.objects.filter(
            post_clicks__gte=5).exclude(post_id__isnull=True).values('post_id')
        trending_data = Blog.objects.filter(
            _id__in=post_ids).order_by('-created')[:10]
        breadcrumbs = [
            {'title': 'Home', 'url': '/'},
            {'title': blog.category},
            {'title': blog.title, 'url': f'{blog.category}/{blog.title}'},
        ]
        context = {
            "blog": blog,
            "breadcrumbs": breadcrumbs,
            'current_post': blog,
            'previous_post': previous_post,
            'next_post': next_post,
            'categories': categories,
            'websitename': indexname,
            'trending': trending_data,
        }
        return render(request, 'blog-single.html', context)


@cache_page(CACHE_TTL)
def comment(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        comment = request.POST["message"]
        subject = request.POST["subject"]
        if len(name) < 5 and len(email) < 3 and len(comment) < 10:
            return HttpResponse(0)
        else:
            comment = Comment(name=name, email=email,
                              comment=comment, subject=subject)
            comment.save()
            return HttpResponse(1)
    else:
        messages.error(request, "Something went wrong please try again")


@cache_page(CACHE_TTL)
@csrf_protect
def postcounter(request):
    if request.method == 'POST':
        # Assuming you have a post ID in the request data
        post_id = request.POST.get('postid')
        print(post_id)

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
        return HttpResponse(1)
    else:
        messages.error(request, "Something went wrong please try again")


@cache_page(CACHE_TTL)
@csrf_protect
def contactview(request):
    indexname = websitenames
    if request.method == "GET":
        context = {
            'websitename': indexname,
        }
        return render(request, 'contact.html', context)
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        if len(username) < 5 and len(email) < 3 and len(message) < 10 and len(subject) < 5:
            return HttpResponse(0)
        else:
            contact = Contact(username=username, email=email,
                              subject=subject, message=message)
            contact.save()
            return HttpResponse(1)


@cache_page(CACHE_TTL)
def category(request, category):
    indexname = websitenames
    fetchcategory = Blog.objects.filter(category=category)
    paginated_number = 10
    paginator = Paginator(fetchcategory, paginated_number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Blog.objects.values('category').annotate(
        total=Count('category')).order_by('category')
    # trending data
    post_ids = Analytics.objects.filter(
        post_clicks__gte=5).exclude(post_id__isnull=True).values('post_id')
    trending_data = Blog.objects.filter(
        _id__in=post_ids).order_by('-created')[:10]
    # trending data ends
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'trending': trending_data,
        'websitename': indexname,
    }
    return render(request, 'category.html', context)


@cache_page(CACHE_TTL)
def aboutus(request):
    indexname = websitenames
    context = {
        'websitename': indexname,
    }
    return render(request, 'aboutus.html', context)


@cache_page(CACHE_TTL)
def termsview(request):
    indexname = websitenames
    context = {
        'websitename': indexname,
    }
    return render(request, 'terms.html', context)


@cache_page(CACHE_TTL)
def privacyview(request):
    indexname = websitenames
    context = {
        'websitename': indexname,
    }
    return render(request, 'privacy.html', context)


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")


robots_txt_content = """\
User-agent: *
Disallow: webstackpros360/admin
Sitemap: https://webstackpros.net/sitemap.xml
"""


# class SearchView(APIView):

#     @method_decorator(cache_page(CACHE_TTL))
#     def post(self, request, search_query, *args, **kwargs):
#         search = Blog.objects.filter(
#             Q(title__iexact=search_query) | Q(content__icontains=search_query) | Q(category__icontains=search_query))
#         serializer = SearchSerializer(search, many=True)
#         return Response(serializer.data)
