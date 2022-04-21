from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
#from datetime import datetime, date
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home') 

class Bigpic(models.Model):
    title = models.CharField(max_length = 255, default = '') #title first picture
    first_pic = models.ImageField(null=False, blank=False, upload_to="images/", default = '') 
    sec_pic1 = models.ImageField(null=False, blank=False, upload_to="images/", default = '') 
    tit_sp1 = models.CharField(max_length = 255, default = '')   # title second picture 1
    second_pic2 = models.ImageField(null=False, blank=False, upload_to="images/", default = '') 
    tit_sp2 = models.CharField(max_length = 255, default = '')  # title second picture 2
    big_ad = models.ImageField(null=False, blank=False, upload_to="images/", default = '') 
    poster = models.ImageField(null=False, blank=False, upload_to="images/", default = '')
    bottom_ad = models.ImageField(null=False, blank=False, upload_to="images/", default = '')
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = 'admin')

    def __str__(self):
        return self.title

class Post(models.Model):
    post_title = models.CharField(max_length = 255, default = '')
    header_image = models.ImageField(null=False, blank=False, upload_to = 'images/', default= '')
    title_tag = models.CharField(max_length=255)
    post_author = models.ForeignKey(User, on_delete = models.CASCADE, default = 'admin')
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    #category = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name = "categories", on_delete = models.CASCADE)
    snippet = models.CharField(max_length=255)      
    
    def __str__(self):
        return self.post_title + ' | ' + str(self.post_author)

    class Meta:
        ordering = ('-post_date',)