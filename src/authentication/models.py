from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _



from typing import Optional

# Create your models here.


class CustomBaseUser(BaseUserManager):
    
    def create_superuser(self, username:str, email:str, password:str=None, **extra_fields) -> "User":
        """
        Creates a super user with the given username, email, and password.

        Parameters:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields (Any): Additional keyword arguments for user creation.

        Returns:
            User: The created user object.
        """
      
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(username, email, password, **extra_fields)
    
    def create_user(self, username:str, email:str, password:str=None, **extra_fields:any) -> "User":
        """
        Creates a new user with the given username, email, and password.

        Parameters:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields (Any): Additional keyword arguments for user creation.

        Returns:
            User: The created user object.
        """
        self._is_valid(email, username)
        
        email = self.normalize_email(email)
        user  = self.model(username=username, email=email, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def _is_valid(self, email:str, username:str) -> None:
        """
        Validates if an email and username field is correct

        Parameters:
            username (str): The username of the user.
            email (str): The email address of the user.
          
        Returns:
          Returns a none value
        """
        if not email:
            raise ValueError("The email field cannot be empty")
        if not username:
            raise ValueError("The username field cannot be empty")
        
        
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model extending AbstractBaseUser and PermissionsMixin."""

    username          = models.CharField(_("username"), max_length=20, unique=True)
    email             = models.EmailField(_("email"), max_length=40, unique=True)
    is_active         = models.BooleanField(_("is active"), default=True)
    is_staff          = models.BooleanField(_("is staff"), default=False)
    is_superuser      = models.BooleanField(_("is superuser"), default=False)
    is_admin          = models.BooleanField(_("is admin"), default=False)
    is_email_verified = models.BooleanField(_("is email verified"), default=False)
    is_banned         = models.BooleanField(_("is banned"), default=False) 
    last_login        = models.DateTimeField(_("last login"), auto_now=True) 
    date_created      = models.DateTimeField(_("date created"), auto_now_add=True)
    verification_data = models.JSONField(default=dict, blank=True, null=False)

    objects = CustomBaseUser()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

   
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'  
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'  
    )
    
    def __str__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
            str: The email address of the user.
        """
        return self.email

    @classmethod
    def get_by_email(cls, email:str) -> Optional["User"]:
        """
        Retrieve a user instance by email address.

        This method abstracts the process of querying the user database by email and also handles 
        any errors if it is not found.
 
        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User or None: The user instance if found, or None if no user matches the email.
        """
        return cls._get_user_model(email, value_type="email")

    @classmethod
    def get_by_username(cls, username:str) -> Optional["User"]:
        """
        Retrieve a user instance by username.

        This method abstracts the process of querying the user database by username
        any errors if it is not found..

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User or None: The user instance if found, or None if no user matches the username.
        """
        return cls._get_user_model(username, value_type="username")

    @classmethod
    def _get_user_model(cls, value:str, value_type:str="email") -> Optional["User"]:
        """
        Private method to retrieve a user instance based on the specified field.

        Args:
            value (str): The value to query (email or username).
            value_type (str): The type of value ('email' or 'username').

        Returns:
            User or None: The user instance if found, or None if no user matches the criteria.
        """
        try:
            if value_type.lower() == "username":
                return cls.objects.get(username=value)
            elif value_type.lower() == "email":
                return cls.objects.get(email=value)
        except cls.DoesNotExist:
            return None
    
    def set_verification_code(self, code:str, expiry_minutes:int) -> None:
        """Set the verification data in the JSONField.
        
           Args:
                code: The verification code to set to JSONField 
                expiry_minutes: The minutes that code will expiry by
             
           Returns:
                Returns none
        """
        current_date = datetime.now()
        self.verification_data = {
            "verification_code": code,
            "date_sent": current_date.isoformat(),
            "expiry_date": (current_date + timedelta(minutes=expiry_minutes)).isoformat()
        }
        self.save()
    
    def clear_verification_data(self) -> None:
        """Clear the verification data"""
        self.verification_data = {}
        self.save()
    
    def is_verification_code_valid(self, verifcation_code:str) -> bool:
        """
        Checks if the verification code is valid
        
        Args:
            verification_code (str): The verificatin code to check.
           
        Returns:
            Returns True if valid or False not

        """
        if not self.verification_data:
            return False
      
        stored_code = self.verification_data.get("verification_code")
     
        if stored_code != verifcation_code:
            return False
        
        try:
            expiry_date         = self.verification_data.get('expiry_date')
            expiration_datetime = datetime.fromisoformat(expiry_date)
            return expiration_datetime >= datetime.now()
        except TypeError:
            return False
        
    
    def ban(self):
        """Ban the user from using the application"""
        if not self.is_banned:
            self.is_banned = True
            self.save()
    
    def un_ban(self):
        """Unban the user from using the application"""
        if self.is_banned:
            self.is_banned = False
            self.save()
        
    def mark_email_as_verified(self):
        """
        Mark the user's email as verified and save the updated instance.

        This method sets the `is_emailed_verified` field to `True` and
        persists the change to the database. It is typically called when
        a user successfully verifies their email address.

        Example:
            user = User.objects.get(email='user@example.com')
            user.mark_email_as_verified()

        Note:
            This method does not perform any additional checks or validations.
            It directly updates the field and saves the instance.
        """
        if not self.is_email_verified:
            self.is_email_verified = True
            self.save()
    