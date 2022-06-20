from django.contrib import admin
from .models import ToDo


class TodoAdmin(admin.ModelAdmin):
    """Add readonly field with creation date"""
    readonly_fields = ('created',)


admin.site.register(ToDo, TodoAdmin)
