from django.urls import path
from .views import index, blogdetailview, comment, postcounter, contactview, category, aboutus, termsview, privacyview, newsletterview, searchresult
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, BlogSitemap, CategorySitemap
from django.views.generic.base import TemplateView
# app_name = 'app'

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'category': CategorySitemap,
}


urlpatterns = [
    path('', index, name="index"),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
    path('privacy-policy/', privacyview, name="privacypolicy"),
    path('terms-and-conditions/', termsview, name='terms'),
    # ... other paths ...
    path('comments/', comment, name="comment"),
    path('analytics/', postcounter, name='analytics'),
    path('contactus/', contactview, name="contact"),
    path('aboutus/', aboutus, name='aboutus'),
    path('newsletter/', newsletterview),
    path('searchresult/', searchresult, name='searchresult'),
    path('<str:category>/<str:slug>/', blogdetailview, name="detailview"),
    path('<str:category>/', category, name="category"),


    # path('search', SearchView.as_view(), name="search"),

    # path('trending', TrendingPostView.as_view(), name='trendingposts')
]
