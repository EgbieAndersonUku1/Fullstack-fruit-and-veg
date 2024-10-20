from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from django.utils import timezone


from .models import Testimonial, UnapprovedTestimonial, ApprovedTestimonial

# Register your models here.

class BaseTestimonial(admin.ModelAdmin):
    ordering           = ['-date_created']
    list_display       = ["author", "ratings", "country", "is_approved", "date_sent", "date_approved", "has_admin_responded"]
    list_display_links = ["author"]
    list_filter        = ["is_approved", "ratings", "country"]
    readonly_fields    = ["date_approved", "ratings", "company_name", 
                          "testimonial_text", "job_title", "date_sent", 
                          "date_created", "location", "country", "user_image",
                          "author",
                          "has_admin_responded",
                          ]
    list_per_page = 25
    
    fieldsets = [
        (None, {
            "fields": ["author", "job_title", "user_image", "company_name", "testimonial_text"],
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
            "fields": ["featured", "admin_response", "has_admin_responded", "tags"]
        })
    ]
    
    def save_model(self, request, obj, form, change):
        print("Saving testimonial in admin...") 
        super().save_model(request, obj, form, change) 

      
class TestimonialAdmin(BaseTestimonial):
   
    search_fields   = ["ratings", "is_approved", "country"]
    # readonly_fields = ["date_sent", "date_created"]
    
   

class UnapprovedTestimonialAdmin(BaseTestimonial):
    search_fields   = ["ratings", "country"]
    readonly_fields    = ["date_approved", "ratings", "company_name", 
                          "testimonial_text", "job_title", "date_sent", 
                          "date_created", "location", "country", "user_image",
                          "author",
                          "has_admin_responded",
                          "is_approved",
                          ]
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        query_set = super().get_queryset(request)
        return query_set.filter(is_approved=False)
    
    def save_model(self, request, obj, form, change):
        print("Saving testimonial in admin...") 
        super().save_model(request, obj, form, change) 
     
            
class ApprovedTestimonialAdmin(BaseTestimonial):
     search_fields = ["ratings", "country"]
    
     
     def get_queryset(self, request: HttpRequest) -> QuerySet:
         query_set = super().get_queryset(request)
         return query_set.filter(is_approved=True)


admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(UnapprovedTestimonial, UnapprovedTestimonialAdmin)
admin.site.register(ApprovedTestimonial, ApprovedTestimonialAdmin)