from django.contrib import admin
from django import forms
from django_ckeditor_5.fields import CKEditor5Field
# Register your models here.

from .models import Blog, Category, NewPost


            
class NewPostAdmin(admin.ModelAdmin):
   
    list_display         = ["id", "title", "author", "is_live"]
    list_display_links   = ["id", "title", "author"]
    fieldsets            = [
        (None, {"fields": ["title", "blog", "author", "cover_pic", "new_category"]}),
        ("Create Post content", {
            "classes": ["collapse", "wide"],  
            "fields": ["post"]
        }),
       
        ("Draft and Publishing", {"fields": ["status"]}),
        ("Post status", {"fields": ["is_live"]}),
        ("Additonal", {"fields": ["created_at", "modified_at"]})
            
    ]
    
    readonly_fields = ["created_at", "modified_at"]



class CategoryAdmin(admin.ModelAdmin):
    list_display       = ["id", "name", "created_at", "modified_at"]
    list_display_links = ["id", "name"]
    
    readonly_fields    = ["created_at", "modified_at"]


admin.site.register(NewPost, NewPostAdmin)
admin.site.register(Category, CategoryAdmin)