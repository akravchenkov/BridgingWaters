import datetime

from django import forms
# Use FormWizard to split form across multiple pages
# https://docs.djangoproject.com/en/1.3/ref/contrib/formtools/form-wizard/
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from bwapp.models import (CodeProjType, CodeElevation, CodeRegion,
                          CodeTopography, CodeClimateZone, CodePrecipLevel)
from django_countries import countries

now = datetime.datetime.now()
YEARS = [str(i) for i in range(1980,now.year+1)]

PROJ_TYPES = [(cpt.code, cpt.value) for cpt in CodeProjType.objects.all()]
ELEVATIONS = [(e.code, e.value) for e in CodeElevation.objects.all()]
REGIONS = [(r.code, r.value) for r in CodeRegion.objects.all()]
TOPOGRAPHIES = [(t.code, t.value) for t in CodeTopography.objects.all()]
CLIM_ZONES = [(cz.code, cz.value) for cz in CodeClimateZone.objects.all()]
PRECIPS = [(p.code, p.value) for p in CodePrecipLevel.objects.all()]
MONTHS = ((1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),
    (6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),
    (11,'November'),(12,'December'),)

class ProjectGeneralForm(forms.Form):
    #general
    title = forms.CharField(max_length=256)
    description = forms.CharField(widget=forms.Textarea)
    start_date = forms.DateField(widget=SelectDateWidget(years=YEARS))
    end_date = forms.DateField(widget=SelectDateWidget(years=YEARS))
    goal = forms.CharField(max_length=768, label='Project Goal')
    proj_mgmt = forms.CharField(widget=forms.Textarea,
                                label='Project Management Description',
                                help_text='Describe how your project was managed.')
    proj_type = forms.MultipleChoiceField (
        widget=forms.CheckboxSelectMultiple,
        label='Project Type',
        help_text='Select all that apply.',
        choices=PROJ_TYPES)
    
class ProjectLocationForm(forms.Form):
    #location
    country = forms.ChoiceField(widget=forms.Select,
        choices=countries.COUNTRIES)
    name = forms.CharField(max_length=60, label='Location Name')
    region = forms.ChoiceField(widget=forms.Select, choices=REGIONS)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    #TODO: ?have region automatically populate in the db, based on country?
    elevation = forms.ChoiceField(widget=forms.Select, choices=ELEVATIONS)
    topography = forms.ChoiceField(widget=forms.Select, choices=TOPOGRAPHIES)
    description = forms.CharField(widget=forms.Textarea, required=False,
                                  help_text='Describe the location.')
    

class ProjectClimateForm(forms.Form):
    #climate
    climate_zone = forms.ChoiceField(widget=forms.Select, choices=CLIM_ZONES)
    precipitation = forms.ChoiceField(widget=forms.Select, choices=PRECIPS)
    has_rainy_season = forms.ChoiceField(widget=forms.Select,
                            choices=(('False','No'),('True','Yes')))
    rainy_months = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=MONTHS, required=False)
    
class ProjectOrgForm(forms.Form):
    #organizations -- need to be able to add multiple
    #-- try using formset?
    #-- https://docs.djangoproject.com/en/1.3/topics/forms/formsets/
    name = forms.CharField(max_length=40, label='Involved Organization Name')
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    add_street1 = forms.CharField(max_length=80, label="Street Address")
    add_street2 = forms.CharField(max_length=80, label="Street Address 2",
                                  required=False)
    add_city = forms.CharField(max_length=80, label="City")
    add_state_prov = forms.CharField(max_length=30, label="State/Province")
    add_code = forms.CharField(max_length=20, label="Postal Code")
    add_country = forms.ChoiceField(widget=forms.Select, label="Country",
                                    choices=countries.COUNTRIES)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    
class ProjectFormWizard(FormWizard):
    def done(self, request, form_list):
        save_project(form_list)
        return HttpResponseRedirect('/bw/projects/submitted/')
        
def save_project(form_list):
    pass
