import bwapp.models

def process_project_add_general(project, form):
    project.reviewed = False
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
    
def process_project_add_location(project, location, form):
    location.project = project
        
    location.country = form.cleaned_data['country']
    location.name = form.cleaned_data['name']
    
    code_region = bwapp.models.CodeRegion.objects.get(
        pk=form.cleaned_data['region'])
    location.region = code_region
    
    location.latitude = form.cleaned_data['latitude']
    location.longitude = form.cleaned_data['longitude']
    
    code_elev = bwapp.models.CodeElevation.objects.get(
        pk=form.cleaned_data['elevation'])
    location.elevation = code_elev
    
    code_topo = bwapp.models.CodeTopography.objects.get(
        pk=form.cleaned_data['topography'])
    location.topography = code_topo
    
    location.description = form.cleaned_data['description']
    
    location.save()

def process_project_add_climate(project, climate, form):
    climate.project = project
    
    code_clim_zone = bwapp.models.CodeClimateZone.objects.get(
        pk=form.cleaned_data['climate_zone'])
    climate.climate_zone = code_clim_zone
    
    code_precip = bwapp.models.CodePrecipLevel.objects.get(
        pk=form.cleaned_data['precipitation']
    )
    climate.precipitation = code_precip
    
    climate.has_rainy_season = form.cleaned_data['has_rainy_season']
    climate.rainy_months = form.cleaned_data['rainy_months']
    
    climate.save()

def process_project_add_community(project, comm, form):
    comm.project = project
    
    code_urban_rural = bwapp.models.CodeUrbanRural.objects.get(
        pk=form.cleaned_data['urban_rural'])
    comm.urban_rural = code_urban_rural
    
    comm.description = form.cleaned_data['description']
    
    code_num_ppl = bwapp.models.CodePplServed.objects.get(
        pk=form.cleaned_data['num_ppl_served'])
    comm.num_ppl_served = code_num_ppl
    
    comm.community_size = form.cleaned_data['community_size']
    
    code_water_mgmt = bwapp.models.CodeWaterMgmtLevel.objects.get(
        pk=form.cleaned_data['water_mgmt_level'])
    comm.water_mgmt_level = code_water_mgmt
    
    comm.save()
    