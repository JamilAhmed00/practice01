from django.contrib import admin
from django.contrib.auth.models import User
from .models import Task
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'start_date', 'end_date', 'is_done')
    list_filter = ('user', 'is_done')
    search_fields = ('name',)

admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)


# Register your models here.
