import bwapp.models
from django.contrib import admin


class DefaultAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'modified')
    date_hierarchy = 'created'
    list_filter = ['created']
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

admin.site.register(bwapp.models.NewsUpdate, DefaultAdmin)
admin.site.register(bwapp.models.Project, DefaultAdmin)
admin.site.register(bwapp.models.FeaturedProject)
admin.site.register(bwapp.models.Location, LocationAdmin)
admin.site.register(bwapp.models.CodeRegion)
admin.site.register(bwapp.models.CodeElevation)
admin.site.register(bwapp.models.CodeTopography)
admin.site.register(bwapp.models.CodeProjType)