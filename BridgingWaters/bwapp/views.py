import bwapp.models
import bwapp.forms
import bwapp.helpers as helpers

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
#TODO: Project_add_files and pictures
#TODO: Way to go back to previous form steps and pull correct data from db

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
    return redirect(project_add_general, step=1)
    
def project_add_general(request, step):
    if request.method == "POST":

        if 'project' in request.session:
            project = request.session['project']
        
        form = bwapp.forms.ProjectForm(request.POST, instance=project)
        
        if form.is_valid():
            project = form.save()
    
            #Save the new project into session
            request.session['project'] = project 
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Project details saved.')
            #TODO: Reset button
            
    else:
        form = bwapp.forms.ProjectForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Basic Information',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_location(request, step):
    if request.method == "POST":
        project = request.session['project']
        
        try: #TODO: best way to do this?
            loc = bwapp.models.Location.objects.get(project=project.pk)
        except: 
            loc = bwapp.models.Location(project=project) #need to instantiate the new location with the project
        
        form = bwapp.forms.LocationForm(request.POST, instance=loc)
        
        if form.is_valid():
            form.save()
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Location details saved.')
            #TODO: Reset button
    else:
        form = bwapp.forms.LocationForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Project Location',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_climate(request, step):
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = bwapp.forms.ProjectClimateForm(request.POST)
        
        if form.is_valid():
            project = request.session['project']
            
            try:
                climate = bwapp.models.Climate.objects.get(project=project.pk)
            except:
                climate = bwapp.models.Climate()
            
            helpers.process_project_add_climate(project, climate, form)
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Location details saved.')
            #TODO: Reset button
    else:
        form = bwapp.forms.ProjectClimateForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Climate Details',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_orgs(request, step):
    #organizations
    ProjectOrgFormSet = formset_factory(bwapp.forms.ProjectOrgForm, max_num=5,
                                        can_delete=False)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectOrgFormSet(request.POST)
        if formset.is_valid():
           
            #Need to go through each form in the formset
            # get the list of orgs associated with the project
            # try to find the current org in the list of orgs
            # if it is not there, add it
            # if there is one there that has been removed, remove it.
            
            project = request.session['project']
            
            org_list = bwapp.models.Organization.objects.filter(
                project__pk=project.pk)
            
            for form in formset:
                #try:
                #    org_list 
                #except:
                org = bwapp.models.Organization()
                
                
                
                helpers.process_project_add_organization(project, org, form)
                
            #for form in formset.deleted_forms:
                #TODO: if an org was removed, then remove it from db
            #    pass
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Location details saved.')
            #TODO: Reset button
    else:
        formset = ProjectOrgFormSet()

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Involved Organizations',
        'step':step,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Involved Organization Information"
        })

def project_add_community(request, step):
    #community
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = bwapp.forms.ProjectCommunityForm(request.POST)
        
        if form.is_valid():
            project = request.session['project']
            
            try:
                comm = bwapp.models.CommunityInfo.objects.get(project=project.pk)
            except:
                comm = bwapp.models.CommunityInfo()
            
            helpers.process_project_add_community(project, comm, form)
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Location details saved.')
            #TODO: Reset button
    else:
        form = bwapp.forms.ProjectCommunityForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Community Information',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })
    
def project_add_geoconds(request, step):
    #geological conditions
    if request.method == "POST":
        #Process, save in session, and redirect to next
        form = bwapp.forms.ProjectGeoCondsForm(request.POST)
        
        if form.is_valid():
            request.session['geo_form'] = form
            return redirect(project_add_contacts)
    else:
        form = bwapp.forms.ProjectGeoCondsForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Geological Conditions',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })
    
def project_add_humres(request, step):
    #human resource contacts
    ProjectHumResFormSet = formset_factory(bwapp.forms.ProjectHumanResForm,
                                           max_num=5, can_delete=False)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectHumResFormSet(request.POST)
        if formset.is_valid():
            humres_form_list = [form for form in formset]
            request.session['humres_form_list'] = humres_form_list
            return redirect(project_add_contacts)
    else:
        formset = ProjectHumResFormSet()

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Human Resources',
        'step':step,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Human Resources Contact Information"
        })
    
def project_add_contacts(request, step):
    #contacts
    ProjectContactFormSet = formset_factory(bwapp.forms.ProjectContactsForm,
                                            max_num=5, can_delete=False)
    
    if request.method == "POST":
        #Process, save in session, and redirect to next
        formset = ProjectContactFormSet(request.POST)
        if formset.is_valid():
            contact_form_list=[form for form in formset]
            request.session['contact_form_list'] = contact_form_list
            return redirect(project_add_process_all)
    else:
        formset = ProjectContactFormSet()

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Project Contacts',
        'step':step,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Contact Information"
        })

def project_add_end(request):
    #TODO: Redirect to some project preview page and flash a message
    #return render(request, 'bwapp/project_submitted.html')
    return redirect(index) 
