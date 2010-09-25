from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'eats.views.index', name='index'),
)
