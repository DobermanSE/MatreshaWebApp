from django.conf.urls import url
from django.contrib.auth import views as auth_views
from apps.accounts.views import *

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/'},
        name='logout'),

    url(r'^registration/$', register_user,
        name='registration'),

    url(r'^confirm/(?P<activation_key>\w+)/', register_confirm),
]