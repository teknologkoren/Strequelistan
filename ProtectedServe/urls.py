from django.conf.urls import url


from . import views

app_name = 'ProtectedServe'

urlpatterns = [
    # ex: /lista/
    url(r'^protected/(?P<file>.*)$', views.protectedFileServe, name='serve_protected_document'),

]
