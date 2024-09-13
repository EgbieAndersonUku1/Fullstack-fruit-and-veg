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
    is_temp_ban       = models.BooleanField(_("is_temp_ban"), default=False)
    last_login        = models.DateTimeField(_("last login"), auto_now=True) 
    date_created      = models.DateTimeField(_("date created"), auto_now_add=True)
    verification_data = models.JSONField(default=dict, blank=True, null=False)
    banned_data       = models.JSONField(default=dict, blank=True, null=False)
    ban_reason        = models.CharField(max_length=255, blank=True, null=True)


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
        HAS_EXPIRED  = "EXPIRED"
        INVALID_CODE =  "Ivalid code"
        if not self.verification_data:
            return False, INVALID_CODE

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
        """
        Permanently ban the user from accessing the application.

        This method sets the `is_banned` flag to `True` and ensures that any 
        temporary ban (`is_temp_ban`) is also cleared. The user instance is 
        saved after applying the ban.
        
        Returns:
            None
        """
        if not self.is_banned:
            self.is_banned = True
            self.is_temp_ban = False
            self.save()

    def un_ban(self):
        """
        Lift the permanent or temporary ban on the user.

        This method resets both the `is_banned` and `is_temp_ban` flags to `False`, 
        unbanning the user and restoring their access to the application. The user 
        instance is saved after lifting the ban.
        
        Returns:
            None
        """
        if self.is_banned:
            self.is_banned = False
            self.is_temp_ban = False
            self.save()

    def is_user_already_banned(self):
        """
        Check if the user is already banned.

        This method checks whether the user has a permanent or temporary ban 
        and returns a corresponding message. If the user is not banned, it returns `None`.

        Returns:
            str or None: A message indicating the ban type if the user is banned, 
                        or `None` if no ban exists.
        """
        BAN_MESSAGE = "User already has a permanent ban"
        TEMP_BAN_MESSAGE = "User already has a temporary ban"

        if self.is_banned:
            return BAN_MESSAGE
        elif self.is_temp_ban:
            return TEMP_BAN_MESSAGE
        return None

    def ban_for_x_amount_of_days(self, ban_reason: str = None, num_of_days_to_ban: int = 30, save: bool = True):
        """
        Temporarily ban the user for a specified number of days.

        This method bans the user for a given period, specified in `num_of_days_to_ban`. 
        The ban reason can optionally be provided and will be stored in the `ban_reason` field.
        If the `num_of_days_to_ban` is not an integer, a `TypeError` will be raised.

        Args:
            ban_reason (str, optional): The reason for the ban, limited to 255 characters.
            num_of_days_to_ban (int, optional): The number of days for which the user will be banned.
                                                Defaults to 30 days. Must be an integer.
            save (bool, optional): Whether to save the instance after applying the ban.
                                Defaults to `True`. Set to `False` to defer saving.

        Raises:
            TypeError: If `num_of_days_to_ban` is not an integer.

        Returns:
            bool or str: `True` if the ban is applied successfully, or a message indicating 
                        if the user is already banned (permanently or temporarily).
        """
        is_banned_resp = self.is_user_already_banned()

        if is_banned_resp is None:
            if not isinstance(num_of_days_to_ban, int):
                raise TypeError("The number of days to ban must be an integer")
            
            current_date = datetime.now()
            if ban_reason:
                self.ban_reason = ban_reason[:255]
            self.banned_data = {
                "date_ban_was_sent": current_date.isoformat(),
                "ban_expires_on": (current_date + timedelta(days=num_of_days_to_ban)).isoformat()
            }
            self.is_banned = False
            self.is_temp_ban = True

            if save:
                self.save()
            return True
        return is_banned_resp

    def has_ban_expired(self) -> bool:
        """
        Check if the user's temporary ban has expired.

        This method compares the current date to the ban expiration date stored 
        in `banned_data`. If the user has a permanent ban (`is_banned=True`), it 
        always returns `False`.

        Returns:
            bool: `True` if the temporary ban has expired, `False` otherwise.
        """
        # If the user is permanently banned, the ban hasn't expired
        if self.is_banned:
            return False

        if self.is_temp_ban and self.banned_data:
            try:
                ban_expires_on = datetime.fromisoformat(self.banned_data.get("ban_expires_on"))
                return datetime.now() > ban_expires_on  
            except (TypeError, ValueError):
                return False
        return False

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
        

class ActiveUserProxy(User):
    """
    Proxy model for the User class representing a active users.

    This proxy model allows for custom behaviour or display options for 
    users who are have active status,
    """
    class Meta:
        proxy = True
        verbose_name = "Active User"
        verbose_name_plural = "Active Users"
        


class NonActiveUserProxy(User):
    """
    Proxy model for the User class representing a active users.

    This proxy model allows for custom behaviour or display options for 
    users who are have active status,
    """
    class Meta:
        proxy = True
        verbose_name = "Non-active User"
        verbose_name_plural = "Non-active Users"