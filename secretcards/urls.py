"""Secret Cards URL Configuration"""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new/$', views.MessageAddView.as_view(), name='add-message'),
    url(r'^', views.HomepageView.as_view(), name='home'),
]
