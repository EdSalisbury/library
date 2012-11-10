from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^books', include('book.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'library.views.index'),
    url(r'^login', 'library.views.user_login'),
    url(r'^logout', 'library.views.user_logout'),
)
