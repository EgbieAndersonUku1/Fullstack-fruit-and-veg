from django import forms
from authentication.models import BanUser

from utils.dates import calculate_days_between_dates


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
        
        if ban_start_date and ban_expires_on:
            if ban_expires_on <= ban_start_date:
                raise forms.ValidationError("The ban expiry date must be later than the ban issued date.")
        elif ban_start_date and not ban_expires_on:
            raise forms.ValidationError("You have not set the ban expiry date")
        elif ban_expires_on and not ban_start_date:
            raise forms.ValidationError("You have not set the ban start date")
        return cleaned_data
        
    def save(self, commit=True):
     
        user_ban_record = super().save(commit=False)

        ban_reason      = self.cleaned_data["ban_reason"]
        ban_start_date  = self.cleaned_data.get("ban_start_date", None)
        ban_expires_on  = self.cleaned_data.get("ban_expires_on", None)
        
        if ban_start_date and ban_expires_on:

            num_of_days_to_ban = calculate_days_between_dates(ban_expires_on, ban_start_date)
            user_ban_record.ban_for_x_amount_of_days(num_of_days_to_ban, save=False)
      
          
        if commit:
            user_ban_record.save()
            # self.trigger_ban_notification_email(user_ban_record)

        return user_ban_record

    def trigger_ban_notification_email(self, user_ban_record):
        # TODO Send an email or trigger notification when user is banned
        pass
