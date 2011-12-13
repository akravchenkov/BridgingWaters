import bwapp.models
import bwapp.forms as f

from django.shortcuts import (render, get_object_or_404,
                              get_list_or_404, redirect)
from django.forms.formsets import formset_factory
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

def project_add_begin(request):
    #TODO: check session, logged in, etc.
    return redirect(project_add_step1)
    
def project_add_step1(request):
    if request.method == "POST":
        pass #TODO: Process, save in session, and redirect to next
    else:
        form = f.ProjectGeneralForm()
        return render(request, 'forms/project_add_basic.html', {
            'step_title':'Basic Information',
            'step':1,
            'step_count':5,
            'form':form
            })

def project_add_step2(request):
    if request.method == "POST":
        pass #TODO: Process, save in session, and redirect to next
    else:
        form = f.ProjectLocationForm()
        return render(request, 'forms/project_add_basic.html', {
            'step_title':'Project Location',
            'step':2,
            'step_count':5,
            'form':form
            })

def project_add_step3(request):
    if request.method == "POST":
        pass #TODO: Process, save in session, and redirect to next
    else:
        form = f.ProjectClimateForm
        return render(request, 'forms/project_add_basic.html', {
            'step_title':'Climate',
            'step':3,
            'step_count':5,
            'form':form
            })

def project_add_step4(request):
    if request.method == "POST":
        pass #TODO: Process, save in session, and redirect to next
    else:
        ProjectOrigFormSet = formset_factory(f.ProjectOrgForm)

        #TODO: Formset, javascript to create additional forms
        return render(request, 'forms/project_add_orgs.html', {
            'step_title':'Involved Organizations',
            'step':4,
            'step_count':5,
            'formset':ProjectOrigFormSet
            })

def project_add_step5(request):
    pass

def project_submitted(request):
    #TODO: get recently submitted project information
    
    return render(request, 'bwapp/project_submitted.html')