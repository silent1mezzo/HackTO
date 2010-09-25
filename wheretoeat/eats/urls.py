from django.conf.urls.defaults import *

urlpatterns = patterns('eats.views',
    url(r'^$', 'index', name='index'),
	url(r'^search/$', 'search', name='search'),
	(r'^search/json/$', 'search_json', {}, 'search_json'),
    
)
