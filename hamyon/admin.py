from django.contrib import admin
from .models import Post, Category, Profile, Comment
# Register your models here.

#class CustomUserAdmin(UserAdmin):
#    model = Big_Pic

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'body')
    actions = ['approve_comments']
    
