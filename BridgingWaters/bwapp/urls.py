from django.conf.urls.defaults import patterns, include, url

import bwapp.forms as f

urlpatterns = patterns('bwapp.views',
    url(r'^$', 'index', name='index'),
    url(r'^projects/(?P<project_id>\d+)/$', 'project_detail'),
    url(r'&projects/submitted/$', 'project_submitted'),
    
    url(r'^projects/add/$', 'project_add_begin'),
    url(r'^projects/add/step/1/$', 'project_add_step1'),
    url(r'^projects/add/step/2/$', 'project_add_step2'),
    url(r'^projects/add/step/3/$', 'project_add_step3'),
    url(r'^projects/add/step/4/$', 'project_add_step4'),
    url(r'^projects/add/step/5/$', 'project_add_step5'),
    url(r'^projects/add/step/6/$', 'project_add_step6'),
    url(r'^projects/add/step/7/$', 'project_add_step7'),
    url(r'^projects/add/step/8/$', 'project_add_step8'),
)
