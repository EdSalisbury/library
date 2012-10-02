from django.conf.urls import patterns, include, url

urlpatterns = patterns('book.views',
    url(r'^$', 'list'),
    url(r'^/(?P<book_id>\d+)$', 'view'),
    url(r'^/(?P<book_id>\d+)/edit$', 'edit'),
    url(r'^/add$', 'add'),
    url(r'^/mass_add$', 'mass_add'),
)
