from bwapp.models import NewsUpdate, Project, FeaturedProject, Location, CodeRegion
from django.contrib import admin


class DefaultAdmin(admin.ModelAdmin):
    # ...
    list_display = ('title', 'created', 'modified')
    date_hierarchy = 'created'
    list_filter = ['created']
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

admin.site.register(NewsUpdate, DefaultAdmin)
admin.site.register(Project, DefaultAdmin)
admin.site.register(FeaturedProject)
admin.site.register(Location, LocationAdmin)
admin.site.register(CodeRegion)
