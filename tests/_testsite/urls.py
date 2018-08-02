import django
from django.conf.urls import include, url
from django.contrib import admin

from . import views


included_urlpatterns = [
    url(r'^test/(\d+)/foo/(\w+)/bar/$', views.dummy, name='included_test_with_args'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dummy/$', views.dummy, name='dummy'),
    url(r'^dummy/(\d+)/foo/(\w+)/bar/$', views.dummy, name='dummy_with_args'),
    url(r'^dummy/(?P<pk1>\w+)/foo/(?P<pk2>\d+)/bar/$', views.dummy, name='dummy_with_kwargs'),
    url(r'^dummy/(\d+)/fooo?/baa?r/$', views.dummy, name='dummy_with_optional_character'),
    url(r'^dummy/(\d+)/foo(?:bar)?/$', views.dummy, name='dummy_with_optional_group'),
    url(r'^dummy/(\d+)/(?:/(?P<op>[a-zA-Z]+)/)?/$', views.dummy, name='dummy_with_optional_kwarg'),
    url(r'^included/(?P<pk1>\w+)/', include(included_urlpatterns)),
]

if django.VERSION >= (2, 0):
    from django.urls import path, re_path
    urlpatterns += [
        path('articles/<int:year>/', views.dummy, name='articles_with_path'),
        path('articles/<int:year>/<int:month>/', views.dummy, name='articles_with_paths'),
        re_path(r'articles/(?P<year>[0-9]{4})/$', views.dummy, name='articles_with_re_path'),
        path('articles/<slug>/', views.dummy, name='articles_with_path_without_converter'),
    ]
