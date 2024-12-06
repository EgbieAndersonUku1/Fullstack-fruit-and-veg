from django.db import models
from django.forms import ValidationError
from utils.generator import generate_token



# Create your models here.

class Brand(models.Model):
    """The model represents the brand for a given product"""
    name        = models.CharField(max_length=100)
    description = models.TextField()
    created_on  = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name'] 
        
    def __str__(self) -> str:
        return self.name
    

class ProductVariations(models.Model):
    """The model represents the different product variations such as size, color, dimensions, etc."""
    product             = models.ForeignKey("ProductModel", on_delete=models.CASCADE, related_name='variations')
    color               = models.CharField(max_length=90)
    size                = models.CharField(max_length=50)
    height              = models.DecimalField(max_digits=10, decimal_places=2)
    width               = models.DecimalField(max_digits=10, decimal_places=2)
    length              = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity      = models.PositiveIntegerField(default=0)
    minimum_stock_order = models.PositiveBigIntegerField()
    maximum_stock_order = models.PositiveBigIntegerField()
    availability        = models.BooleanField(default=False)
    created_on          = models.DateTimeField(auto_now_add=True)
    modified_on         = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.product.product_name} - {self.color} - {self.size}"
    
    def clean(self):
        if self.minimum_stock_order > self.maximum_stock_order:
            raise ValidationError("Minimum stock order cannot exceed the maximum stock order.")
        if self.minimum_stock_order <= 0 or self.maximum_stock_order <= 0:
            raise ValidationError("Stock order values must be positive.")
    
    def save(self, *args, **kwargs):
        self.availability = self.stock_quantity > 0
        super().save(*args, **kwargs)

    class Meta:
        verbose_name        = "Product Variation"
        verbose_name_plural = "Product Variations"
        ordering            = ['product', 'color', 'size']



class Category(models.Model):
    """The model represents the category for each product"""
    category    = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['category'] 
        
    def __str__(self) -> str:
        return self.category
    
    
class ProductModel(models.Model):
    """The model represent the fields for each product e.g product name, description, etc"""
    name            = models.CharField(max_length=150)
    description     = models.TextField()
    is_featured     = models.BooleanField(default=False)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="products")
    brand           = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    sku             = models.CharField(max_length=255, unique=True, default=generate_token) 
    upc             = models.CharField(max_length=255, unique=True, default=generate_token) 
    price           = models.DecimalField(max_digits=10, decimal_places=2)    
    discount        = models.BooleanField(default=False)
    discount_price  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    primary_image   = models.ImageField(upload_to="product_images")
    side_image      = models.ImageField(upload_to="product_images")
    side_image_2    = models.ImageField(upload_to="product_images")
    
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

            
