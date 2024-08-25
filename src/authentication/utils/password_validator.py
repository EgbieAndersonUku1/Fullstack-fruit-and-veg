import re

class PasswordStrengthChecker:
    """
    A class to check the strength of a password based on various criteria.

    Attributes:
        password (str): The password to be checked.
        default_length (int): The minimum length required for the password.
    """
    
    def __init__(self, password, default_length=8) -> None:
        """
        Initializes the PasswordStrengthChecker with a password and a default minimum length.

        Args:
            password (str): The password to be checked.
            default_length (int, optional): The minimum length required for the password. Defaults to 8.
        """
        self.password = password
        self.default_length = default_length

    def set_password(self, password:str) -> None:
        """
        Sets a new password.

        Args:
            password (str): The new password to be checked.
        """
        self.password = password
    
    def set_password_length(self, password_length:int) -> None:
        """
        Sets a new minimum length requirement for the password.

        Args:
            password_length (int): The new minimum length for the password.
        """
        self.default_length = password_length
    
    def contains_at_least_length_chars(self) -> bool:
        """
        Checks if the password contains at least the minimum required number of characters.

        Returns:
            bool: True if the password's length is greater than or equal to the default length, otherwise False.
        """
        return len(self.password) >= self.default_length
    
    def contains_at_least_one_number(self) -> bool:
        """
        Checks if the password contains at least one numeric digit.

        Returns:
            bool: True if the password contains at least one digit, otherwise False.
        """
        return bool(re.search(r'\d', self.password))
    
    def contains_lowercases(self) -> bool:
        """
        Checks if the password contains at least one lowercase letter.

        Returns:
            bool: True if the password contains at least one lowercase letter, otherwise False.
        """
        return bool(re.search(r'[a-z]', self.password))
    
    def contains_uppercases(self) -> bool:
        """
        Checks if the password contains at least one uppercase letter.

        Returns:
            bool: True if the password contains at least one uppercase letter, otherwise False.
        """
        return bool(re.search(r'[A-Z]', self.password))
    
    def contains_special_chars(self) -> bool:
        """
        Checks if the password contains at least one special character (non-alphanumeric).

        Returns:
            bool: True if the password contains at least one special character, otherwise False.
        """
        return bool(re.search(r'[\W_]', self.password))
    
    def is_strong_password(self) -> bool:
        """
        Evaluates whether the password is strong based on all criteria:
        - Minimum length
        - At least one digit
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one special character

        Returns:
            bool: True if the password meets all the criteria, otherwise False.
        """
        return (self.contains_at_least_length_chars() and
                self.contains_at_least_one_number() and
                self.contains_lowercases() and
                self.contains_uppercases() and
                self.contains_special_chars())

    
            