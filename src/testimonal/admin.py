from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from django.utils import timezone


from .models import Testimonial, UnapprovedTestimonial, ApprovedTestimonial

# Register your models here.

class BaseTestimonial(admin.ModelAdmin):
    ordering           = ['-date_created']
    list_display       = ["author", "title", "ratings", "country", "location", "is_approved", "date_sent", "date_approved"]
    list_display_links = ["author", "title"]
    list_filter        = ["is_approved", "ratings", "country"]
    readonly_fields    = ["date_approved"]
    list_per_page = 25
    
    fieldsets = [
        (None, {
            "fields": ["author", "title", "user_image", "company_name", "testimonial_text"],
        }),
        
        ('Location Info', {
            "classes": ["wide", "collapse"],
            "fields": ["country", "location"],
        }),
        ("Ratings info", {
            "classes": ["wide", "collaspe"],
            "fields": ["ratings"]
        }),
        ("Status info", {
            "classes": ["wide", "collaspe"],
            "fields": ["is_approved"]
        }),
        
        ("Additional info", {
            "classes": ["wide", "collaspe"],
            "fields": ["featured", "admin_response",  "tags"]
        })
    ]
    
    def save_model(self, request, obj, form, change):
        print("Saving testimonial in admin...") 
        super().save_model(request, obj, form, change) 

      
class TestimonialAdmin(BaseTestimonial):
   
    search_fields   = ["ratings", "is_approved", "country"]
    readonly_fields = ["date_sent", "date_created"]
    
   

class UnapprovedTestimonialAdmin(BaseTestimonial):
    search_fields   = ["ratings", "country"]
    readonly_fields = ["date_approved", "is_approved"]
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        query_set = super().get_queryset(request)
        return query_set.filter(is_approved=False)
     
            
class ApprovedTestimonialAdmin(BaseTestimonial):
     search_fields = ["ratings", "country"]
    
     
     def get_queryset(self, request: HttpRequest) -> QuerySet:
         query_set = super().get_queryset(request)
         return query_set.filter(is_approved=True)


admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(UnapprovedTestimonial, UnapprovedTestimonialAdmin)
admin.site.register(ApprovedTestimonial, ApprovedTestimonialAdmin)