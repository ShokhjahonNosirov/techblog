from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post, Category 
from hitcount.views import HitCountDetailView
from taggit.models import Tag


class HomeView(ListView):
    model = Post
    template_name = 'tech-index.html'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context.update({
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context



def CategoryView(request, cats): #cats hozir bu yerda tipa argument, code advomida cats nimaligi izohlab ketiladi.
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
        similar_posts = self.object.tags.similar_objects()[:3]
        context["post_menu"] = post_menu
        context.update({
            'similar_posts':similar_posts,
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context

  