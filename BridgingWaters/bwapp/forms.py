import datetime

from django import forms
# Use FormWizard to split form across multiple pages
# https://docs.djangoproject.com/en/1.3/ref/contrib/formtools/form-wizard/
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from django_countries import countries

now = datetime.datetime.now()
YEARS = [str(i) for i in range(1980,now.year+1)]

class ProjectForm1(forms.Form):
    #general
    title = forms.CharField(max_length=256)
    description = forms.CharField(widget=forms.Textarea)
    start_date = forms.DateField(widget=SelectDateWidget(years=YEARS))
    end_date = forms.DateField(widget=SelectDateWidget(years=YEARS))
    goal = forms.CharField(max_length=768, label='Project Goal')
    proj_mgmt = forms.CharField(widget=forms.Textarea,
                                label='Project Management Description',
                                help_text='Describe how your project was managed.')
    country = forms.ChoiceField(widget=forms.Select,
        choices=countries.COUNTRIES)
    
class ProjectForm2(forms.Form):
    #location
    pass
    

class ProjectForm3(forms.Form):
    #community info
    pass
    
class ProjectWizard(FormWizard):
    def done(self, request, form_list):
        save_project(form_list)
        return HttpResponseRedirect('/bw/submitted/')
        
def save_project(form_list):
    pass