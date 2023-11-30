#You need to create this file yourself
from django.urls import path
from . import views #from current directory
from .views import HomeView, AboutView

urlpatterns = [
    path('', HomeView.as_view(), name='blog-home'),
    path('about/', AboutView.as_view(), name='blog-about'),
]