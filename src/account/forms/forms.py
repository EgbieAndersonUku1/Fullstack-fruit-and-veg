from django import forms
from utils.country_parser import parse_country_file

from  .base_form_helper  import BaseFormMeasurements
from ..utils.product_category_utils import (get_product_category_choices,
                                            get_product_color_choices, 
                                            get_product_size_choices,
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

    is_featured_item = forms.ChoiceField(label="Featured item", choices=CATEGORY_CHOICES, initial=CATEGORY_CHOICES[0])

    category = forms.ChoiceField(label="Select a product category", 
                                 choices=get_product_category_choices(),
                                 widget=forms.Select(attrs={
                                     "id": "select-category",
                                     "class": "select-category",
                                 }))

    new_category = forms.CharField(max_length=100, required=False, 
                                   widget=forms.TextInput(attrs={
                                       "id": "add-category",
                                       "placeholder": "Enter a category"
                                   }))

    brand = forms.CharField(label="Brand", max_length=20,
                            widget=forms.TextInput(attrs={"id": "brand", "placeholder": "Enter a brand..."}))

    sku = forms.CharField(label="SKU (Stock Keeping Unit)", max_length=20, required=False,
                          widget=forms.TextInput(attrs={"id": "sku", "placeholder": "Enter a SKU or leave blank to have the system autogenerate it.."}))

    upc = forms.CharField(label="UPC (Universal Product Code)", max_length=20, required=False,
                          widget=forms.TextInput(attrs={"id": "upc", "placeholder": "Enter a UPC or leave blank to have the system autogenerate it..."}))

    short_description = forms.CharField(label="Enter a short description",
                                        widget=forms.Textarea(attrs={"id": "short-description", "rows": "5",
                                                                     "cols": "10",
                                                                     "placeholder": "Enter a short description..."
                                                                     }))


class DetailedFormDescription(BaseFormMeasurements):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_choices = get_product_color_choices()
        self.size_choices = get_product_size_choices()

    description = forms.CharField(label="Enter a detailed description",
                                  widget=forms.Textarea(attrs={"id": "detailed-description", "rows": "10",
                                                               "cols": "10",
                                                               "placeholder": "Enter a description..."}))


class PricingAndInventoryForm(forms.Form):
    STOCK_CHOICES = [
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
                                                               "step": "0.01"
                                                               }))

    available = forms.ChoiceField(label="Availability", choices=STOCK_CHOICES, widget=forms.Select(attrs={
        "id": "availability",
        "class": "select-category",
    }))

    select_discount = forms.ChoiceField(label="Add a discount?", choices=DISCOUNT_OPTIONS,
                                        widget=forms.Select(attrs={
                                            "id": "select-discount",
                                            "class": "select-category",
                                        }))

    add_discount = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                                      widget=forms.NumberInput(attrs={"min": "1",
                                                                      "max": "1000000",
                                                                      "step": "0.01",
                                                                      "id": "add-discount",
                                                                       "type": "number",
                                                                      }))

    quantity_stock = forms.FloatField(label="Quantity in stock",
                                      widget=forms.NumberInput(attrs={"min": "0",
                                                                      "max": "1000000",
                                                                      "step": "1",
                                                                      "id": "quantity-stock",
                                                                      "type": "number",
                                                                      }))

    minimum_order = forms.FloatField(label="Minimum order quantity",
                                     widget=forms.NumberInput(attrs={"min": "0",
                                                                     "max": "1000000",
                                                                     "step": "1",
                                                                     "id": "minimum-order-quantity",
                                                                      "type": "number",
                                                                    
                                                                     }))
    maximum_order = forms.FloatField(label="Maximum order quantity",
                                     widget=forms.NumberInput(attrs={"min": "0",
                                                                     "max": "1000000",
                                                                     "step": "1",
                                                                     "id": "maximum-order-quantity",
                                                                    
                                                                     }))


class ImageAndMediaForm(forms.Form):
    primary_image = forms.ImageField(
        label="Upload primary image (required)",
        widget=forms.ClearableFileInput(attrs={
            "id": "primary-image",
            "accept": "image/*",
            "aria-describedby": "primary-image-description"
        })
    )

    side_image1 = forms.ImageField(
        label="Upload side image 1 (required)",
        widget=forms.ClearableFileInput(attrs={
            "id": "side-image1",
            "accept": "image/*",
            "aria-describedby": "side-image1-description",
        })
    )

    side_image2 = forms.ImageField(
        label="Upload side image 2 (required)",
        widget=forms.ClearableFileInput(attrs={
            "id": "side-image2",
            "accept": "image/*",
            "aria-describedby": "side-image2-description"
        })
    )

    

class ShippingAndDeliveryForm(forms.Form):
    DELIVERY_OPTIONS = [
        ("s", "Standard Delivery"),
        ("p", "Premium Shipping"),
        ("e", "Express Shipping") 
    ]
    height = forms.CharField(widget=forms.TextInput(attrs={
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter the shipping height...",
                                     "type": "number",
                                     "step": "0.01",
                                     "min": "1",
                                     "max": "10000",
                                 }))
    width = forms.CharField(widget=forms.TextInput(attrs={
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter the shipping width..",
                                     "type": "number",
                                     "step": "0.01",
                                     "min": "1",
                                     "max": "10000",
                                 }))
    
    length = forms.CharField(widget=forms.TextInput(attrs={
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter the shipping length..",
                                     "type": "number",
                                     "step": "0.01",
                                     "min": "1",
                                     "max": "10000",
                                 }))

    weight = forms.CharField(widget=forms.TextInput(attrs={
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter the shipping weight..",
                                     "type": "number",
                                     "step": "0.01",
                                     "min": "0.00",
                                     "max": "10000",
                                 }))
    
    standard_shipping = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                     "id": "standard_shipping",
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter the price for a standard delivery..",
                                     "type": "number",
                                     "step": "0.01",
                                     "min": "0.00",
                                     "max": "10000",
                                    
                                 }))
    
    
    premium_shipping = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                     "id": "premium_shipping",
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter the price for a premimum delivery..",
                                     "type": "number",
                                     "step": "0.01",
                                     "min": "0.00",
                                     "max": "10000",
                                 }))
    
    express_shipping = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                     "id": "express_shipping",
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter the price for express shipping..",
                                     "type": "number",
                                     "step": "0.01",
                                     "min": "0.00",
                                     "max": "10000",
                                 }))
    delivery_options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                choices=DELIVERY_OPTIONS,
                                              )


class SeoAndMetaForm(forms.Form):
    meta_title = forms.CharField(label="Meta title (optional)", min_length=3, max_length=40,
                                 required=False,
                                 widget=forms.TextInput(attrs={
                                     "id": "meta-title-input",
                                     "aria-labelledby": "meta-title-label",
                                     "placeholder": "Enter a meta title...",
                                 }))

    meta_keywords = forms.CharField(label="Add meta keywords (separate by commas) - optional", min_length=3, 
                                    max_length=40, 
                                    required=False,
                                    widget=forms.TextInput(attrs={
                                        "id": "meta-keyword-input",
                                        "aria-labelledby": "meta-keyword-label",
                                        "placeholder": "e.g delicious, creamy, banana..."
                                    }))

    meta_description = forms.CharField(label="Meta description (optional)", 
                                       required=False,
                                       widget=forms.Textarea(attrs={
                                       "id": "meta-description-textarea",
                                       "rows": "10",
                                       "cols": "10",
                                       "aria-labelledby": "meta-description-label",
                                    }))



class NutritionForm(forms.Form):
    
    calories      = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    carbohydrates = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    sugar         = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    protein       = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0)
    fibre         = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    fat           = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    
    
    
class AdditionalInformationForm(forms.Form):
    RETURN_POLICY_OPTIONS = [("n", "No"), ("y", "Yes")]
    COUNTRIES_CHOICES = parse_country_file("data/countries.txt")

    title = forms.CharField(label="Manufacturer title", min_length=4, 
                            max_length=40, 
                            widget=forms.TextInput(attrs={
                                "id": "manufacturer-title",
                                "aria-labelledby": "manufacturer-title",
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
                                      }))

    recommendation = forms.CharField(label="Recommendation (optional)", 
                                    required=False,
                                    widget=forms.Textarea(attrs={
                                    "id": "recommendation-description",
                                    "rows": "5",
                                    "cols": "10",
                                    "aria-labelledby": "Recommendation-label",
                                    "placeholder": "Optional: Leave blank if no recommendation (e.g., 'Pair with a fresh salad')"

                                     }))
    
    description = forms.CharField(label="Warranty description (optional)", 
                                    required=False,
                                    widget=forms.Textarea(attrs={
                                    "id": "warranty-description",
                                    "rows": "15",
                                    "cols": "10",
                                    "aria-labelledby": "warranty-description-label",
                                    "placeholder": "Leave blank for no warranty..."
                                     }))

