from django.urls import path
from .views import HomeView, ArticleDetailView, CategoryView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('category/<int:cats>/', CategoryView, name='category'),
]