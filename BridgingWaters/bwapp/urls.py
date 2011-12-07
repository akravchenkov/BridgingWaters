from django.conf.urls.defaults import patterns, include, url
from bwapp.forms import ProjectForm1, ProjectForm2, ProjectForm3, ProjectWizard


urlpatterns = patterns('bwapp.views',
    url(r'^$', 'index', name='index'),
    url(r'^projects/(?P<project_id>\d+)/$', 'project_detail'),
    url(r'^projects/add/$', ProjectWizard([ProjectForm1, ProjectForm2,
                                          ProjectForm3])),
)
