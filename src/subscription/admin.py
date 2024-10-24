from django.contrib import admin

from .models import NewsletterSubscription, UnsubscribedNewsletterSubscription, SubscribedNewsletterSubscription

# Register your models here.

class BaseNewsletterAdmin(admin.ModelAdmin):
    list_display       = ["id", "user", "email", "subscribed_on", "unsubscribed", "frequency", "date_unsubscribed"]
    list_display_links = ["id", "user"]
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



admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(UnsubscribedNewsletterSubscription, UnsubscribedNewsletterSubscriptionAdmin)
admin.site.register(SubscribedNewsletterSubscription, SubscribedNewsletterSubscriptionAdmin)