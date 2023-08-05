from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
# ^ this was used for like part after like to come back to the site 
from django.views.generic import ListView, DetailView
from .models import Post, Category, Comment, Contact, IpModel
from hitcount.views import HitCountDetailView
from accounts.forms import CommentForm
from taggit.models import Tag
from django.core.mail import send_mail
import requests


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HomeView(ListView):
    model = Post
    template_name = 'tech-index.html'
    paginate_by = 7

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        #currency exchange
        url = f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url)
        data = response.json()
        all_values = [ i['CcyNm_UZ'] for i in data ] #hamma dictlar ichidan shu keyni ovotti
        uz = [ i['Rate'] for i in data ] #hamma dictlar ichidan shu keyni ovotti
        m = [all_values[n] for n in (0,1,2,3,4,12,14,35)] #dicni indexini oldi
        n = [uz[n] for n in (0,1,2,3,4,12,14,35)] #dicni indexini oldi
        pd = {m[i]: n[i] for i in range(len(m))} # bitta dictionaryga qoyvoldi 

        context.update({
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
            'pd': pd,
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
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # adding like count
        like_status = False
        ip = get_client_ip(request)
        try:
            if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
                like_status = True
            else:
                like_status = False
        except IpModel.DoesNotExist:
            ip = None

        context['like_status'] = like_status

        return self.render_to_response(context)
    

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

        #currency exchange
        url = f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url)
        data = response.json()
        all_values = [ i['CcyNm_UZ'] for i in data ] #hamma dictlar ichidan shu keyni ovotti
        uz = [ i['Rate'] for i in data ] #hamma dictlar ichidan shu keyni ovotti
        m = [all_values[n] for n in (0,1,2,3,4,12,14,35)] #dicni indexini oldi
        n = [uz[n] for n in (0,1,2,3,4,12,14,35)] #dicni indexini oldi
        pd = {m[i]: n[i] for i in range(len(m))} # bitta dictionaryga qoyvoldi 

        context.update({
            'similar_posts':similar_posts,
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
            'comments': comments,
            'pd': pd,
            })

        return context   


def post_like(request, year, month, day, slug):
    post = Post.objects.get(slug=slug)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('article-detail', args=[year, month, day, slug]))


def AboutView(request): 
    if request.method == "POST":
        contact = Contact()
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_number = request.POST['message-number']
        message = request.POST['message']
        
        # send an email
        send_mail(
            message_name, #subject
            message, #message
            message_email, #from email
            ['iamshokhjahon@gmail.com'], #to email , kop yozish un vergul qoyb yozb keturasan
            fail_silently=False,
        )

        contact.name = message_name    # 113-116 databasega save qilish uchun 
        contact.email = message_email
        contact.message = message
        contact.save()

        return redirect('contact_success')
    else:
        return render(request, 'about.html', {})


def ContactSucessView(request): 
    return render(request, 'contact_success.html')









































  