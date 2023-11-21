from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog


class StaticViewSitemap(Sitemap):
    # Priority for all URLs
    priority = 0.5
    # Change frequency for all URLs
    changefreq = 'weekly'

    def items(self):
        # Return a list of URL names for static views
        return ['index', 'contact', 'aboutus', 'terms', 'privacypolicy',]

    def location(self, item):
        # Return the URL for the given URL name
        return reverse(item)


class BlogSitemap(Sitemap):
    # Priority for blog detail URLs
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        # Return queryset of dynamic URLs for blogdetailview
        return Blog.objects.all()  # Replace YourBlogModel with your actual model

    def location(self, obj):
        # Return the URL for each blog detail item
        # Adjust this based on your URL structure
        return f'/{obj.category}/{obj.slug}'


class CategorySitemap(Sitemap):
    # Priority for category URLs
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        # Return queryset of dynamic URLs for category view
        # Replace YourCategoryModel with your actual model
        return Blog.objects.all()

    def location(self, obj):
        # Return the URL for each category item
        return f'/{obj.category}/'  # Adjust this based on your URL structure
