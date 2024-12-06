from django.db import models

# Create your models here.

class Brand(models.Model):
    name        = models.CharField(max_length=100)
    created_on  = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    

class ProductVariations(models.Model):
    product        = models.ForeignKey("ProductModel", on_delete=models.CASCADE, related_name='variations')
    color          = models.CharField(max_length=90)
    size           = models.CharField(max_length=50)
    height         = models.DecimalField(max_digits=10, decimal_places=2)
    width          = models.DecimalField(max_digits=10, decimal_places=2)
    length         = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_on     = models.DateTimeField(auto_now_add=True)
    modified_on    = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
          return f"{self.product.product_name} - {self.color} - {self.size}"
      


class Category(models.Model):
    category    = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.category
    
    
    
class ProductModel(models.Model):
    product_name = models.CharField(max_length=10)
    description  = models.TextField()
    is_featured  = models.BooleanField(default=False)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand        = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    sku          = models.CharField(max_length=255, unique=True) # Note to self, maybe have the sku code generated automatically - TBD later
    upc          = models.CharField(max_length=255, unique=True) # Note to self, maybe have the upc code generated automatically - TBD later
    


