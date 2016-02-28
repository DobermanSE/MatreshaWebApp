from django.conf.urls import url
from django.contrib.auth import views as auth_views
from apps.accounts.views import *

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/'},
        name='logout'),

    url(r'^registration/$', register_user,
        name='registration'),

    url(r'^seller_registration/$', register_user, {'seller': True}),

    url(r'^confirm/(?P<activation_key>\w+)/', register_confirm),

    url(r'^password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect': '/accounts/password/reset/done/', 'template_name': 'password_reset_form.html',
         'email_template_name': 'password_reset_email.html'},
        name="password_reset"),

    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'password_reset_done.html'}),

    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': '/accounts/password/done/', 'template_name': 'password_reset_confirm.html'},
        name="password_reset_confirm"),

    url(r'^password/done/$',
        auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'}),
]