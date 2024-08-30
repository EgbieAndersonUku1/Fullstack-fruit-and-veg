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
    
    def set_verification_code(self, code: str, expiry_minutes: int, save:bool=True) -> None:
        """
        Set the verification code and its expiration time in the user's verification data.

        This method updates the `verification_data` JSONField with a verification code, the date
        it was sent, and its expiry date. The instance is saved to the database by default, but
        this can be controlled with the `save` parameter.

        Args:
            code (str): The verification code to set in the `verification_data`.
            expiry_minutes (int): The number of minutes after which the verification code expires.
            save (bool, optional): Whether to save the instance after setting the verification code.
                                Defaults to `True`. Set to `False` to defer saving.

        Returns:
            None

        Example:
            user = User.objects.get(email='user@example.com')
            user.set_verification_code(code='123456', expiry_minutes=30, save=False)  # Set code without saving
            user.perform_other_updates()
            user.save()  # Save all changes at once

        Note:
            This method does not perform any validation on the verification code or the expiration time.
            It directly updates the `verification_data` field and saves the instance if `save=True`.
        """
        current_date = datetime.now()
        self.verification_data = {
            "verification_code": code,
            "date_sent": current_date.isoformat(),
            "expiry_date": (current_date + timedelta(minutes=expiry_minutes)).isoformat()
        }

        if save:
            self.save()
    
    def clear_verification_data(self, save:bool=True) -> None:
        """
        Clear the user's verification data and optionally save the updated instance.

        This method sets the `verification_data` field to an empty dictionary (`{}`).
        By default, it saves the instance to the database, but you can prevent an immediate
        save by setting the `save` parameter to `False`. This is useful when you want to 
        perform multiple operations on the user instance and save all changes at once.

        Args:
            save (bool): Whether to save the instance after clearing the verification data. 
                        Defaults to `True`. Set to `False` to defer saving.

        Example:
            user = User.objects.get(email='user@example.com')
            user.clear_verification_data(save=False)  # Clear data without saving
            user.perform_other_updates()
            user.save()  # Save all changes at once

        Note:
            This method does not perform any additional checks or validations.
            It directly updates the `verification_data` field and saves the instance if `save=True`.
        """
        self.verification_data = {}

        if save:
            self.save()

    
    def is_verification_code_valid(self, verification_code: str) -> tuple[bool, str]:
        """
        Checks if the verification code is valid and if it has expired.

        Args:
            verification_code (str): The verification code to check.

        Returns:
            tuple: A tuple where the first element is a boolean indicating
                if the code is valid, and the second element is a string
                indicating the status:
                - 'EXPIRED' if the code has expired,
                - None if the code is invalid or the verification data is missing.
        """
        HAS_EXPIRED = "EXPIRED"
        if not self.verification_data:
            return False, None

        stored_code = self.verification_data.get("verification_code")
        
        if stored_code != verification_code:
            return False, None

        try:
            expiry_date = self.verification_data.get('expiry_date')
            expiration_datetime = datetime.fromisoformat(expiry_date)
            
            if expiration_datetime < datetime.now():
                return False, HAS_EXPIRED
            return True, None
        
        except (TypeError, ValueError):
            return False, None
    
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
        
    def mark_email_as_verified(self, save:bool=True):
        """
        Mark the user's email as verified and optionally save the updated instance.

        This method sets the `is_email_verified` field to `True`. By default, it
        saves the instance to the database. However, you can prevent an immediate
        save by setting the `save` parameter to `False`. This can be useful if you 
        need to perform multiple updates on the user instance without hitting the 
        database each time.

        Args:
            save (bool): Whether to save the instance after marking the email as verified. 
                        Defaults to `True`. Set to `False` to defer saving.

        Example:
            user = User.objects.get(email='user@example.com')
            user.mark_email_as_verified(save=False)  # Mark as verified without saving
            user.perform_other_updates()
            user.save()  # Save all changes at once

        Note:
            This method does not perform any additional checks or validations.
            It directly updates the `is_email_verified` field and saves the instance if `save=True`.
        """
        if not self.is_email_verified:
            self.is_email_verified = True

        if save:
            self.save()

    
    @classmethod
    def does_user_exists(cls, username):
        """
        Check if a user with the given username exists in the database.

        This class method queries the database to determine if a user with
        the specified username is present. It returns a boolean indicating
        the existence of the user.

        This method doesn't load a user object into memory; it only checks
        for the existence of a user. It can be called without instantiating 
        the class.

        Args:
            username (str): The username to search for in the database.

        Returns:
            bool: True if a user with the given username exists, False otherwise.
        """
        return cls.objects.filter(username=username).exists()



class VerifiedUserProxy(User):
    """
    Proxy model for the User class representing a verified user.

    This proxy model is used to differentiate verified users and provide 
    additional functionality or behaviour specific to them without altering 
    the original User model or creating a new database table.
    """
    class Meta:
        proxy = True
        verbose_name = "Verified User"
        verbose_name_plural = "Verified Users"



class BannedUserProxy(User):
    """
    Proxy model for the User class representing a banned user.

    This proxy model allows for custom behaviour or display options for 
    users who are banned, while leveraging the existing User model's 
    database structure.
    """
    class Meta:
        proxy = True
        verbose_name = "Banned User"
        verbose_name_plural = "Banned Users"



class SuperUserProxy(User):
    """
    Proxy model for the User class representing a super users.

    This proxy model allows for custom behaviour or display options for 
    users who are have superuser status,
    """
    class Meta:
        proxy = True
        verbose_name = "Superuser"
        verbose_name_plural = "Superusers"
        
        

class AdminUserProxy(User):
    """
    Proxy model for the User class representing a admin users.

    This proxy model allows for custom behaviour or display options for 
    users who are have admin status,
    """
    class Meta:
        proxy = True
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"
        
        
        
class StaffUserProxy(User):
    """
    Proxy model for the User class representing a staff users.

    This proxy model allows for custom behaviour or display options for 
    users who are have staff status,
    """
    class Meta:
        proxy = True
        verbose_name = "Staff User"
        verbose_name_plural = "Staff Users"