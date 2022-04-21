from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Bigpic, Post, Category 
from hitcount.views import HitCountDetailView

class HomeView(ListView):
    context_object_name = 'bigpic_list'
    model = Bigpic
    template_name = 'tech-index.html'
    
    def get_context_data(self, *args, **kwargs):
        post_menu = Post.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["post_menu"] = post_menu
        ordering = ['-post_date']
        return context


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    ordering = ['-post_date']
    return render(request, 'categories.html', {'cats':cats, 'category_posts':category_posts})


def category_list(request):
    category_list = Category.objects.all()
    context = {
        'category_list':category_list
        }
    return context
        
class ArticleDetailView(HitCountDetailView):
    model = Post
    template_name = 'tech_single.html'
    count_hit = True 
    def get_context_data(self, *args, **kwargs):
        post_menu = Post.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["post_menu"] = post_menu
        return context


  