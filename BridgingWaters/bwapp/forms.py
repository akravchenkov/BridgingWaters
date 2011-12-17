import datetime

from django import forms
# Use FormWizard to split form across multiple pages
# https://docs.djangoproject.com/en/1.3/ref/contrib/formtools/form-wizard/
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from django_countries import countries
from django.core.exceptions import ValidationError

import bwapp.models as m

now = datetime.datetime.now()
YEARS = [str(i) for i in range(1980,now.year+1)]

EMPTY_CHOICE = (None,'- - - -')

PROJ_TYPES = [(obj.code, obj.value) for obj in m.CodeProjType.objects.all()]

ELEVATIONS = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeElevation.objects.all()]
REGIONS = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeRegion.objects.all()]
TOPOGRAPHIES = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeTopography.objects.all()]
CLIM_ZONES = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeClimateZone.objects.all()]
PRECIP_LEVELS = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodePrecipLevel.objects.all()]
RESOURCES = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeResource.objects.all()]
PROFESSIONS = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeProjType.objects.all()] + [(99,'Other')]
URB_RURAL = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeUrbanRural.objects.all()]
PPL_SERVED = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodePplServed.objects.all()]
WATER_MGMT_LEVELS = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in
    m.CodeWaterMgmtLevel.objects.all()]
SOIL_TYPES = [EMPTY_CHOICE] + [(obj.code, obj.value) for obj in m.CodeSoilType.objects.all()]

YES_NO = [('False','No'),('True','Yes')]

EXISTING_KEYWORDS = [(obj.id, obj.value) for obj in m.Keywords.objects.all()]

MONTHS = ((1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),
    (6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),
    (11,'November'),(12,'December'),)

def validate_select(value): #TODO: Is this the best way to do selects with a blank default option?
    if value=="None":
        raise ValidationError(u'An option must be selected.')
    
class ProjectGeneralForm(forms.Form):
    #general
    title = forms.CharField(max_length=256, 
        widget=forms.TextInput(attrs={'class':'title'}))
    description = forms.CharField(widget=forms.Textarea)
    start_date = forms.DateField(widget=SelectDateWidget(years=YEARS),
        label="Start Date")
    end_date = forms.DateField(widget=SelectDateWidget(years=YEARS),
        label="End Date")
    goal = forms.CharField(max_length=768, label='Project Goal',
        widget=forms.TextInput(attrs={'size':'70'}))
    proj_mgmt = forms.CharField(widget=forms.Textarea,
                                label='Project Management Description',
                                help_text='Describe how your project was managed.')
    proj_type = forms.MultipleChoiceField (
        widget=forms.CheckboxSelectMultiple,
        label='Project Type',
        help_text='Select all that apply. At least one is required.',
        choices=PROJ_TYPES)
        
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if end_date < start_date:
            raise forms.ValidationError(u"End date must be before start date.")
        return end_date
    
class ProjectLocationForm(forms.Form):
    #location
    country = forms.ChoiceField(widget=forms.Select,
        choices=countries.COUNTRIES)
    name = forms.CharField(max_length=60, label='Location Name')
    region = forms.ChoiceField(widget=forms.Select, choices=REGIONS, 
        validators=[validate_select])
    latitude = forms.FloatField() #TODO: Some kind of google map interface to find location?
    longitude = forms.FloatField()
    #TODO: have region automatically populate in the db, based on country?
    elevation = forms.ChoiceField(widget=forms.Select, choices=ELEVATIONS,
        validators=[validate_select])
    topography = forms.ChoiceField(widget=forms.Select, choices=TOPOGRAPHIES,
        validators=[validate_select])
    description = forms.CharField(widget=forms.Textarea, required=False,
                                  help_text='Describe the location.')
    

class ProjectClimateForm(forms.Form):
    #climate
    climate_zone = forms.ChoiceField(widget=forms.Select, choices=CLIM_ZONES,
                                     validators=[validate_select])
    precipitation = forms.ChoiceField(widget=forms.Select,
                                      choices=PRECIP_LEVELS,
                                      validators=[validate_select])
    has_rainy_season = forms.ChoiceField(widget=forms.Select, choices=YES_NO)
    rainy_months = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=MONTHS, required=False)
    
class ProjectOrgForm(forms.Form):
    #organizations
    name = forms.CharField(max_length=40, label='Organization Name', 
        widget=forms.TextInput(attrs={'class':'title'}))
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

class ProjectCommunityForm(forms.Form):
    urban_rural = forms.ChoiceField(widget=forms.Select, choices=URB_RURAL,
        label="Urban/Rural",
        validators=[validate_select])
    description = forms.CharField(widget=forms.Textarea)
    num_ppl_served = forms.ChoiceField(widget=forms.Select, choices=PPL_SERVED,
        label="Number of People Served",
        validators=[validate_select])
    community_size = forms.IntegerField(label="Community Size")
    water_mgmt_level = forms.ChoiceField(widget=forms.Select, choices=WATER_MGMT_LEVELS,
        label="Water Management Level",
        help_text="Level of government at which water is managed.",
        validators=[validate_select])

class ProjectContactsForm(forms.Form):
    given_name = forms.CharField(max_length=30, label="Given Name")
    middle_name = forms.CharField(max_length=30, required=False, 
        label="Middle Name/Initial")
    surname = forms.CharField(max_length=30)
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
    
class ProjectGeoCondsForm(forms.Form):
    soil_type = forms.ChoiceField(widget=forms.Select, choices=SOIL_TYPES,
        label="Primary Soil Type",
        help_text="Select the soil type most prevalent in your project area.",
        validators=[validate_select])
    description = forms.CharField(widget=forms.Textarea, required=False,
        help_text="Describe the geological and soil conditions of your project area.")
    hit_bedrock = forms.ChoiceField(widget=forms.Select, choices=YES_NO,
        label="Hit Bedrock?",
        help_text="Did you encounter bedrock while implementing your project?")
    hit_water_table = forms.ChoiceField(widget=forms.Select, choices=YES_NO,
        label="Hit Water Table?",
        help_text="Did you encounter the water table while implementing your project?")
    impact = forms.CharField(widget=forms.Textarea, required=False,
        label="Impact of Geological Conditions",
        help_text="Describe how the geological and soil conditions impacted your project.")
        
class ProjectHumanResForm(forms.Form):
    given_name = forms.CharField(max_length=30, label="Given Name")
    middle_name = forms.CharField(max_length=30, required=False, 
        label="Middle Name/Initial")
    surname = forms.CharField(max_length=30)
    profession = forms.ChoiceField(widget=forms.Select, choices=PROFESSIONS,
        validators=[validate_select])
    
    #TODO: Hide the label and help_text also
    profession_other = forms.CharField(max_length=30, required=False, 
        label="Profession (other)",
        help_text="Please input a profession if you selected 'Other'",
        widget=forms.TextInput(attrs={'class':''})) #TODO: class hide
    
    phone = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    add_street1 = forms.CharField(max_length=80, label="Street Address",
                                   required=False)
    add_street2 = forms.CharField(max_length=80, label="Street Address 2",
                                  required=False)
    add_city = forms.CharField(max_length=80, label="City", required=False)
    add_state_prov = forms.CharField(max_length=30, label="State/Province",
                                   required=False)
    add_code = forms.CharField(max_length=20, label="Postal Code", required=False)
    add_country = forms.ChoiceField(widget=forms.Select, label="Country",
                                    choices=countries.COUNTRIES,
                                    required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    
