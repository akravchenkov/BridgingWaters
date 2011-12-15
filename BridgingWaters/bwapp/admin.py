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

class ClimateInline(admin.StackedInline):
    model = bwapp.models.Climate
    can_delete = False

class CommunityInfoInline(admin.StackedInline):
    model = bwapp.models.CommunityInfo
    can_delete = False

class LocationInline(admin.StackedInline):
    model = bwapp.models.Location
    can_delete = False

class GeoConditionsInline(admin.StackedInline):
    model = bwapp.models.GeoConditions
    can_delete = False

class ProjectAdmin(DefaultAdmin):
    inlines = [LocationInline, ClimateInline, CommunityInfoInline,
               ProjectContactInline, GeoConditionsInline,
               HumanResContactInline, OrganizationInline]

admin.site.register(bwapp.models.NewsUpdate, DefaultAdmin)
admin.site.register(bwapp.models.Project, ProjectAdmin)
admin.site.register(bwapp.models.FeaturedProject)
admin.site.register(bwapp.models.Location, LocationAdmin)
admin.site.register(bwapp.models.CodeRegion)
admin.site.register(bwapp.models.CodeElevation)
admin.site.register(bwapp.models.CodeTopography)
admin.site.register(bwapp.models.CodeProjType)
admin.site.register(bwapp.models.CodeProfession)
admin.site.register(bwapp.models.CodePrecipLevel)
admin.site.register(bwapp.models.CodeClimateZone)
admin.site.register(bwapp.models.CodeUrbanRural)
admin.site.register(bwapp.models.CodeWaterMgmtLevel)
admin.site.register(bwapp.models.CodePplServed)
admin.site.register(bwapp.models.CodeSoilType)
admin.site.register(bwapp.models.Keywords)
admin.site.register(bwapp.models.Climate)
admin.site.register(bwapp.models.CommunityInfo)
admin.site.register(bwapp.models.GeoConditions)
admin.site.register(bwapp.models.Organization, OrganizationAdmin)



