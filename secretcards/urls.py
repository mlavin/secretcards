"""Secret Cards URL Configuration"""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new/$', views.MessageAddView.as_view(), name='add-message'),
    url(r'^i/(?P<slug>[0-9a-f]{16})/$',
        views.MessageDetailView.as_view(), name='message-detail'),
    url(r'^i/(?P<slug>[0-9a-f]{16})\.png$',
        views.MessageDetailView.as_view(content_type='image/png'), name='message-image'),
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^', views.HomepageView.as_view(), name='home'),
]
