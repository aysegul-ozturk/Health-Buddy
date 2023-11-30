from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Post
# Create your views here.
'''
posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]
'''

class HomeView(View):

    def get(self, request):
        posts = Post.objects.order_by('-date_posted')
        context = {
            'posts': posts
        }
        return render(request, 'blog/home.html', context)

class AboutView(View):

    def get(self, request):
        return render(request, 'blog/about.html', {'title': 'About'})