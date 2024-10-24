from django.contrib import admin

from .models import NewsletterSubscription, UnsubscribedNewsletterSubscription, SubscribedNewsletterSubscription

# Register your models here.

class BaseNewsletterAdmin(admin.ModelAdmin):
    list_display       = ["id", "user", "email", "subscribed_on", "unsubscribed", "frequency", "modified_on"]
    list_display_links = ["id", "user"]
    list_per_page      = 40
      
      
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