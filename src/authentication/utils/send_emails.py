
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.utils.send_email import send_email


def send_registration_email(subject, from_email, user, verification_url):
    
    email_template_html     = "email_assets/registration/registration.html"
    email_template_text     = "email_assets/registration/registration.txt"
    
    return send_email(subject=subject,
                      from_email=from_email,
                      to_email=user.email,
                      email_template=email_template_html,
                      text_template=email_template_text,
                      context={"username": user.username.title(), 
                               "verification_url": verification_url
                               }
            
               )