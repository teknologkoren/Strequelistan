"""alge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from .settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^api/', include('api.urls')),

    url(r'^', include('strecklista.urls')),
    url(r'^admin/', admin.site.urls, name="admin"),

    #Login/logout views for browsable api
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Password reset
    url(r'^user/password/', include('alge.password_reset')),

    # Media files
    url(r'^media/', include('ProtectedServe.urls')),
]
