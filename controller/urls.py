from django.urls import path
from .views import IndexAPIView, BlogDetailView

urlpatterns = [
    path('blogs/', IndexAPIView.as_view(), name="index"),
    path('blogs/<str:slug>', BlogDetailView.as_view(), name="detailview")
]
