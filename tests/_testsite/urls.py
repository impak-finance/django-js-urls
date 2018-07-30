from django.conf.urls import url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dummy/$', views.dummy, name='dummy'),
    url(r'^dummy/(\d+)/foo/(\d+)/bar/$', views.dummy, name='dummy_with_args'),
]
