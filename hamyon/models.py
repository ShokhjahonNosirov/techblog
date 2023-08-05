from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
#from datetime import datetime, date
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager


class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip
    

class Category(models.Model):
    name = models.CharField(max_length=255) 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home') 

class Profile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE) #, related_name = "user" 
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    telegram_url = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.user)
   
    def get_absolute_url(self):
        #return reverse('article-detail', args = (str(self.id)))
        return reverse('home')     
    


class Post(models.Model, HitCountMixin):
    post_title = models.CharField(max_length = 255, default = '')
    slug = models.SlugField(max_length=250, unique_for_date='publish', unique=True)
    header_image = models.ImageField(null=False, blank=False, upload_to = 'images/', default= '')
    post_author = models.ForeignKey(User, on_delete = models.CASCADE, default = 'admin')
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True) #created
    publish = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, related_name = "categories", on_delete = models.CASCADE)
    snippet = models.CharField(max_length=700)      
    tags = TaggableManager()
    likes = models.ManyToManyField(IpModel, related_name="post_likes", blank=True) #new 
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )


    def get_absolute_url(self):
        return reverse("article-detail", 
                        args=[self.publish.year,
                        self.publish.month,
                        self.publish.day, self.slug])

    def current_hit_count(self):
        return self.hit_count.hits


    def total_views(self):
        return self.views.count()
    
    def __str__(self):
        return self.post_title + ' | ' + str(self.post_author)
    
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ('-publish',)

class Comment(models.Model):
    post = models.ForeignKey(Post, 
                            on_delete=models.CASCADE, 
                            related_name = 'comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Contact(models.Model):
    name = models.CharField(max_length=158)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name