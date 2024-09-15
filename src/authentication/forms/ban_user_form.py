from django import forms
from authentication.models import BanUser

from utils.dates import calculate_days_between_dates


class BanUserAdminForm(forms.ModelForm):
    class Meta:
        model = BanUser
        fields = ["user", "ban_reason", "ban_start_date", "ban_expires_on"]
    
    def clean(self):
        cleaned_data = super().clean()
        
        ban_start_date = cleaned_data.get("ban_start_date")
        ban_expires_on = cleaned_data.get("ban_expires_on")
        
        if ban_start_date and ban_expires_on:
            if ban_expires_on <= ban_start_date:
                raise forms.ValidationError("The ban expiry date must be later than the ban issued date.")
        
        return cleaned_data
        
    def save(self, commit=True):
     
        ban_user = super().save(commit=False)

        ban_reason      = self.cleaned_data["ban_reason"]
        ban_start_date  = self.cleaned_data["ban_start_date"]
        ban_expires_on  = self.cleaned_data["ban_expires_on"]
        
        num_of_days_to_ban = calculate_days_between_dates(ban_expires_on, ban_start_date)
        ban_user.ban_for_x_amount_of_days(ban_reason, num_of_days_to_ban, save=False)
            

        if commit:
            ban_user.save()
            # self.trigger_ban_notification_email(ban_user)

        return ban_user

    def trigger_ban_notification_email(self, ban_user):
        # TODO Send an email or trigger notification when user is banned
        pass
