from django import forms
from ..utils.country_parser import parse_country_file

from  .base_form_helper  import BaseFormMeasurements
from ..utils.product_category_utils import (get_product_category_choices,
                                            get_product_color_choices, 
                                            get_product_size_chocies,
                                            get_shipping_options
                                            )


class BasicFormDescription(forms.Form):
    CATEGORY_CHOICES = [
        ("n", "No"),
        ("y", "Yes")
    ]
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
                                }))
    
    
    is_featured_item = forms.ChoiceField(label="Featured item", choices=CATEGORY_CHOICES, initial=CATEGORY_CHOICES[0])
    new_category = forms.CharField(max_length="100", 
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
                                                                     "cols": "10", 
                                                                     "placeholder": "Enter a short description..."}))
    



class DetailedFormDescription(BaseFormMeasurements):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.color_choices = get_product_color_choices()
        self.size_choices  = get_product_size_chocies()
        
      
    description = forms.CharField(label="Enter a description description", 
                                widget=forms.Textarea(attrs={"id": "short-description", "rows": "10", 
                                                             "cols": "10", 
                                                            "placeholder": "Enter a description..."}))
    
    
    
    

class PricingAndInventoryForm(forms.Form):
    CATEGORY_CHOICES = [
        ("is", "In Stock"),
        ("oos", "Out of Stock"),
        ("po", "Pre-Order")
    ]
    
    DISCOUNT_OPTIONS = [
        ("", "Select a category"),
        ("yes", "Yes"),
        ("no", "No")
    ]
    price = forms.DecimalField(max_digits=10, decimal_places=2, 
                               widget=forms.NumberInput(attrs={"min": "1", 
                                                               "max": "1000000",
                                                                "step": "0.01",
                                                                "name": "price",
                                                               }))
    
    
    category = forms.ChoiceField(label="Availability", choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
                                     "name": "availability",
                                     "id": "availability",
                                     "class": "select-category",
                                    }))
    
    select_discount = forms.ChoiceField(label="Add a discount?", choices=DISCOUNT_OPTIONS,
                                     widget=forms.Select(attrs={
                                         "name": "select-discount",
                                         "id": "select-discount",
                                         "class": "select-category",
                                     })
                                     )
    
    add_discount = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                               widget=forms.NumberInput(attrs={"min": "1", 
                                                               "max": "1000000",
                                                                "step": "0.01",
                                                                "name": "add-discount",
                                                                "id": "add-discount",
                                                               
                                                                
                                                               }))
    
    quantity_stock = forms.FloatField(label="Quantity in stock", 
                               widget=forms.NumberInput(attrs={"min": "1", 
                                                               "max": "1000000",
                                                                "step": "1",
                                                                "name": "quantity-stock",
                                                                "id": "quantity-stock",
                                                                "required": True,
                                                                
                                                               }))
    
    minimum_order = forms.FloatField(label="Minimum order quantity", 
                               widget=forms.NumberInput(attrs={"min": "1", 
                                                               "max": "1000000",
                                                                "step": "1",
                                                                "name": "minimum-order-quantity",
                                                                "id": "minimum-order-quantity",
                                                                "required": True,
                                                                
                                                               }))
    maximum_order = forms.FloatField(label="Maximum order quantity", 
                               widget=forms.NumberInput(attrs={"min": "1", 
                                                               "max": "1000000",
                                                                "step": "1",
                                                                "name": "maximum-order-quantity",
                                                                "id": "maximum-order-quantity",
                                                                "required": True,
                                                                
                                                               }))
    


class ImageAndMediaForm(forms.Form):
    
    primary_image = forms.ImageField(
        label="Upload primary image (required)",
        widget=forms.ClearableFileInput(attrs={
            "id": "primary-image",
            "accept": "image/*",
            "name": "primary-image",
            "aria-describedby": "primary-image-description"
        })
    )

    side_image1 = forms.ImageField(
        label="Upload side image 1 (required)",
        widget=forms.ClearableFileInput(attrs={
            "id": "side-image1",
            "accept": "image/*",
            "name": "side-image1",
            "aria-describedby": "side-image1-description",
        })
    )

    side_image2 = forms.ImageField(
        label="Upload side image 2 (required)",
        widget=forms.ClearableFileInput(attrs={
            "id": "side-image2",
            "accept": "image/*",
            "name": "side-image2",
            "aria-describedby": "side-image2-description"
        })
    )

    primary_video = forms.FileField(
        label="Upload primary video (optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "id": "primary-video",
            "accept": "video/*",
            "name": "primary-video",
            "aria-describedby": "primary-video-description"
        })
    )


# Shipping and delivery form
class ShippingAndDeliveryForm(BaseFormMeasurements):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.delivery_options = get_shipping_options()
        

# Seo and meta form
class SeoAndMetaForm(forms.Form):
    meta_title = forms.CharField(label="Meta title", min_length=3, max_length=40, 
                                 widget=forms.TextInput(attrs={
                                    "id": "meta-title-input",
                                    "aria-labelledby": "meta-title-label",
                                    "name": "meta-title",
                                    "placeholder": "Enter a meta title...",
                                 }))
    
    meta_keywords = forms.CharField(label="Add meta keywords (separate by commas)", min_length=3, max_length=40, 
                                 widget=forms.TextInput(attrs={
                                    "id": "meta-keyword-input",
                                    "aria-labelledby": "meta-keyword-label",
                                    "name": "meta-keywords",
                                    "aria-labelledby": "meta-keywords-label",
                                    "placeholder": "e.g delicious, creamy, banana...."
                                 }))
    
    meta_description = forms.CharField(label="Meta description", widget=forms.Textarea(attrs={
                                        "id": "meta-description-textarea",
                                        "rows": "10",
                                        "cols": "10",
                                        "aria-labelledby": "meta-description-label",
                                        }))
    



# Additonal information
class AdditionalInformationForm(forms.Form):
    RETURN_POLICY_OPTIONS = [ ("n", "No"), ("y", "Yes")]
    COUNTRIES_CHOICES     = parse_country_file("data/countries.txt")
    
    title = forms.CharField(label="Manufacturer title", min_length=4, max_length=40, 
                            widget=forms.TextInput(attrs={
                                "id": "manafacturer-title",
                                "aria-labelledby": "manufacturer-title",
                                "name": "manafacturer-title",
                                "placeholder": "Enter a manufacturer title...",
                            }))
    
    countries = forms.ChoiceField(label="Country of origin", 
                                  choices=COUNTRIES_CHOICES,
                                  widget=forms.Select(attrs={
                                      "aria-label": "Select Country of Origin",
                                      "id": "countries",
                                      
                                  }))
    
    return_policy = forms.ChoiceField(label="Return policy", 
                                      choices=RETURN_POLICY_OPTIONS,
                                      initial=RETURN_POLICY_OPTIONS[0],
                                      widget=forms.Select(attrs={
                                            "aria-label": "Select Return Policy",
                                            "id": "return-policy",
                                            "name":"return-policy",
                                            
                                        }))
    
    description = forms.CharField(label="Warranty description", widget=forms.Textarea(attrs={
                                        "id": "warranty-description",
                                        "rows": "15",
                                        "cols": "10",
                                        "aria-labelledby": "warranty-description-label",
                                        }))