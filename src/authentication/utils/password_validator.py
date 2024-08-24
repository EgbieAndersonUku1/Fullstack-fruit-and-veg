import re

class PasswordStrengthChecker:
    
    def __init__(self, password, default_length=8) -> None:
        self.password       = password
        self.default_length = default_length

        
    def set_password(self, password):
        self.password = password
    
    def set_password_length(self, password_length):
        self.default_length = password_length
    
    def contains_at_least_length_chars(self):
        return True if len(self.password) < self.password else False
    
    def contains_at_least_one_number(self):
        return 
    
    def contains_lowercases(self):
        pass
    
    def contains_uppercases(self):
        pass
    
    
    
            