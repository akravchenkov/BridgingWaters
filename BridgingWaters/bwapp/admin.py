from bwapp.models import NewsUpdate
from django.contrib import admin


class NewsUpdateAdmin(admin.ModelAdmin):
    # ...
    list_display = ('title', 'created', 'modified')
    date_hierarchy = 'created'
    list_filter = ['created']

admin.site.register(NewsUpdate, NewsUpdateAdmin)