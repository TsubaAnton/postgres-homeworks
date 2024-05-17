from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Newsletter, Client, Message, Logs
from .forms import ClientForm, MessageForm, NewsletterForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404


class HomePageView(TemplateView):
    template_name = 'base.html'


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = 'newsletter/newsletter_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Newsletter.objects.all()
        return Newsletter.objects.filter(owner=self.request.user)


class NewsletterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Newsletter
    permission_required = 'view_all_newsletter'
    template_name = 'newsletter/newsletter_detail.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Newsletter.objects.all()
        return Newsletter.objects.filter(owner=self.request.user)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    # reverse_lazy в 'Newsletter:list'
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('service:newsletter')
    template_name = 'newsletter/newsletter_form.html'

    def get_object(self, queryset=None):
        if self.request.get.user.is_staff:
            return get_object_or_404(Newsletter, pk=self.kwargs['pk'])
        return get_object_or_404(Newsletter, pk=self.kwargs['pk'], owner=self.request.user)


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    # reverse_lazy в 'Newsletter:list'
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('service:newsletter')
    template_name = 'newsletter/newsletter_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    # reverse_lazy в 'Newsletter:list'
    model = Newsletter
    permission_required = 'deactivate_newsletter'
    success_url = reverse_lazy('service:newsletter')
    template_name = 'newsletter/newsletter_confirm_delete.html'

    def get_object(self, queryset=None):
        if self.request.user.is_staff:
            return get_object_or_404(Newsletter, pk=self.kwargs['pk'])
        return get_object_or_404(Newsletter, pk=self.kwargs['pk'], owner=self.request.user)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/client_list.html'
    permission_required = 'view_user_list'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client/client_detail.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    # reverse_lazy в Client:list
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:client')
    template_name = 'client/client_form.html'

    def get_object(self, queryset=None):
        if self.request.user.is_staff:
            return get_object_or_404(Client, pk=self.kwargs['pk'])
        return get_object_or_404(Client, pk=self.kwargs['pk'], owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    # reverse_lazy в Client:list
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:client')
    template_name = 'client/client_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    # reverse_lazy в Client:list
    model = Client
    success_url = reverse_lazy('service:client')
    template_name = 'client/client_confirm_delete.html'

    def get_object(self, queryset=None):
        if self.request.user.is_staff:
            return get_object_or_404(Client, pk=self.kwargs['pk'])
        return get_object_or_404(Client, pk=self.kwargs['pk'], owner=self.request.user)


class MessageListview(ListView):
    model = Message
    template_name = 'message/message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/message_detail.html'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message')
    template_name = 'message/message_form.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message')
    template_name = 'message/message_form.html'


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('service:message')
    template_name = 'message/message_confirm_delete.html'


class LogsCreateView(CreateView):
    model = Logs

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs
    template_name = 'logs/logs_list.html'
    success_url = reverse_lazy('servise:logs')

    def get_queryset(self):
        return Logs.objects.filter(user=self.request.user)
