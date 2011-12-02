import bwapp.models

from django.shortcuts import render, get_object_or_404, get_list_or_404
from random import choice

def index(request):
    latest_news_list = \
        bwapp.models.NewsUpdate.objects.all().order_by('-created')[:5]
    featured_proj_list = bwapp.models.FeaturedProject.objects.all()
    feat_proj = choice(featured_proj_list)
    loc = feat_proj.project.location_set.all()[0]
    return render(request, 'bwapp/index.html', {
        'latest_news_list':latest_news_list,
        'feat_proj':feat_proj,
        'loc':loc
        })
    
def project_detail(request, project_id):
    p = get_object_or_404(bwapp.models.Project, pk=project_id)
    comm_info = p.communityinfo_set.all()[0]
    loc = p.location_set.all()[0]
    return render(request, 'bwapp/project_detail.html',{
        'p': p,
        'comm_info': comm_info,
        'loc': loc
        })