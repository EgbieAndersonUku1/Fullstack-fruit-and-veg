from django import forms

class BaseFormMeasurements(forms.Form):
    length = forms.DecimalField(label="Length", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "length",
                                    "min": "0.1",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter length in cm",
                                    "aria-describedby":"length-desc",
                                    
                                }))
    
    width = forms.DecimalField(label="Width", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "width",
                                    "min": "0.1",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter length in cm",
                                     "aria-describedby":"width-desc",
                                    
                                }))
    
    height = forms.DecimalField(label="Height", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "height",
                                    "min": "0.1",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter length in cm",
                                    "aria-describedby":"height-desc",
                                }))
    
    weight = forms.DecimalField(label="Weight", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "weight",
                                    "min": "0.01",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter weight in gram",
                                    "aria-describedby":"weight-desc",
                                    
                                }))