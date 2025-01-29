from django.core.files.uploadedfile import SimpleUploadedFile

import factory

from product.models import Category, Product, ProductVariation, Shipping, Manufacturer, Brand


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating instances of the Category model.

    This factory generates fake data for the 'category' and 'description' fields 
    using the Faker library, which generates random words and sentences.

    Fields:
        category (str): A randomly generated word representing the category name.
        description (str): A randomly generated sentence describing the category.
    """
    class Meta:
        model = Category
    
    category    = factory.Faker("word")
    description = factory.Faker("sentence")


class BrandFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating instances of the Brand model.

    This factory generates fake data for the 'name' and 'description' fields 
    using the Faker library, which generates random names and sentences.

    Fields:
        name (str): A randomly generated brand name.
        description (str): A randomly generated description for the brand.
    """
    class Meta:
        model = Brand
        
    name        = factory.Faker("name")
    description = factory.Faker("sentence")


class ManufacturerFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating instances of the Manufacturer model.

    This factory generates fake data for the 'name', 'description', 'address',
    and 'contact_num' fields using the Faker library, which generates random
    names, addresses, paragraphs, and phone numbers.

    Fields:
        name (str): A randomly generated manufacturer name.
        description (str): A randomly generated description for the manufacturer.
        address (str): A randomly generated address for the manufacturer.
        contact_num (str): A randomly generated phone number for the manufacturer.
    """
    class Meta:
        model = Manufacturer
    
    name        = factory.Faker("name")
    description = factory.Faker("paragraph")
    address     = factory.Faker("address")
    contact_num = factory.Faker("phone_number")


class ProductFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating instances of the Product model.

    This factory generates fake data for various fields, including 'name',
    'long_description', 'short_description', 'price', 'weight', 'primary_image',
    'side_image', and 'side_image_2'. It also automatically generates related
    models for 'brand', 'category', and 'manufacturer'.

    Fields:
        name (str): A randomly generated product name.
        long_description (str): A randomly generated long description of the product.
        short_description (str): A randomly generated short description of the product.
        brand (Brand): A randomly generated Brand instance related to the product.
        category (Category): A randomly generated Category instance related to the product.
        price (decimal): A randomly generated price for the product.
        weight (int): A randomly generated weight for the product.
        primary_image (Image): A lazy-loaded image for the primary image field.
        side_image (Image): A lazy-loaded image for the side image field.
        side_image_2 (Image): A lazy-loaded image for the second side image field.
        manufacturer (Manufacturer): A randomly generated Manufacturer instance related to the product.
        country_of_origin (str): A randomly generated country of origin.
    """
    class Meta:
        model = Product
    
    name              = factory.Faker("name")
    long_description  = factory.Faker("sentence", nb_words=100)
    short_description = factory.Faker("paragraph")
    brand             = factory.SubFactory(BrandFactory)
    category          = factory.SubFactory(CategoryFactory)
    price             = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    weight            = factory.Faker("random_int", min=1, max=100) 
    primary_image     = factory.LazyAttribute(lambda _: SimpleUploadedFile("primary_image.jpg", b"file_content", content_type="image/jpeg"))
    side_image        = factory.LazyAttribute(lambda _: SimpleUploadedFile("side_image.jpg", b"file_content", content_type="image/jpeg"))
    side_image_2      = factory.LazyAttribute(lambda _: SimpleUploadedFile("side_image_2.jpg", b"file_content", content_type="image/jpeg"))
    manufacturer      = factory.SubFactory(ManufacturerFactory)
    country_of_origin = factory.Faker("country")
