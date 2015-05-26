# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',  # noqa
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # API URLs

    # Token Authentication
    url(r'^api/v1/auth/', obtain_auth_token),

    # Users endpoints
    url(r'^api/v1/users/', include("users.urls", namespace="users")),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
