from django.conf.urls.defaults import patterns, include, url

import bwapp.forms as f

urlpatterns = patterns('bwapp.views',
    url(r'^$', 'index', name='bw_index'),
    url(r'^projects/(?P<project_id>\d+)/$', 'project_detail', name="project_detail"),
    
    url(r'^projects/add/$', 'project_add_begin', name="project_add_begin"),
    url(r'^projects/add/step/(?P<step>1)/$', 'project_add_general', name="add_project_1"),
    url(r'^projects/add/step/(?P<step>2)/$', 'project_add_location', name="add_project_2"),
    url(r'^projects/add/step/(?P<step>3)/$', 'project_add_climate', name="add_project_3"),
    url(r'^projects/add/step/(?P<step>4)/$', 'project_add_orgs', name="add_project_4"),
    url(r'^projects/add/step/(?P<step>5)/$', 'project_add_community', name="add_project_5"),
    url(r'^projects/add/step/(?P<step>6)/$', 'project_add_geoconds', name="add_project_6"),
    url(r'^projects/add/step/(?P<step>7)/$', 'project_add_humres', name="add_project_7"),
    url(r'^projects/add/step/(?P<step>8)/$', 'project_add_contacts', name="add_project_8"),
    url(r'^projects/add/step/9/$', 'project_add_end', name="add_project_9"),

)
