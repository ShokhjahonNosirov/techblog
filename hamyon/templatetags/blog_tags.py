from django import template
from ..models import Post
from ..views import ArticleDetailView
from django.db.models import Count


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()

    