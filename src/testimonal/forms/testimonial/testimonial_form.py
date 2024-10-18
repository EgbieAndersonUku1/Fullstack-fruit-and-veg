from django import forms 
from testimonal.models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        exclude = ["author", "ratings", "is_approved", 
                   "date_approved", "featured", "date_sent",
                   "admin_resports", "tags", "date_created"
                   ]
    
    def save(self, commit=True, reset_fields=False):
        """
        Save the Testimonial instance.

        This method overrides the default save behaviour to include
        additional logic for resetting fields when editing a testimonial.

        Parameters:
        - commit (bool): If True, the instance will be saved to the database.
        - reset_fields (bool): If True, resets the following fields to their default values:
            - is_approved (bool): Set to False.
            - has_admin_responded (bool): Set to False.
            - date_approved (datetime): Set to None.
            - admin_response (str): Set to None.

        Returns:
        - testimonial (Testimonial): The saved instance.
        """
        # Call the original save method to create or update the instance
        testimonial = super().save(commit=commit)

        if reset_fields:
          
            testimonial.is_approved          = False
            testimonial.has_admin_responded  = False
            testimonial.date_approved        = None
            testimonial.admin_response       = None

            if commit:
                testimonial.save()

        return testimonial