from django import forms
from .utils.product_category_utils import get_product_category_choices, get_product_color_choices, get_product_size_chocies


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
                                                                     "cols": "10", "required": True,
                                                                     "placeholder": "Enter a short description..."}))
    



class DetailedFormDescription(forms.Form):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.color_choices = get_product_color_choices()
        self.size_choices  = get_product_size_chocies()
        
       
  
    length = forms.DecimalField(label="Length (in centimeters)", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "length",
                                    "min": "0.1",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter length in cm"
                                    
                                }))
    
    width = forms.DecimalField(label="Width (in centimeters)", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "width",
                                    "min": "0.1",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter length in cm"
                                    
                                }))
    
    height = forms.DecimalField(label="Height (in centimeters)", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "height",
                                    "min": "0.1",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter length in cm"
                                    
                                }))
    
    weight = forms.DecimalField(label="Weight (in grams)", max_digits=10, decimal_places=2, 
                                widget=forms.NumberInput(attrs={
                                    "id": "weight",
                                    "min": "0.01",
                                    "step": "0.01",
                                    "aria-required": "true",
                                    "placeholder": "Enter weight in gram"
                                    
                                }))
    
    description = forms.CharField(label="Enter a description description", 
                                widget=forms.Textarea(attrs={"id": "short-description", "rows": "10", 
                                                             "cols": "10", "required": True,
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
                                         "required": True,
                                         "name": "select-discount",
                                         "id": "select-discount",
                                         "class": "select-category",
                                     })
                                     )
    
    add_discount = forms.DecimalField(max_digits=10, decimal_places=2, 
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
    
    