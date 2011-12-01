import bwapp.models
from django.contrib import admin


class DefaultAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'modified')
    date_hierarchy = 'created'
    list_filter = ['created']
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
   

class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'website']}),
        ('Address', {'fields': ['add_street1', 'add_street2', 'add_city',
                                'add_state_prov', 'add_code', 'add_country']}),
        (None, {'fields': ['notes']})
    ]

class OrganizationInline(admin.StackedInline):
    model = bwapp.models.Organization
    fieldsets = [
        (None, {'fields': ['name', 'website']}),
        ('Address', {'fields': ['add_street1', 'add_street2', 'add_city',
                                'add_state_prov', 'add_code', 'add_country']}),
        (None, {'fields': ['notes']})
    ]
    extra = 0
    
    
class ProjectContactInline(admin.StackedInline):
    model = bwapp.models.ProjectContact
    fieldsets = [
        (None, {'fields': ['given_name', 'middle_name', 'surname', 'phone',
                           'email', 'website']}),
        ('Address', {'fields': ['add_street1', 'add_street2', 'add_city',
                                'add_state_prov', 'add_code', 'add_country']}),
        (None, {'fields': ['project']})
    ]
    extra = 0

class HumanResContactInline(admin.StackedInline):
    model = bwapp.models.HumanResContact
    fieldsets = [
        (None, {'fields': ['given_name', 'middle_name', 'surname', 'phone',
                           'email', 'type', 'other_type']}),
        ('Address', {'fields': ['add_street1', 'add_street2', 'add_city',
                                'add_state_prov', 'add_code', 'add_country']}),
        (None, {'fields': ['notes', 'project']})
    ]
    extra = 0

class ProjectAdmin(DefaultAdmin):
    inlines = [ProjectContactInline, HumanResContactInline]

admin.site.register(bwapp.models.NewsUpdate, DefaultAdmin)
admin.site.register(bwapp.models.Project, ProjectAdmin)
admin.site.register(bwapp.models.FeaturedProject)
admin.site.register(bwapp.models.Location, LocationAdmin)
admin.site.register(bwapp.models.CodeRegion)
admin.site.register(bwapp.models.CodeElevation)
admin.site.register(bwapp.models.CodeTopography)
admin.site.register(bwapp.models.CodeProjType)
admin.site.register(bwapp.models.Organization, OrganizationAdmin)



