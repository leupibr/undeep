from django.contrib import admin

from api.models import Document, Category


class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'path']}),
        ('Document', {'fields': ['date', 'hsize', 'uploaded', 'modified'], 'classes': ['collapse']}),
        ('Assignment', {'fields': ['category', 'method'], 'classes': ['collapse']})
    ]
    readonly_fields = ['path', 'hsize', 'uploaded', 'modified']
    list_display = ('path', 'category', 'hsize', 'uploaded', 'modified')
    list_filter = ['uploaded', 'modified', 'category', 'method']
    search_fields = ['name', 'path']


admin.site.register(Document, DocumentAdmin)
admin.site.register(Category)
