from django import forms
from authentication.models import BanUser

from django.utils.timezone import is_naive, make_aware


def validate_date_ranges(start_date, end_date):
  
    if start_date and end_date:
        if end_date <= start_date:
            raise forms.ValidationError("The ban expiry date must be later than the ban issued date.")
    elif start_date and not end_date:
        raise forms.ValidationError("You have not set the ban expiry date.")
    elif end_date and not start_date:
        raise forms.ValidationError("You have not set the ban start date.")

        
class BanUserAdminForm(forms.ModelForm):
    class Meta:
        model = BanUser
        fields = ["user", "ban_reason", "ban_start_date", "ban_expires_on"]
    
    def clean(self):
        cleaned_data = super().clean()
        
        ban_start_date = cleaned_data.get("ban_start_date", None)
        ban_expires_on = cleaned_data.get("ban_expires_on", None)
        is_banned_msg  = ""
        
        # Check if the user is already banned
        user_ban_record = BanUser.objects.filter(user=cleaned_data["user"]).first()
        
        if user_ban_record:
            is_banned_msg = user_ban_record.is_user_already_banned()
        
        if is_banned_msg:
            raise forms.ValidationError(is_banned_msg)
        
        validate_date_ranges(ban_start_date, ban_expires_on)
        
        return cleaned_data
        
    def save(self, commit=True):
        user_ban_record = super().save(commit=False)

        user           =  self.cleaned_data.get("user")
        ban_start_date = self.cleaned_data.get("ban_start_date", None)
        ban_expires_on = self.cleaned_data.get("ban_expires_on", None)
        
        if ban_start_date and ban_expires_on:
            user_ban_record.ban_for_date_range(ban_start_date, ban_expires_on, save=False)
        elif not ban_start_date and not ban_expires_on:
            user_ban_record.user = user
            user_ban_record.ban()

        if commit:
            user_ban_record.save()
            # Optionally trigger a notification email
            # self.trigger_ban_notification_email(user_ban_record)

        return user_ban_record

    def trigger_ban_notification_email(self, user_ban_record):
        # TODO: Implement logic to send notification emails when a user is banned
        pass
