from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()


from utils.country_parser import parse_country_file
COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")

# Create your models here.

class Testimonial(models.Model):
    """The testimonal class"""
    
    author               = models.ForeignKey(User, max_length=40, on_delete=models.CASCADE, related_name="testimonals")
    title                = models.CharField(max_length=40)
    user_image           = models.URLField(verbose_name="User image url", null=True, blank=True)
    testimonial_text     = models.TextField()
    ratings              = models.SmallIntegerField()
    company_name         = models.CharField(max_length=50)
    country              = models.CharField(max_length=40, choices=COUNTRIES_CHOICES, default=COUNTRIES_CHOICES[0])
    location             = models.CharField(max_length=40)
    is_approved          = models.BooleanField(default=False)
    date_approved        = models.DateTimeField(blank=True, null=True)
    featured             = models.BooleanField(default=False)
    date_sent            = models.DateTimeField(auto_now_add=True)
    admin_response       = models.CharField(max_length=40, blank=True, null=True)   
    has_admin_responded  = models.BooleanField(default=False)
    tags                 = models.ManyToManyField("Tag", blank=True)
    date_created         = models.DateTimeField(auto_now_add=True) 
    updated_on           = models.DateTimeField(auto_now=True)   

    class Meta:
        verbose_name        = "Testimonial"
        verbose_name_plural = "All Testimonials"
        
    def __str__(self) -> str:
        """Returns a user friendly representation of the author and the title for the testimonal model"""
        return f'{self.author} - {self.title[:50]}'
    
    @classmethod
    def get_by_user(cls, user):
        """
        Takes a user instance and returns the testimonial belonging to that user
        
        Params:
            user (instance): The user instance belonging to the user that will be used to retreive their testimonial
            
        Returns:
            Returns the testimonial object belonging to the user or returns none.
        """
        try:
            return cls.objects.get(author=user)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_user_and_id(cls, user, testimonial_id):
        """
        Retrieves a testimonial by the given user and testimonial ID.
        
        Params:
            user (User instance): The user instance to retrieve the testimonial for.
            testimonial_id (int): The ID of the testimonial.

        Returns:
            Testimonial instance: The testimonial object or None if not found.
        """
        return cls.objects.filter(author=user, id=testimonial_id).first()
    

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
    
class UnapprovedTestimonial(Testimonial):
    """A proxy model that displays testimonials that have not been approved."""
    
    class Meta:
        proxy = True
        verbose_name = "Unapproved Testimonial"
        verbose_name_plural = "Unapproved Testimonials"


class ApprovedTestimonial(Testimonial):
    """A proxy model that displays testimonials that have been approved."""
    
    class Meta:
        proxy = True
        verbose_name = "Approved Testimonial"
        verbose_name_plural = "Approved Testimonials"



class TestimonialMessages:
    ERROR_EDITING_OTHER_TESTIMONIAL = "You cannot edit someone else's testimonial."
    ERROR_TESTIMONIAL_NOT_FOUND     = "The testimonial was not found."
    SUCCESS_TESTIMONIAL_UPDATED     = "Testimonial updated successfully!"