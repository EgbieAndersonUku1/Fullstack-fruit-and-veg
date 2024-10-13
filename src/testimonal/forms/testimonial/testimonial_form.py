from django import forms 
from testimonal.models import Testimonial


class TestimonalForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        exclude = ["author", "ratings", "is_approved", 
                   "date_approved", "featured", "date_sent",
                   "admin_resports", "tags", "date_created"
                   ]