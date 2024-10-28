from django import forms


class SubscriptionFeedBackForm(forms.Form):
    reason_for_unsubscribing = forms.CharField(
        widget=forms.Textarea(attrs={
            "cols": "30",
            "rows": "10",
            "placeholder": "Share your thoughts here...",
        }),
        
        help_text="Please provide at least 50 characters."
    )