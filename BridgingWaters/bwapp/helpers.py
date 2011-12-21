import bwapp.models



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
    
def process_project_add_organization(project, org, form):
    org.project = project
    
    org.name = form.cleaned_data['name']
    org.notes = form.cleaned_data['notes']
    org.phone = form.cleaned_data['phone']
    org.email = form.cleaned_data['email']
    org.add_street1 = form.cleaned_data['add_street1']
    org.add_street2 = form.cleaned_data['add_street2']
    org.add_city = form.cleaned_data['add_city']
    org.add_state_prov = form.cleaned_data['add_state_prov']
    org.add_code = form.cleaned_data['add_code']
    org.add_country = form.cleaned_data['add_country']
    org.website = form.cleaned_data['website']
    
    org.save()