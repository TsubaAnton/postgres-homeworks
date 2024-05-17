from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .forms import BlogForm
from .models import Blog
from service.models import Newsletter, Client


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_newsletters'] = Newsletter.objects.count()
        context['active_newsletters'] = Newsletter.objects.filter(status=Newsletter.Status.LAUNCHED).count()
        context['unique_clients'] = Client.objects.distinct().count()
        context['random_articles'] = Blog.objects.filter(is_published=True).order_by('?')[:3]
        return context


class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.add_blog'
    success_url = reverse_lazy('blog:blog')
    template_name = 'blog/blog_form.html'


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.change_blog'
    success_url = reverse_lazy('blog:blog')
    template_name = 'blog/blog_form.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'blog.delete_blog'
    success_url = reverse_lazy('blog:blog')
    template_name = 'blog/blog_confirm_delete.html'
