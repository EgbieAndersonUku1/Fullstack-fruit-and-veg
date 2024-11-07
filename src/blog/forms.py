from django import forms 
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import NewPost, Category



class NewBlogPost(forms.ModelForm):
    new_category_name = forms.CharField(max_length=60, required=False, label="New Category")
    new_category      = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                               required=False,
                                               label="Select Category",
                                               help_text="Or select an existing category"
                                          )
    class Meta:
        model  = NewPost
        fields = ['title', 'new_category', 'blog', 'cover_pic', 'author', 'post', 'status']
      
    def clean_post(self):
        post   = self.cleaned_data.get('post')
        status = self.cleaned_data.get('status')
        
        if status == NewPost.PUBLISHED and not post:
            raise forms.ValidationError("Published posts must have content.")
        
        return post