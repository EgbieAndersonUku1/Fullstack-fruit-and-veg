from django import forms
from .utils.product_category_utils import get_product_category_choices


class BasicFormDescription(forms.Form):
    
    name = forms.CharField(label="Product name", max_length=100, min_length=3,
                            widget=forms.TextInput(attrs={
                                    "id": "product-name",
                                    "placeholder": "Enter a product name..."
                            })
    )

    category = forms.ChoiceField(label="Select a product category", 
                                choices=get_product_category_choices(),
                                widget=forms.Select(attrs={
                                    "id": "select-category",
                                    "name": "select-a-category",
                                    "class": "select-category",
                                    "required": True,
                                }))
    
    new_category = forms.CharField(max_length="100", min_length=6, 
                    widget=forms.TextInput(attrs={
                        "id": "add-category",
                        "placeholder": "Enter a category",
                        "name": "add-category",        
                    }))
    
    brand = forms.CharField(label="Brand", max_length=20, 
                          widget=forms.TextInput(attrs={"id": "brand", "name": "brand", "placeholder": "Enter a brand..."}))
    
    sku = forms.CharField(label="SKU (Stock Keeping Unit)", max_length=20, 
                          widget=forms.TextInput(attrs={"id": "sku", "name": "sku", "placeholder": "Enter a SKU..."}))
    
    upc = forms.CharField(label="UPC (Universal Product Code)", max_length=20, 
                          widget=forms.TextInput(attrs={"id": "upc", "name": "upc", "placeholder": "Enter a UPC..."}))
    
    short_description = forms.CharField(label="Enter a short description", 
                                        widget=forms.Textarea(attrs={"id": "short-description", "rows": "5", 
                                                                     "cols": "10", "required": True,
                                                                     "placeholder": "Enter a short description..."}))
    
    