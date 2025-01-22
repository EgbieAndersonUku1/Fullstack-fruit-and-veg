from django.db import models
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, is_naive
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from typing import Optional
from utils.dates import calculate_days_between_dates, is_date_valid
from utils.utils import get_local_ip_address



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

    username                 = models.CharField(_("username"), max_length=20, unique=True, db_index=True)
    email                    = models.EmailField(_("email"), max_length=40, unique=True, db_index=True)
    is_active                = models.BooleanField(_("is active"), default=True)
    is_staff                 = models.BooleanField(_("is staff"), default=False)
    is_superuser             = models.BooleanField(_("is superuser"), default=False)
    is_admin                 = models.BooleanField(_("is admin"), default=False)
    is_email_verified        = models.BooleanField(_("is email verified"), default=False)
    is_banned                = models.BooleanField(_("is banned"), default=False) 
    is_temp_ban              = models.BooleanField(_("is_temp_ban"), default=False)
    last_login               = models.DateTimeField(_("last login"), auto_now=True) 
    date_created             = models.DateTimeField(_("date created"), auto_now_add=True)
    verification_data        = models.JSONField(default=dict, blank=True, null=False)
    last_token_generated_on  = models.DateTimeField(null=True, blank=True)
  
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

    def is_token_request_allowed(self):
        """
        Check if sufficient time has passed since the last token was generated.
        """
        
        TEN_MINUTES_IN_SECS = 600
        current_date        = make_aware(datetime.now())
        
        if self.last_token_generated_on:
            time_since_last_token = (current_date - self.last_token_generated_on).total_seconds()
            return time_since_last_token >= TEN_MINUTES_IN_SECS
        return True

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
                return cls.objects.get(username=value.lower())
            elif value_type.lower() == "email":
                return cls.objects.get(email=value.lower())
        except cls.DoesNotExist:
            return None
    
    def set_verification_code(self, code: str, expiry_minutes: int, save: bool = True, default_key: str = "verification_code") -> None:
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
            default_key (str, optional): The key under which to store the verification data.
                                        Defaults to `"verification_code"`.

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
            Different keys (e.g., `"verify_forgotten_password"`) can be used to handle different
            types of verifications.
        """
        
        current_date = datetime.now()

        self.verification_data[default_key.lower()] = {
            "verification_code": code,
            "date_sent": current_date.isoformat(),
            "expiry_date": (current_date + timedelta(minutes=expiry_minutes)).isoformat()
        }
        self.last_token_generated_on = make_aware(datetime.now())
        if save:
            self.save()

    
    def clear_verification_data(self, save: bool = True, default_key: str = "verification_code") -> None:
        """
        Clear the specified verification data from the user's account.

        This method removes the verification information stored under a specific key in the 
        `verification_data` JSONField (default is `"verification_code"`). By default, the 
        instance is saved to the database after the key is deleted, but you can defer saving 
        by setting the `save` parameter to `False`. This is useful when performing multiple 
        updates on the user instance and saving all changes at once.

        Args:
            save (bool): Whether to save the instance after clearing the specified verification data. 
                        Defaults to `True`. Set to `False` to defer saving.
            default_key (str, optional): The key to clear from the `verification_data`. 
                                        Defaults to `"verification_code"`.

        Example:
            user = User.objects.get(email='user@example.com')
            user.clear_verification_data(save=False)  # Clear data without saving
            user.perform_other_updates()
            user.save()  # Save all changes at once

        Note:
            - This method does not raise an error if the specified key does not exist.
            - It directly updates the `verification_data` field and saves the instance if `save=True`.
        """
        
        try:
            del self.verification_data[default_key]
        except KeyError:
            pass
        else:
            if save:
                self.save()

    def is_verification_code_valid(self, verification_code: str, default_key: str = "verification_code") -> tuple[bool, str]:
        """
        Validates the given verification code and checks if it has expired.

        This method verifies whether the provided `verification_code` matches the code stored in 
        the user's `verification_data` (under the specified `default_key`) and checks if the 
        code has expired based on its expiration date.

        Args:
            verification_code (str): The verification code to validate.
            default_key (str, optional): The key in the `verification_data` where the verification 
                                        code is stored. Defaults to `"verification_code"`.

        Returns:
            tuple: A tuple where the first element is a boolean indicating if the code is valid, 
                and the second element is a string indicating the status:
                - `"EXPIRED"` if the code has expired,
                - `"INVALID_CODE"` if the code does not match or the verification data is missing,
                - `None` if the code is valid and not expired.

        Example:
            user = User.objects.get(email='user@example.com')
            is_valid, status = user.is_verification_code_valid(verification_code='123456')

            if is_valid:
                print("Verification successful")
            elif status == "EXPIRED":
                print("Verification code has expired")
            else:
                print("Invalid verification code")

        Note:
            - This method assumes that the `verification_data` contains the necessary keys for 
            `"verification_code"` and `"expiry_date"`. 
            - In case of missing or invalid data, it returns the appropriate status to indicate the issue.
        """
        HAS_EXPIRED  = "EXPIRED"
        INVALID_CODE = "INVALID_CODE"

        verification_data = self.verification_data.get(default_key, {})
     
        
        if not verification_data:
            return False, INVALID_CODE


        stored_code = verification_data.get("verification_code")

        if stored_code != verification_code:
            return False, INVALID_CODE

        try:
            expiry_date = verification_data.get("expiry_date")
            expiration_datetime = datetime.fromisoformat(expiry_date)

            if expiration_datetime < datetime.now():
                return False, HAS_EXPIRED
            return True, None

        except (TypeError, ValueError):
            return False, None

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


class BanUser(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bans")
    ban_reason          = models.TextField()  
    ban_start_date      = models.DateTimeField(null=True, blank=True)
    ban_expires_on      = models.DateTimeField(null=True, blank=True)
    modified_on         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "All banned users"
        verbose_name_plural = "All banned users"
        
    def __str__(self):
        return f"{self.user} banned for {self.ban_reason}"

    @property
    def start_date(self):
        """Mostly for the admin interface. When called displays the start date of the ban"""
        return self.ban_start_date
    
    @property
    def expires_on(self):
        """Mostly for the admin interface. When called displays the date the ban will end"""
        return self.ban_expires_on
    
    
    @property
    def username(self):
        """Mostly for the admin interface. When called displlays the name of the user who is banned"""
        return self.user.username.title()
    
    @property
    def ban_duration_days(self):
        """Return the total number of days for the ban."""
        if self.ban_start_date and self.ban_expires_on:
            return calculate_days_between_dates(self.ban_expires_on, self.ban_start_date)
        return None
       
    @property
    def remaining_days(self):
        """Return the number of days remaining until the ban expires."""
        
        if not self.ban_expires_on:
            return None
        current_date = make_aware(datetime.now())
        if self.ban_expires_on < current_date:
            return 0
        return calculate_days_between_dates(self.ban_expires_on, current_date)
      
    
    def ban(self):
        """
        Permanently ban the user from accessing the application.
        """
        if not self.user.is_banned:
            self.user.is_banned = True
            self.user.is_temp_ban = False
            self.user.save()

    def un_ban(self):
        """
        Lift the permanent or temporary ban on the user.
        """
        if self.user.is_banned or self.user.is_temp_ban:
            self.user.is_banned = False
            self.user.is_temp_ban = False
            self.user.save()

    def is_user_already_banned(self):
        """
        Check if the user is already banned.
        """
        if self.user.is_banned:
            return "User already has a permanent ban"
        elif self.user.is_temp_ban:
            return "User already has a temporary ban"
        return None
    
    def ban_for_x_amount_of_days(self, num_of_days_to_ban: int = 30, save: bool = True):
        """
        Temporarily ban the user for a specified number of days starting from the day of the ban.
        
        Parameters:
          - num_of_days_to_ban (int): The number of days to ban a given user
          
          - save (bool): Optional. If True (default), saves the updated `BanUser` 
          instance and the associated `User` object to the database. If False, 
          the method returns the updated `BanUser` instance without saving.

        Raises:
        - TypeError: If num_of_days_to_ban is not int 
        
        Returns:
        - True if `save` is True.
        - The updated `BanUser` instance if `save` is False.

        Example:
        >>> ban_user_instance = BanUser.objects.get(user=some_user)
        >>> ban_user_instance.ban_for_x_amount_of_days(num_of_days_to_ban=10)
        """
        is_banned_resp = self.is_user_already_banned()

        if is_banned_resp is None:
            if not isinstance(num_of_days_to_ban, int):
                raise TypeError("The number of days to ban must be an integer")

            self.ban_start_date   = make_aware(datetime.now())
            self.ban_expires_on   = self.ban_start_date + timedelta(days=num_of_days_to_ban)

            self.user.is_banned   = False
            self.user.is_temp_ban = True
            self.user.save()
            
            if save:
                self.save()
                return True
            else:
                return self
        return is_banned_resp

    def ban_for_date_range(self, start_date, end_date, save=True):
        """
        Temporarily bans a user for a specified date range.

        This method sets a ban on the user from the provided start date to the end date.
        If `save` is set to True, the  changes are saved to the database. If `save` is False, 
        the instance is returned for further modifications or inspection.

        Parameters:
        - start_date (datetime): The start date and time for the ban. Must be a valid 
          `datetime` object and should be earlier than the `end_date`.
          
        - end_date (datetime): The end date and time for the ban. Must be a valid 
          `datetime` object and should be later than the `start_date`.
          
        - save (bool): Optional. If True (default), saves the updated `BanUser` 
          instance and the associated `User` object to the database. If False, 
          the method returns the updated `BanUser` instance without saving.

        Raises:
        - ValueError: If either `start_date` or `end_date` is not a valid `datetime` 
          object, or if `start_date` is not earlier than `end_date`.

        Returns:
        - None if `save` is True.
        - The updated `BanUser` instance if `save` is False.

        Example:
        >>> ban_user_instance = BanUser.objects.get(user=some_user)
        >>> ban_user_instance.ban_for_date_range(datetime(2024, 9, 1), datetime(2024, 9, 30))
       """
       
        if not is_date_valid(start_date) and not is_date_valid(end_date):
            raise ValueError("The dates entered must be datetime objects")
        
        if start_date > end_date:
            raise ValueError("The start date cannot be greater than the end date")
        
        is_banned_resp = self.is_user_already_banned()
        
        if is_banned_resp is None:
            
            self.ban_start_date = make_aware(start_date) if is_naive(start_date) else start_date
            self.ban_expires_on = make_aware(end_date) if is_naive(end_date) else end_date
            
            self.user.is_temp_ban = True
            self.user.is_banned   = False
            self.user.save()
        
            if save:
                self.save()
            else:
                return self
        return is_banned_resp
    
    def has_ban_expired(self) -> bool:
        """
        Check if the user's temporary ban has expired.
        """
        if self.user.is_banned:
            return False

        if self.user.is_temp_ban:
            current_date = make_aware(datetime.now())
            return current_date > self.ban_expires_on
        
        return False

    
    
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


class TempBannedUserProxy(User):
    """
    Proxy model for the User class representing a banned user.

    This proxy model allows for custom behaviour or display options for 
    users who are banned, while leveraging the existing User model's 
    database structure.
    """
    class Meta:
        proxy = True
        verbose_name = "Temporary Banned User"
        verbose_name_plural = "Temporary Banned Users"


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
        

class UserDevice(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_devices")
    local_ip          = models.GenericIPAddressField(null=False, verbose_name="Local Device IP Address", default=get_local_ip_address)  # local device ip e.g 192.168.x.x
    frontend_timezone = models.CharField(max_length=100, null=False, db_index=True, verbose_name="Frontend Time Zone")
    backend_timezone  = models.CharField(max_length=100, null=False, db_index=True, verbose_name="Backend Time Zone")
    user_agent        = models.CharField(max_length=1000, null=False, db_index=True, verbose_name="User Agent")
    screen_width      = models.PositiveSmallIntegerField(null=False, db_index=False)
    screen_height     = models.PositiveSmallIntegerField(null=False, db_index=False)
    platform          = models.CharField(max_length=50, null=False, verbose_name="Operating System")
    pixel_ratio       = models.CharField(max_length=50, db_index=False, null=False)
    browser           = models.CharField(max_length=50, null=True, db_index=True) # e.g chrome
    browser_version   = models.CharField(max_length=50, null=True, db_index=True) # e.g version 131.1
    device            = models.CharField(max_length=60, null=True, blank=False, db_index=True) # e.g desktop, laptop
    is_touch_device   = models.BooleanField(default=False, verbose_name="Is Touchscreen Device")
    last_login        = models.DateTimeField(auto_now=True, verbose_name="Last Login Time")
    created_on        = models.DateTimeField(auto_now_add=True)
    modified_on       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "User Device"
        verbose_name_plural = "User Devices"
        
    def __str__(self):
        return f"{self.user.username} - <Platform: {self.platform}> - Screen Resolution: <{self.screen_resolution}>"
    
    @property
    def screen_resolution(self):
        return f"{self.screen_width}x{self.screen_height}"

    class Meta:
        verbose_name        = "User Device"
        verbose_name_plural = "User Devices"
        


class LoginAttempt(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_attempts")
    client_ip_address = models.GenericIPAddressField(db_index=True)
    host_name         = models.CharField(max_length=255)
    organization      = models.CharField(max_length=255)
    country           = models.CharField(max_length=255, db_index=True)
    city              = models.CharField(max_length=255, db_index=True)
    region            = models.CharField(max_length=255, db_index=True)
    longitude         = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    latitude          = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    timezone          = models.CharField(max_length=255, db_index=True)
    timestamp         = models.DateTimeField(auto_now_add=True)
    org               = models.CharField(max_length=255, null=True, blank=True, verbose_name="Organization")
    hostname          = models.CharField(max_length=255, null=True, blank=True, verbose_name="Hostname")
    is_successful     = models.BooleanField(default=False)
    created_on        = models.DateTimeField(auto_now_add=True)
    modified_on       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"
        indexes = [
            models.Index(fields=["client_ip_address", "timestamp"]),
            models.Index(fields=["country", "region", "city"]),
        ]

    def __str__(self):
        return f"LoginAttempt(user:{self.user}, ip:{self.client_ip_address}, success:{self.is_successful})"
