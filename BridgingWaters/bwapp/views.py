from django.shortcuts import render, get_object_or_404, get_list_or_404
from bwapp.models import NewsUpdate, FeaturedProject, Project
from random import choice

def index(request):
    latest_news_list = NewsUpdate.objects.all().order_by('-created')[:5]
    featured_proj_list = FeaturedProject.objects.all()
    rand_feat_proj = choice(featured_proj_list)
    return render(request, 'bwapp/index.html', {
        'latest_news_list':latest_news_list,
        'rand_feat_proj':rand_feat_proj
        })
    
def project_detail(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    return render(request, 'bwapp/project_detail.html',
                  {'project':p})