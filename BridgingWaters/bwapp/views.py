import bwapp.models
import bwapp.forms

from django.shortcuts import (render, get_object_or_404,
                              get_list_or_404, redirect)
from django.forms.formsets import formset_factory
from django.contrib import messages

from random import choice

STEP_COUNT = 8

#TODO: If use the save button, save current responses to database, redirect to same form
#TODO: If use the save and continute, save current responses to database, redirect to next form
#TODO: Somehow make sure that when a form is accessed, the previous steps have been completed already
#TODO: Require logon before project adding, tie the entry to user
#TODO: Make an audit table to track stuff

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
        form = bwapp.forms.ProjectGeneralForm(request.POST)
        
        if form.is_valid():
            
            #TODO: Best way to do this?
            if 'project' in request.session:
                project = request.session['project']
            else:
                project = bwapp.models.Project()
            
            project.reviewd = False
            project.title = form.cleaned_data['title']
            project.description = form.cleaned_data['description']
            project.start_date = form.cleaned_data['start_date']
            project.end_date = form.cleaned_data['end_date']
            project.goal = form.cleaned_data['goal']
            project.proj_mgmt = form.cleaned_data['proj_mgmt']
            
            project.save() #Need to save before able to save ManyToMany field
            
            project.proj_types = form.cleaned_data['proj_type']
            #TODO: project.keywords
            project.save()
    
            request.session['project'] = project #Save the new project into session
            
            if "save_and_cont" in request.POST:
                return redirect(project_add_step2)
            else:
                messages.info(request, 'Project details saved.')
            #TODO: Reset button
            
    else:
        form = bwapp.forms.ProjectGeneralForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Basic Information',
        'step':1,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step2(request):
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = bwapp.forms.ProjectLocationForm(request.POST)
        
        if form.is_valid():
            project = request.session['project']
        
            try: #TODO: best way to do this?
                loc = bwapp.models.Location.objects.get(project=project.pk)
            except: 
                loc = bwapp.models.Location()
            
            loc.project = project
        
            loc.country = form.cleaned_data['country']
            loc.name = form.cleaned_data['name']
            
            code_region = bwapp.models.CodeRegion.objects.get(pk=form.cleaned_data['region'])
            loc.region = code_region
            
            loc.latitude = form.cleaned_data['latitude']
            loc.longitude = form.cleaned_data['longitude']
            
            code_elev = bwapp.models.CodeElevation.objects.get(pk=form.cleaned_data['elevation'])
            loc.elevation = code_elev
            
            code_topo = bwapp.models.CodeTopography.objects.get(pk=form.cleaned_data['topography'])
            loc.topography = code_topo
            
            loc.description = form.cleaned_data['description']
            
            loc.save()
            
            if "save_and_cont" in request.POST:
                return redirect(project_add_step3)
            else:
                messages.info(request, 'Location details saved.')
            #TODO: Reset button
    else:
        form = bwapp.forms.ProjectLocationForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Project Location',
        'step':2,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step3(request):
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = bwapp.forms.ProjectClimateForm(request.POST)
        
        if form.is_valid():
            request.session['climate_form'] = form
            return redirect(project_add_step4)
    else:
        form = bwapp.forms.ProjectClimateForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Climate',
        'step':3,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step4(request):
    #organizations
    ProjectOrgFormSet = formset_factory(bwapp.forms.ProjectOrgForm, max_num=5)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectOrgFormSet(request.POST)
        if formset.is_valid():
            org_form_list=[form for form in formset]
            request.session['org_form_list'] = org_form_list
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
        form = bwapp.forms.ProjectCommunityForm(request.POST)
        
        if form.is_valid():
            request.session['community_form'] = form
            return redirect(project_add_step6)
    else:
        form = bwapp.forms.ProjectCommunityForm()
        
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
        form = bwapp.forms.ProjectGeoCondsForm(request.POST)
        
        if form.is_valid():
            request.session['geo_form'] = form
            return redirect(project_add_step7)
    else:
        form = bwapp.forms.ProjectGeoCondsForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Geological Conditions',
        'step':6,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_step7(request):
    #contacts
    ProjectContactFormSet = formset_factory(bwapp.forms.ProjectContactsForm, max_num=5)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectContactFormSet(request.POST)
        if formset.is_valid():
            contact_form_list=[form for form in formset]
            request.session['contact_form_list'] = contact_form_list
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
    ProjectHumResFormSet = formset_factory(bwapp.forms.ProjectHumanResForm, max_num=5)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectHumResFormSet(request.POST)
        if formset.is_valid():
            humres_form_list = [form for form in formset]
            request.session['humres_form_list'] = humres_form_list
            return redirect(project_add_process_all)
    else:
        formset = ProjectHumResFormSet()

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Human Resources',
        'step':8,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Human Resources Contact Information"
        })

def project_add_process_all(request):
    #TODO: Should actually save all this stuff in the DB once each form is submitted
    # but use the Reviewed field to make sure that uncomplete stuff is not used
    general_form = request.session['general_form']
    #location_form = request.session['location_form']
    #climate_form = request.session['climate_form']
    #community_form = request.session['community_form']
    #org_form_list = request.session['org_form_list']
    #geo_conds_form = request.session['geo_form']
    #contact_form_list = request.session['contact_form_list']
    #humres_form_list = request.session['humres_form_list']
    
    project = bwapp.models.Project()
    project.title = general_form.cleaned_data['title']
    project.description = general_form.cleaned_data['description']
    project.start_date = general_form.cleaned_data['start_date']
    project.end_date = general_form.cleaned_data['end_date']
    project.goal = general_form.cleaned_data['goal']
    project.proj_mgmt = general_form.cleaned_data['proj_mgmt']
    #TODO: project.keywords
    project.reviewed = False
    
    project.save()
    
    project.proj_types = general_form.cleaned_data['proj_type']
    project.save()
    
    return redirect(index) #TODO: Redirect to some project preview page
    
    
def project_submitted(request):
    #TODO: get recently submitted project information to display on the page
    return render(request, 'bwapp/project_submitted.html')