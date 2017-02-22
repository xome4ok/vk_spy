"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),

    url(r'^users$', views.users_view, name='users_view'),
    url(r'^users/id(?P<user_id>[0-9]+)/$', views.user_info_view, name='user_info_view'),
    url(r'^api/tracks/start/id(?P<user_id>[0-9]+)$', views.user_start_tracking, name='user_start_tracking'),
    url(r'^api/tracks/stop/id(?P<user_id>[0-9]+)$', views.user_stop_tracking, name='user_stop_tracking'),
    url(r'^secret_form/id(?P<user_id>[0-9]+)$', views.secret_form, name='secret_form'),
    url(r'^users/add$', views.user_start_tracking_by_page_address, name='user_add_by_address'),
    url(r'^api/tracks/id(?P<user_id>[0-9]+)$', views.user_track_json, name='user_track_json'),

]

