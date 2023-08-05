from django.urls import path
from .views import HomeView, ArticleDetailView, CategoryView, AboutView, ContactSucessView, post_like #, LikeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('category/<int:cats>/', CategoryView, name='category'),
    path('about/', AboutView, name='about'),
    path('contact_success/', ContactSucessView, name='contact_success'),
    path('like/<int:year>/<int:month>/<int:day>/<slug:slug>', post_like, name='blog_like'),
    #path('like/<int:year>/<int:month>/<int:day>/<slug:slug>/', LikeView, name='like_post'),
]