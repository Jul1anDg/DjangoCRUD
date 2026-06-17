from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)  # Hacer que date_created sea de solo lectura
    
admin.site.register(Task, TaskAdmin)
# Register your models here.
