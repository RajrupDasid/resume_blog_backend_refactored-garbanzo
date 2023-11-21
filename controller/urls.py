from django.urls import path
from .views import index, blogdetailview, comment, postcounter, contactview, category, aboutus, termsview, privacyview, robots_txt
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, BlogSitemap, CategorySitemap

# app_name = 'app'

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'category': CategorySitemap,
}


urlpatterns = [
    path('', index, name="index"),
    path('<str:category>/<str:slug>',
         blogdetailview, name="detailview"),
    path('<str:category>/', category, name="category"),
    path('comments/', comment, name="comment"),
    path('analytics/', postcounter, name='analytics'),
    path('contacts/', contactview, name="contact"),
    path('aboutus/', aboutus, name='aboutus'),
    path('terms-and-conditions', termsview, name='terms'),
    path('privacy-policy', privacyview, name="privacypolicy"),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # path('search', SearchView.as_view(), name="search"),

    # path('trending', TrendingPostView.as_view(), name='trendingposts')
]
