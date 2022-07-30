from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
#from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home') 

class Profile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    telegram_url = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.user)
   
    def get_absolute_url(self):
        #return reverse('article-detail', args = (str(self.id)))
        return reverse('home')     
    


class Post(models.Model, HitCountMixin):
    post_title = models.CharField(max_length = 255, default = '')
    header_image = models.ImageField(null=False, blank=False, upload_to = 'images/', default= '')
    post_author = models.ForeignKey(User, on_delete = models.CASCADE, default = 'admin')
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    #category = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name = "categories", on_delete = models.CASCADE)
    snippet = models.CharField(max_length=255)      
    tags = TaggableManager()
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )



    def current_hit_count(self):
        return self.hit_count.hits


    def total_views(self):
        return self.views.count()
    
    def __str__(self):
        return self.post_title + ' | ' + str(self.post_author)

    class Meta:
        ordering = ('-post_date',)
