from django.contrib import admin
from .models import Post, Category, Profile, Comment, Contact, IpModel
# Register your models here.

#class CustomUserAdmin(UserAdmin):
#    model = Big_Pic

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(IpModel)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'body')
    actions = ['approve_comments']
    
