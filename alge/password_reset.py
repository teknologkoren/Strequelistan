from django.conf.urls import url
import django.contrib.auth.views as password_views

# TODO: Don't reach into another app to pick password templates.
urlpatterns = [
    url(r'^reset/$',
        password_views.password_reset,
        {'post_reset_redirect' : '/user/password/reset/done/',
         'template_name': 'strecklista/password_reset_form.html'},
        name="password_reset"),

    url(r'^reset/done/$',
        password_views.password_reset_done,
        {'template_name': 'strecklista/password_reset_done.html'}),

    url(r'^reset/(?P<uidb64>([0-9A-Za-z]+)?)-(?P<token>(.+)?)/$',
        password_views.password_reset_confirm,
        {'post_reset_redirect' : '/lista/login',
         'template_name': 'strecklista/password_reset_form.html'},
        name='password_reset_confirm'),

    url(r'^done/$',
        password_views.password_reset_complete,
        {'template_name': 'strecklista/password_reset_complete.html'}),
]
