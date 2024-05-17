from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import ServiceConfig
from .views import (HomePageView, ClientListView, ClientCreateView, ClientDeleteView, ClientDetailView,
                    ClientUpdateView, MessageListview, MessageCreateView, MessageUpdateView, MessageDetailView,
                    MessageDeleteView, NewsletterListView, NewsletterCreateView, NewsletterUpdateView,
                    NewsletterDetailView, NewsletterDeleteView, LogsListView)

app_name = ServiceConfig.name

urlpatterns = [
    path('', cache_page(60)(HomePageView.as_view()), name='homepage'),
    path('client/', ClientListView.as_view(), name='client'),
    path('client/create', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', MessageListview.as_view(), name='message'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('newsletter/', NewsletterListView.as_view(), name='newsletter'),
    path('newsletter/create', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/update', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletter/delete/<int:pk>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('logs/', LogsListView.as_view(), name='logs'),
]