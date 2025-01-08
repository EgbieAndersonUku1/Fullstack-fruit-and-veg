from django.contrib import admin

from .models import Product, ProductVariation, Category, Brand, Manufacturer, Shipping


# Register your models here.

class ProductVariationStackInline(admin.StackedInline):
    """
    Displays product variations within the Product model in the admin interface.
    """
    model  = ProductVariation
    extra  = 1


class ShippingStackInline(admin.StackedInline):
    """
    Displays shipping within the Product model in the admin interface.
    """
    model = Shipping
    extra = 1


class ShippingAdmin(admin.ModelAdmin):
    """
    Admin interface for the Shipping model.

    This standalone model allows for direthct management of shipping attributes
    (e.g., shipping height, shippng width) without navigating through the parent Product model.
    """
    list_display = ["shipping_type", "product", "height", "width", "length", "created_on", "modified_on"]
    fieldsets    = [
        ("General Information", { "fields": ["product", "price", "shipping_type" ]}),
        ("Dimensions", { "fields": ["height", "width", "length"]}),
        ("Weight", { "fields": ["weight"]}),
      
    ]
    
    readonly_fields = ["created_on", "modified_on"]
    list_per_page   = 25
    list_filter     = ["price"]
    search_fields   = ["price"]
    

class CategoryAdmin(admin.ModelAdmin):
    """
    Displays category model in the admin interface.
    """
    list_display       = ["id", "category", "created_on", "modified_on"]
    list_per_page      = 25
    readonly_fields    = ["created_on", "modified_on"]
    search_fields      = ["category"]
    list_display_links = ["id", "category"]
    
    
class ProductModelAdmin(admin.ModelAdmin):
    """
    Displays the product model admin interface.
    """
    list_display      = ["id", "name", "brand_name", "price",  "is_discounted_price", "is_featured", "created_on", "modified_on"]
    list_filter       = ["is_featured", "name", "brand", "is_featured"]
    search_fields     = ["name", "sku", "upc", "brand", 
                         "meta_title", "meta_keywords", 
                         "country_of_origin", "manufacturer", "id"]
    list_display_links = ["id", "name"]
    list_per_page = 25
    
    
    fieldsets = [
        ("General Information", { "fields": ["name", "short_description", "category", "brand", "sku", "upc", "long_description" ]}),
        ("Pricing and Discounts", { "fields": ["price", "is_discounted_price", "discount_price"]}),
        ("Media", { "fields": ["primary_image", "side_image", "side_image_2"]}),
        ("SEO Metadata", { "fields": ["meta_title", "meta_keywords", "meta_description"]}),
        ("Additonal information", { "fields": ["manufacturer", "country_of_origin", "warranty_period"]}),
        ("Highlight", { "fields": ["is_featured"]}),
        
    ]
    
    readonly_fields = ["created_on", "modified_on"]
    list_per_page   = 25
    inlines         = [ProductVariationStackInline, ShippingStackInline]
    
    def brand_name(self, obj):
        return obj.brand
    
    
class ProductVariationAdmin(admin.ModelAdmin):
    """
    Admin interface for the ProductVariation model.

    This standalone model allows for direct management of product attributes
    (e.g., size, color) without navigating through the parent Product model.
    """
    list_display       = ["id", "product", "stock_quantity", "color", "size", "stock_availability", "created_on", "modified_on"]
    list_filter        = ["product", "size", "color", "availability", "height", "width", "length"]
    search_fields      = ["size", "color", "availability", "height", "width", "length", "id"]
    list_display_links = ["id", "product"]
    list_per_page      = 25

    
    fieldsets = [
        ("General Information", {"fields": ["product", "color", "size", "availability"]}),
        ("Dimensions", {"fields": ["height", "width", "length"]}),
        ("Stock Control", {"fields": ["stock_quantity", "minimum_stock_order", "maximum_stock_order"]}),
    ]

    readonly_fields = ["created_on", "modified_on"]
   
    def stock_availability(self, obj):
        """Return a readable display of the stock's availability."""
        return obj.stock_availability()


class BrandModelAdmin(admin.ModelAdmin):
    """
    Displays brand model in the admin interface.
    """
    list_display       = ["id", "name", "created_on", "modified_on"]
    list_per_page      = 25
    readonly_fields    = ["created_on", "modified_on"]
    search_fields      = ["name", "id"]
    list_display_links = ["id", "name"]



class ManufacturerAdmin(admin.ModelAdmin):
    """
    Displays manufacturer model in the admin interface.
    """
    list_display       = ["id", "name", "contact_num", "is_certified", "contact_num", "created_on", "modified_on"]
    list_per_page      = 25
    readonly_fields    = ["created_on", "modified_on"]
    search_fields      = ["name", "contact_num", "id"]
    list_display_links = ["id", "name"]
    
    
    
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Brand, BrandModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(Shipping, ShippingAdmin)

