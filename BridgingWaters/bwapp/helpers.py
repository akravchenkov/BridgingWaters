import bwapp.models


    
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