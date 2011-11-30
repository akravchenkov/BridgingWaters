from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:


urlpatterns = patterns('bwapp.views',
    url(r'^$', 'index', name='index')
)
