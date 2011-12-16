import bwapp.models
import bwapp.forms as f

from django.shortcuts import (render, get_object_or_404,
                              get_list_or_404, redirect)
from django.forms.formsets import formset_factory
from random import choice

STEP_COUNT = 8

#TODO: If use the save button, save current responses to database, redirect to same form
#TODO: If use the save and continute, save current responses to database, redirect to next form

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
        #Process, save in session, and redirect to next
        form = f.ProjectGeneralForm(request.POST)
        
        if form.is_valid():
            request.session['general_form'] = form
            return redirect(project_add_step2)
    else:
        form = f.ProjectGeneralForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Basic Information',
        'step':1,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step2(request):
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = f.ProjectLocationForm(request.POST)
        
        if form.is_valid():
            request.session['location_form'] = form
            return redirect(project_add_step3)
    else:
        form = f.ProjectLocationForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Project Location',
        'step':2,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step3(request):
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = f.ProjectClimateForm(request.POST)
        
        if form.is_valid():
            request.session['climate_form'] = form
            return redirect(project_add_step4)
    else:
        form = f.ProjectClimateForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Climate',
        'step':3,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step4(request):
    #organizations
    ProjectOrgFormSet = formset_factory(f.ProjectOrgForm, max_num=5)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectOrgFormSet(request.POST)
        if formset.is_valid():
            request.session['org_formset'] = formset
            return redirect(project_add_step5)
    else:
        formset = ProjectOrgFormSet()

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Involved Organizations',
        'step':4,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Involved Organization Information"
        })

def project_add_step5(request):
    #community
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = f.ProjectCommunityForm(request.POST)
        
        if form.is_valid():
            request.session['community_form'] = form
            return redirect(project_add_step6)
    else:
        form = f.ProjectCommunityForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Community Information',
        'step':5,
        'step_count':STEP_COUNT,
        'form':form
        })
    
def project_add_step6(request):
    #geological conditions
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = f.ProjectGeoCondsForm(request.POST)
        
        if form.is_valid():
            request.session['geo_form'] = form
            return redirect(project_add_step7)
    else:
        form = f.ProjectGeoCondsForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Geological Conditions',
        'step':6,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step7(request):
    #contacts
    ProjectContactFormSet = formset_factory(f.ProjectContactsForm, max_num=5)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectContactFormSet(request.POST)
        if formset.is_valid():
            request.session['contacts_formset'] = formset
            return redirect(project_add_step8)
    else:
        formset = ProjectContactFormSet()

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Project Contacts',
        'step':7,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Contact Information"
        })

def project_add_step8(request):
    #human resource contacts
    ProjectHumResFormSet = formset_factory(f.ProjectHumanResForm, max_num=5)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectHumResFormSet(request.POST)
        if formset.is_valid():
            request.session['humres_formset'] = formset
            return redirect(project_add_step8)
    else:
        formset = ProjectHumResFormSet()

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Human Resources',
        'step':8,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Human Resources Contact Information"
        })
    
    
    
def project_submitted(request):
    #TODO: get recently submitted project information to display on the page
    return render(request, 'bwapp/project_submitted.html')