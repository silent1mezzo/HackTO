from django.conf.urls.defaults import *

urlpatterns = patterns('eats.views',
    url(r'^$', 'index', name='index'),
	(r'^search/json/$', 'search_json', {}, 'search_json'),    
)
