from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import Bigpic, Post, Category
# Register your models here.

#class CustomUserAdmin(UserAdmin):
#    model = Big_Pic

admin.site.register(Post)
admin.site.register(Bigpic)
admin.site.register(Category)