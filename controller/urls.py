from django.urls import path
from .views import IndexAPIView, BlogDetailView, Contact, SearchView, CategoryView, PostClickCounter

urlpatterns = [
    path('blogs/', IndexAPIView.as_view(), name="index"),
    path('blogs/<str:category>/<str:slug>',
         BlogDetailView.as_view(), name="detailview"),
    path('contacts/', Contact.as_view(), name="contactview"),
    path('search', SearchView.as_view(), name="search"),
    path('category/<str:category>', CategoryView.as_view(), name="category"),
    path('logVisit', PostClickCounter.as_view(), name='analytics')
]
