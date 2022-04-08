from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Bigpic, Post 


class HomeView(ListView):
    context_object_name = 'bigpic_list'
    model = Bigpic
    template_name = 'tech-index.html'
    ordering = ['-id']
    
    def get_context_data(self, *args, **kwargs):
        post_menu = Post.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["post_menu"] = post_menu
        return context
        
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'tech_single.html'

    def get_context_data(self, *args, **kwargs):
        post_menu = Post.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["post_menu"] = post_menu
        return context


  