from typing import Any
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils import timezone


from .models import (NewsletterSubscription,
                     UnsubscribedNewsletterSubscription, 
                     SubscribedNewsletterSubscription,
                     NewsletterSubscriptionHistory
                     )

# Register your models here.

class BaseNewsletterAdmin(admin.ModelAdmin):
    list_display       = ["title", "user", "email", "subscribed_on", "unsubscribed", "frequency", "date_unsubscribed"]
    list_display_links = ["title", "user"]
    list_per_page      = 40
    readonly_fields    = ["subscribed_on", "modified_on"]
    fieldsets = [
        (None, {"fields": ["user", "email", "frequency", "subscribed_on", "modified_on"]}),
         ("Unsubscribe", {"fields": ["unsubscribed", "reason_for_unsubscribing", "unsubscribed_on"]}),
        
    ]

    def date_unsubscribed(self, obj):
        return obj.date_unsubscribed
    
    date_unsubscribed.short_description = "Date unsubscribed"
      
      
class NewsletterSubscriptionAdmin(BaseNewsletterAdmin):
    list_filter        = ["frequency", "unsubscribed"]
    

class UnsubscribedNewsletterSubscriptionAdmin(BaseNewsletterAdmin):
    def get_queryset(self, request):
        """
        Override the default queryset to show only unsubscribed users.
        """
        qs = super().get_queryset(request)
        return qs.filter(unsubscribed=True)


class SubscribedNewsletterSubscriptionAdmin(BaseNewsletterAdmin):
    list_filter = ["frequency"]
    
    def get_queryset(self, request):
        """
        Override the default queryset to show only subscribed users.
        """
        qs = super().get_queryset(request)
        return qs.filter(unsubscribed=False)


class NewsletterSubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display        = ["id", "title", "email", "action", "timestamp", "frequency"]
    list_display_links  = ["id", "title", "email"]
    list_per_page       = 40
    readonly_fields     = ["timestamp", "reason_for_unsubscribing", "email", "frequency", "action", "user"]
    list_filter         = ["user", "frequency", "user__username"]


admin.site.register(NewsletterSubscriptionHistory, NewsletterSubscriptionHistoryAdmin)
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(UnsubscribedNewsletterSubscription, UnsubscribedNewsletterSubscriptionAdmin)
admin.site.register(SubscribedNewsletterSubscription, SubscribedNewsletterSubscriptionAdmin)