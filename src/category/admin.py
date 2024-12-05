from django.contrib import admin

from category.models import AllDepartmentsModel

# Register your models here.


class AllDepartmentsModelAdmin(admin.ModelAdmin):
    
    list_display       = ["id", "name", "created_at", "modified_at"]
    list_display_links = ["id", "name"]
    readonly_fields    = ["created_at", "modified_at"]
    
    

admin.site.register(AllDepartmentsModel, AllDepartmentsModelAdmin)