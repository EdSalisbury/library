from django.conf.urls import patterns, include, url

urlpatterns = patterns('videogame.views',
    url(r'^$', 'list'),
    url(r'^/(?P<videogame_id>\d+)$', 'view'),
    url(r'^/(?P<videogame_id>\d+)/edit$', 'edit'),
    url(r'^/add$', 'add'),
    url(r'^/mass_add$', 'mass_add'),
)
