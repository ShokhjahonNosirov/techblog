from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Category, Comment
from hitcount.views import HitCountDetailView
from members.forms import CommentForm
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



def CategoryView(request, cats): #cats hozir bu yerda tipa argument, code davomida cats nimaligi izohlab ketiladi.
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
    form = CommentForm()
    

    def date(self, year, month, day, slug):
        obj = super().get_object(slug=obj,
                                        publish__year=year, 
                                        publish__month=month,
                                        publish__day=day)
        return obj


    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form = form.save(commit=False)
            form.post = post
            form.name = request.user
            form.save()

            return redirect('article-detail', kwargs['year'], kwargs['month'], kwargs['day'], kwargs['slug'])
        
        return redirect('home')

    

    def get_context_data(self, *args, **kwargs):
        post_menu = Post.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        similar_posts = self.object.tags.similar_objects()[:2]
        context["post_menu"] = post_menu
        post = Post.objects.get(slug=kwargs['object'].slug)
        comments = post.comments.all()

        context.update({
            'similar_posts':similar_posts,
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
            'comments': comments,
            })
        return context   


















































  