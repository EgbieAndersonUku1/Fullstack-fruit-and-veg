from django.db import models
from django.forms import ValidationError
from utils.generator import generate_token


# Create your models here.


class Brand(models.Model):
    """The model represents the brand for a given product"""
    
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name'] 
        
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
    contact_num  = models.CharField(blank=True, null=True, max_length=12) 
    is_certified = models.BooleanField(default=True)
    created_on   = models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class ProductVariation(models.Model):
    """The model represents the different product variations such as size, color, dimensions, etc."""
    
    product             = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='product_variations')
    color               = models.CharField(max_length=90)
    size                = models.CharField(max_length=50, verbose_name="Size (e.g s, m, l, xl)")
    height              = models.DecimalField(max_digits=10, decimal_places=2)
    width               = models.DecimalField(max_digits=10, decimal_places=2)
    length              = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity      = models.PositiveIntegerField(default=0)
    minimum_stock_order = models.PositiveBigIntegerField(default=0)
    maximum_stock_order = models.PositiveBigIntegerField(default=0)
    availability        = models.BooleanField(default=False)
    created_on          = models.DateTimeField(auto_now_add=True)
    modified_on         = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.color} - {self.size}"
    
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
    
    product              = models.ForeignKey("Product", on_delete=models.SET_NULL, blank=True, null=True )
    shipping_height      = models.DecimalField(max_digits=10, decimal_places=2)  
    shipping_width       = models.DecimalField(max_digits=10, decimal_places=2)  
    shipping_length      = models.DecimalField(max_digits=10, decimal_places=2)  
    shipping_weight      = models.DecimalField(max_digits=10, decimal_places=2)  
    standard_shipping    = models.DecimalField(max_digits=10, decimal_places=2)  
    premium_shipping     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)  
    express_shipping     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)  
    created_on           = models.DateTimeField(auto_now_add=True)
    modified_on          = models.DateTimeField(auto_now=True)
            
    def __str__(self) -> str:
        return self.product.name
    
    def clean(self):
        """
        Validates the shipping and pricing fields to ensure all values are non-negative
        before saving to the database.
        """
        negative_fields = {
            "shipping_height": self.shipping_height,
            "shipping_width": self.shipping_width,
            "shipping_length": self.shipping_length,
            "shipping_weight": self.shipping_weight,
            "standard_shipping": self.standard_shipping,
            "premium_shipping": self.premium_shipping,
            "express_shipping": self.express_shipping,
        }
        
        for field, value in negative_fields.items():
            if value is not None and value < 0:
                raise ValidationError(f"The {field.replace("_", " ")} cannot be less that 0")
       
            
           
class Product(models.Model):
    """The model represent the fields for each product e.g product name, description, etc"""
    
    name               = models.CharField(max_length=150)
    long_description   = models.TextField(verbose_name="Long description")
    short_description  = models.TextField(max_length=255, verbose_name="Short description")
    is_featured        = models.BooleanField(default=False)
    category           = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="products")
    brand              = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    sku                = models.CharField(max_length=255, unique=True, default=generate_token) 
    upc                = models.CharField(max_length=255, unique=True, default=generate_token) 
    price              = models.DecimalField(max_digits=10, decimal_places=2)    
    discount           = models.BooleanField(default=False)
    discount_price     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    primary_image      = models.ImageField(upload_to="product_images")
    side_image         = models.ImageField(upload_to="product_images")
    side_image_2       = models.ImageField(upload_to="product_images")
    meta_title         = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords      = models.CharField(max_length=255, blank=True, null=True)
    meta_description   = models.TextField(blank=True, null=True)
    manufacturer       = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    country_of_origin  = models.CharField(max_length=50)
    nutrition          = models.JSONField(null=True, blank=True)
    warranty_period    = models.TextField(blank=True, null=True,  default="No warranty")
    created_on         = models.DateTimeField(auto_now_add=True)
    modified_on        = models.DateTimeField(auto_now=True)
            
    def get_warranty_period(self):
        return self.warranty_period or "No warranty"
    
    def clean(self):
        if self.discount and not self.discount_price:
            raise ValidationError("Discount price must be set when discount is enabled.")
        if not self.discount and self.discount_price:
            raise ValidationError("Discount price should be empty when discount is disabled.")
        if self.discount and self.discount_price and (self.price >= self.discount_price):
            raise ValidationError("Discount price cannot be greater or equal to the actual price")

    def get_discounted_price(self):
        """Returns the discounted price else returns the actual price"""  
        return self.discount_price if self.discount else self.price      

            
