from django.db import models
from django.db.models.functions import Lower
from django.forms import ValidationError

from utils.generator import generate_token
from utils.custom_errors import ShippingDataError

# Create your models here.


class Brand(models.Model):
    """The model represents the brand for a given product"""
    
    name        = models.CharField(max_length=100, db_index=True, unique=True, null=False)
    description = models.TextField(blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = [Lower('name')]   # Ensures case-insensitive alphabetical ordering
        
    def __str__(self) -> str:
        return self.name
    
    
class Category(models.Model):
    """The model represents the category for each product"""
    
    category    = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name        = "Category"
        verbose_name_plural = "Categories"
        ordering = ['category'] 
        
    def __str__(self) -> str:
        return self.category
    


class Manufacturer(models.Model):
    """The model represents the manufacturer of the product"""
    
    name         = models.CharField(max_length=255)
    description  = models.TextField(blank=True, null=True)
    address      = models.CharField(max_length=255)
    contact_num  = models.CharField(blank=True, null=True, max_length=20) 
    is_certified = models.BooleanField(default=True)
    created_on   = models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class ProductVariation(models.Model):
    """The model represents the different product variations such as size, color, dimensions, etc."""
    
    class Availability(models.TextChoices):
        IN_STOCK     = ("is", "In Stock")
        OUT_OF_STOCK = ("oo", "Out of Stock")
        PRE_ORDER    = ("po", "Pre-order")
        
    product             = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='product_variations')
    color               = models.CharField(max_length=90)
    size                = models.CharField(max_length=50, verbose_name="Size (e.g. s, m, l, xl)")
    height              = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Height (in cm)")  
    width               = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Width (in cm)")    
    length              = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Length (in cm)")   
    stock_quantity      = models.PositiveIntegerField(default=0)
    minimum_stock_order = models.PositiveBigIntegerField(default=0)
    maximum_stock_order = models.PositiveBigIntegerField(default=0)
    availability        = models.CharField(choices=Availability.choices, default=Availability.IN_STOCK, max_length=2)
    created_on          = models.DateTimeField(auto_now_add=True)
    modified_on         = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"Name: <{self.product.name.title()}> - Colour: <{self.color.title()}> - Size: <{self.size.title()}>"
    
    def stock_availability(self):
        """Return a readable display of the stock's availability."""
        if self.availability == self.Availability.IN_STOCK:
            return "In Stock"
        elif self.availability == self.Availability.OUT_OF_STOCK:
            return "Out of Stock"
        else: 
            return "Pre-order"
        return "Unknown"  
    
    def clean(self):
        if self.minimum_stock_order > self.maximum_stock_order:
            raise ValidationError("Minimum stock order cannot exceed the maximum stock order.")
        if self.minimum_stock_order <= 0 or self.maximum_stock_order <= 0:
            raise ValidationError("Stock order values must be positive.")
    
    def save(self, *args, **kwargs):
        self.availability = self.stock_quantity > 0
        super().save(*args, **kwargs)

    class Meta:
        ordering  = ['product', 'color', 'size']


class Shipping(models.Model):
    """The model represents the shipping"""
    
    class ShippingType(models.TextChoices):
        STANDARD = "s", "Standard"
        EXPRESS = "e",  "Express"
        PREMIUM = "p",  "Premium"

    product      = models.ForeignKey("Product", on_delete=models.CASCADE, blank=True, null=True)
    height       = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    width        = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    length       = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    weight       = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    price        = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    shipping_type = models.CharField(choices=ShippingType.choices, default=ShippingType.STANDARD)
    created_on   = models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)
        
    def __str__(self) -> str:
        if self.shipping_type == self.ShippingType.STANDARD:
            return "Shipping Type - Standard"
        elif self.shipping_type == self.ShippingType.EXPRESS:
            return "Shipping Type - Express"
        else: 
            return "Shipping Type - Premium"
        
    
    def product_name(self):
        return self.product.name
    
    def clean(self):
        """
        Validates the shipping and pricing fields to ensure all values are non-negative
        before saving to the database.
        """
        negative_fields = {
            "shipping_height": self.height,
            "shipping_width": self.width,
            "shipping_length": self.length,
            "shipping_weight": self.weight,
            "standard_shipping": self.price,
        }
        
        for field, value in negative_fields.items():
            if value is not None and value < 0:
                raise ValidationError(f"The {field.replace("_", " ")} cannot be less that 0")
       
            
    def apply_shipping_options(self, shipping_data, save=True):
        """
        Updates the shipping object based on the provided shipping data.
        """
        if not isinstance(shipping_data, dict):
            raise ShippingDataError(f"Expected 'shipping_data' to be a dictionary, got {type(shipping_data).__name__}.")

        if "delivery_options" not in shipping_data:
            raise ShippingDataError("'delivery_options' key is missing from the shipping_data dictionary.")

        # Extract and validate delivery options
        delivery_options = shipping_data.get("delivery_options", [])
        if not isinstance(delivery_options, list):
            raise ShippingDataError(f"'delivery_options' should be a list, got {type(delivery_options).__name__}.")

        for delivery_option in delivery_options:
            if delivery_option.lower() == Shipping.ShippingType.STANDARD.value > 0:
                self.shipping_type = shipping_data.get("standard_shipping", 0)
            elif delivery_option.lower() == Shipping.ShippingType.EXPRESS.value > 0:
                self.shipping_type = shipping_data.get("express_shipping", 0)
            elif delivery_option.lower() == Shipping.ShippingType.PREMIUM.value > 0:
                self.shipping_type = shipping_data.get("premium_shipping", 0)

        if save:
            self.save()

            
class Product(models.Model):
    """The model represent the fields for each product e.g product name, description, etc"""
    
    name                = models.CharField(max_length=150)
    long_description    = models.TextField(verbose_name="Long description")
    short_description   = models.TextField(max_length=255, verbose_name="Short description")
    is_featured         = models.BooleanField(default=False)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="products")
    brand               = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    sku                 = models.CharField(max_length=255, unique=True) 
    upc                 = models.CharField(max_length=255, unique=True) 
    price               = models.DecimalField(max_digits=10, decimal_places=2)    
    is_discounted_price = models.BooleanField(default=False)
    discount_price      = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight              = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    primary_image       = models.ImageField(upload_to="product_images")
    side_image          = models.ImageField(upload_to="product_images")
    side_image_2        = models.ImageField(upload_to="product_images")
    meta_title          = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords       = models.CharField(max_length=255, blank=True, null=True)
    meta_description    = models.TextField(blank=True, null=True)
    manufacturer        = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    country_of_origin   = models.CharField(max_length=50)
    nutrition           = models.JSONField(null=True, blank=True)
    warranty_period     = models.TextField(blank=True, null=True,  default="No warranty")
    is_returnable       = models.BooleanField(default=False)
    recommendation      = models.CharField(max_length=255, blank=True, null=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    modified_on         = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name 
    
    def brand_name(self):
        return self.brand.title()
    
    def get_warranty_period(self):
        return self.warranty_period or "No warranty"
    
    def clean(self):
        if self.is_discounted_price and not self.discount_price:
            raise ValidationError("Discount price must be set when discount is enabled.")
        if not self.is_discounted_price and self.discount_price:
            raise ValidationError("Discount price should be empty when discount is disabled.")
        if self.is_discounted_price and self.discount_price and (self.price >= self.discount_price):
            raise ValidationError("Discount price cannot be greater or equal to the actual price")

    def get_discounted_price(self):
        """Returns the discounted price else returns the actual price"""  
        return self.discount_price if self.discount else self.price      
    
    def save(self, *args, **kwargs):
        """Allows the save method to be overriden"""
        if not self.sku:
            self.sku = generate_token()
        if not self.upc:
            self.upc = generate_token()
        super().save(*args, **kwargs)