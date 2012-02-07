import bwapp.models
import bwapp.forms
import bwapp.helpers as helpers

from django.shortcuts import (render, get_object_or_404,
                              get_list_or_404, redirect)
from django.forms.models import modelformset_factory
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
#TODO: How to make refresh on an Add page not re-add item to the database.

def index(request):
    latest_news_list = \
        bwapp.models.NewsUpdate.objects.all().order_by('-created')[:5]
    featured_proj_list = bwapp.models.FeaturedProject.objects.all()
    feat_proj = choice(featured_proj_list)
    
    return render(request, 'index.html', {
        'latest_news_list':latest_news_list,
        'feat_proj':feat_proj.project,
        })
    
def project_detail(request, project_id):
    p = get_object_or_404(bwapp.models.Project, pk=project_id)
    comm_info = p.communityinfo_set.all()[0]
    return render(request, 'project_detail.html',{
        'p': p
        })

def browse_projects(request):
    
    return render(request, 'browse_projects.html')

def project_add_begin(request):
    #TODO: check session, logged in, etc.
    return redirect(project_add_general, step=1)
    
def project_add_general(request, step):
    if 'project' in request.session:
        project = request.session['project']
    else:
        project = None
    
    if request.method == "POST":
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
        form = bwapp.forms.ProjectForm(instance=project)
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Basic Information',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_location(request, step):
    project = request.session['project'] #TODO: redirect to beginning of add process, display error message
    try:
        loc = bwapp.models.Location.objects.get(project=project)
    except:
        loc = bwapp.models.Location(project=project)
    
    if request.method == "POST":
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
        form = bwapp.forms.LocationForm(instance=loc)
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Project Location',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_climate(request, step):
    project = request.session['project'] #TODO: redirect to beginning of add process, display error message
    try:
        climate = bwapp.models.Climate.objects.get(project=project)
    except:
        climate = bwapp.models.Climate(project=project)
    
    if request.method == "POST": 
        form = bwapp.forms.ClimateForm(request.POST, instance=climate)
        
        if form.is_valid():
            form.save()
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Climate details saved.')
            #TODO: Reset button
    else:
        form = bwapp.forms.ClimateForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Climate Details',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })

def project_add_community(request, step):
    project = request.session['project'] #TODO: redirect to beginning of add process, display error message
    try:
        comm = bwapp.models.CommunityInfo.objects.get(project=project)
    except:
        comm = bwapp.models.CommunityInfo(project=project)
    
    if request.method == "POST": 
        form = bwapp.forms.CommunityInfoForm(request.POST, instance=comm)
        
        if form.is_valid():
            form.save()
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Community details saved.')
            #TODO: Reset button
    else:
        form = bwapp.forms.CommunityInfoForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Community Information',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })
    
def project_add_geoconds(request, step):
    project = request.session['project'] #TODO: redirect to beginning of add process, display error message
    
    try:
        geoconds = bwapp.models.GeoConditions.objects.get(project=project)
    except:
        geoconds = bwapp.models.GeoConditions(project=project)
    
    if request.method == "POST": 
        form = bwapp.forms.GeoConditionsForm(request.POST, instance=geoconds)
        
        if form.is_valid():
            form.save()
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Geological conditions details saved.')
            #TODO: Reset button
    else:
        form = bwapp.forms.GeoConditionsForm()
        
    return render(request, 'forms/project_add_basic.html', {
        'step_title':'Geological Conditions',
        'step':step,
        'step_count':STEP_COUNT,
        'form':form
        })
        
def project_add_orgs(request, step):
    OrganizationFormSet = modelformset_factory(
        bwapp.models.Organization,
        form=bwapp.forms.OrganizationForm, 
        max_num=5,
        can_delete=False)
    
    project = request.session['project'] #TODO: redirect to beginning of add process, display error message
    
    if request.method == "POST":
        formset = OrganizationFormSet(request.POST, 
            queryset=bwapp.models.Organization.objects.filter(project__pk=project.pk))
        
        if formset.is_valid():
            organizations = formset.save(commit=False) #TODO: Need to set the project into each organization
            # or the save will fail (same for other formsets).
            # maybe custom instantiation method or something?
            for org in organizations:
                org.project = project
                org.save()
            #for form in formset.deleted_forms:
                #TODO: if an org was removed, then remove it from db
            #    pass
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Organization details saved.')
            #TODO: Reset button
    else:
        formset = OrganizationFormSet(
            queryset=bwapp.models.Organization.objects.filter(project__pk=project.pk))

    return render(request, 'forms/project_add_formset.html', {
        'step_title':"Involved Organizations",
        'step':step,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Involved Organization Information"
        })
    
def project_add_humres(request, step):
    HumanResFormSet = modelformset_factory(
        bwapp.models.HumanResContact,
        form=bwapp.forms.HumanResourceContactForm, 
        max_num=5,
        can_delete=False)
    
    project = request.session['project'] #TODO: redirect to beginning of add process, display error message
    
    if request.method == "POST":
        formset = HumanResFormSet(request.POST, 
            queryset=bwapp.models.HumanResContact.objects.filter(project__pk=project.pk))
        
        if formset.is_valid():
            human_res_contacts = formset.save(commit=False) #TODO: Need to set the project into each organization
            # or the save will fail (same for other formsets).
            # maybe custom instantiation method or something?
            for contact in human_res_contacts:
                contact.project = project
                contact.save()
            #for form in formset.deleted_forms:
                #TODO: if a contact was removed, then remove it from db
            #    pass
            
            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Human resource details saved.')
            #TODO: Reset button
    else:
        formset = HumanResFormSet(
            queryset=bwapp.models.HumanResContact.objects.filter(project__pk=project.pk))


    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Human Resources',
        'step':step,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Human Resources Contact Information"
        })
    
def project_add_contacts(request, step):
    ProjectContactFormSet = modelformset_factory(
        bwapp.models.ProjectContact,
        form=bwapp.forms.ProjectContactForm,
        max_num=5, 
        can_delete=False)
    
    project = request.session['project'] #TODO: redirect to beginning of add process, display error message
    
    if request.method == "POST":
        formset = ProjectContactFormSet(request.POST, 
            queryset=bwapp.models.ProjectContact.objects.filter(
                project__pk=project.pk))
        
        if formset.is_valid():
            contacts = formset.save(commit=False) #TODO: Need to set the project into each organization
            # or the save will fail (same for other formsets).
            # maybe custom instantiation method or something?
            for contact in contacts:
                contact.project = project
                contact.save()
            #for form in formset.deleted_forms:
                #TODO: if a contact was removed, then remove it from db
            #    pass

            next_step = int(step)+1
            if "save_and_cont" in request.POST:
                return redirect("add_project_%s" % (next_step), step=next_step)
            else:
                messages.info(request, 'Contact details saved.')
            #TODO: Reset button
    else:
        formset = ProjectContactFormSet(
            queryset=bwapp.models.ProjectContact.objects.filter(
                project__pk=project.pk))

    return render(request, 'forms/project_add_formset.html', {
        'step_title':'Project Contacts',
        'step':step,
        'step_count':STEP_COUNT,
        'formset':formset,
        'legend':"Contact Information"
        })

def project_add_end(request, step):
    #TODO: Redirect to some project preview page and flash a message
    project = request.session['project']
    p = get_object_or_404(bwapp.models.Project, pk=project.id)
    return render(request, 'project_add_submit.html', {
        'p':p
        }) 
