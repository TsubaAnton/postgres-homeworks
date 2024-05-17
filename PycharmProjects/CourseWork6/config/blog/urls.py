from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import BlogConfig
from .views import BlogListView, BlogCreateView, BlogUpdateView, BlogDetailView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(BlogListView.as_view()), name='blog'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/update', BlogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>', cache_page(10)(BlogDetailView.as_view()), name='blog_detail'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='blog_confirm_delete'),
]
