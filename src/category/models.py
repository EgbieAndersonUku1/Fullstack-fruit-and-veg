from django.db import models

from authentication.models import User


# Create your models here.
class AllDepartmentsModel(models.Model):
    
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    @classmethod  
    def get_all_departments(cls):
        """
        Retrieves all departments associated with a given user.

        Args:
            user (User): The user instance used to retrieve the departments.

        Returns:
            QuerySet: A queryset containing all departments associated with the user.

        Raises:
            TypeError: If the provided user is not an instance of the User class.
        """
        return cls.objects.order_by('name')

        