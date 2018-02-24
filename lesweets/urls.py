"""lesweets URL Configuration

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
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^create_mathlib/(?P<category_id>[^/]+)/(?P<story_id>[^/]+)', views.create_mathlib, name='create_mathlib'),
    url(r'^create_jeopardy$', views.create_jeopardy, name='create_jeopardy'),
]

for activity in views.ACTIVITIES:
	urlpatterns.append(path(activity['slug'], activity['view'], name=activity['slug']))
