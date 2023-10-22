from django.urls import path
from .views import IndexAPIView, BlogDetailView, Contact

urlpatterns = [
    path('blogs/', IndexAPIView.as_view(), name="index"),
    path('blogs/<str:category>/<str:slug>',
         BlogDetailView.as_view(), name="detailview"),
    path('contacts/', Contact.as_view(), name="contactview")
]
