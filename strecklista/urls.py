from django.conf.urls import url, include
from django.conf import settings

from django.contrib.auth.views import logout

from . import views

app_name = 'strecklista'

urlpatterns = [
    # The 'pwa.urls' MUST use an empty string as the URL prefix
    url('', include('pwa.urls')),

    # ex: /lista/
    url(r'^untabbed', views.index, name='index_untabbed'),
    url(r'^$', views.tabbed_index, name='index'),
    # url(r'^$', views.index, name='index'),

    url(r'^register', views.register, name='register'),
    url(r'^acceptRegisterRequest', views.acceptRegisterRequest, name='acceptRegister'),
    url(r'^denyRegisterRequest', views.denyRegisterRequest, name='denyRegister'),


    url(r'^login', views.login, name='login'),
    url(r'^profile/(?P<user_id>[0-9]+)', views.profile, name='profile'),
    url(r'^bulkTransactions/', views.bulkTransactions, name='bulkTransactions'),

    url(r'^quote/(?P<quote_id>[0-9]+)', views.singleQuote, name='singleQuote'),
    url(r'^quote/', views.quote, name='quote'),

    url(r'^submitQuote/', views.submitQuote, name='submitQuote'),

    url(r'^heddaHopper/', views.heddaHopper, name='heddaHopper'),

    url(r'^suggestions/', views.suggestion, name='suggestions'),

    url(r'^logout/$', logout, {'next_page': '/'}),

    url(r'^product/', views.product, name='product'),

    url(r'^transaction/', views.transaction, name='transaction'),
    url(r'^transactionHistory/', views.transactionHistory, name='transactionHistory'),
    url(r'^returnTransaction/', views.returnTransaction, name='returnTransaction'),

    url(r'^request_reset/', views.requestPasswordReset, name='requestPasswordReset'),
    url(r'^reset_password/', views.resetPassword, name='resetPassword'),

    url(r'^admintools/', views.admin_tools, name='adminTools'),

    # A printable version of the strecklista.
    url(r'^paperlist/', include('strecklista.paperlist')),

    url(r'^updateProfileImage/', views.updateAvatar, name='updateAvatar'),
]

# If we're debugging, add patterns for all component demos.
if settings.DEBUG:
    from .components import demos
    urlpatterns += [url("_/dev/" + demo.__name__ + "$", demo) for demo in demos]
