from django.urls import path

from . import views


urlpatterns = [
     path("subscribe/", view=views.subscribe_user, name='subscribe'),
     path("manage/", view=views.manage_subscription, name="manage_subscription"),
     path("update/", view=views.update_newsletter_frequency, name="update_frequency"),
     path("unsubscribe/", view=views.unsubscribe, name="unsubscribe"),
     path("re_subscribe/", view=views.re_subscribe, name="re_subscribe"),
]