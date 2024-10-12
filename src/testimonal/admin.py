from django.contrib import admin

from .models import Testimonal

# Register your models here.

class TestimonalAdmin(admin.ModelAdmin):
    list_display  = ["author", "title", "ratings", "country", "location", "is_approved", "date_sent"]
    list_per_page = 25
    search_fields = ["ratings", "is_approved", "country"]




admin.site.register(Testimonal, TestimonalAdmin)