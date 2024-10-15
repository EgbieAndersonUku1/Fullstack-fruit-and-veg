from django.conf import settings

from authentication.utils.send_email import send_email


def send_registration_email(subject, from_email, user, verification_url):
    """
    Sends a registration email to a new user with a verification link.

    This function uses pre-defined HTML and plain text email templates to send 
    a registration email to the specified user. The email includes a verification 
    link that the user must click to verify their email address and activate their account.

    Parameters:
    - subject (str): The subject line of the email.
    - from_email (str): The sender's email address.
    - user (User): The user object containing the recipient's information, such as their email address and username.
    - verification_url (str): The URL that the user should visit to verify their email address.

    Returns:
    - bool: True if the email was sent successfully, False otherwise.
    """
    
    email_template_html     = "email_assets/registration/registration.html"
    email_template_text     = "email_assets/registration/registration.txt"
    
    return _send_email_helper(
        email_template_html,
        email_template_text,
        subject=subject,
        from_email=from_email,
        to_email=user.email,
        username=user.username.title(),
        verification_url=verification_url
    )
   

def resend_expired_verification_email(subject, from_email, user, verification_url):
    """
    Sends an email to a user with a new verification token after the previous one has expired.
    This function uses pre-defined HTML and plain text email templates to re-send 
    a registration email to the specified user. The email includes a verification 
    link that the user must click to verify their email address and activate their account.

    
    Parameters:
    - subject (str): The subject line of the email.
    - from_email (str): The sender's email address.
    - user (User): The user object containing the recipient's information.
    - verification_url (str): The new verification URL for the user.

    Returns:
    - bool: True if the email was sent successfully, False otherwise.
    """
    email_template_html = "email_assets/registration/registration-expiry-notification.html"
    email_template_text = "email_assets/registration/registration-expiry-notification.txt"
    
    return _send_email_helper(
        email_template_html,
        email_template_text,
        subject=subject,
        from_email=from_email,
        to_email=user.email,
        username=user.username.title(),
        verification_url=verification_url
    )
  
  
def send_forgotten_password_verification_email(subject, from_email, user, verification_url):
    
    email_template_html = "email_assets/forgotten-password/forgotten-password-request.html"
    email_template_text = "email_assets/forgotten-password/forgotten-password-request.txt"
    
    return _send_email_helper(
        email_template_html,
        email_template_text,
        subject=subject,
        from_email=from_email,
        to_email=user.email,
        username=user.username.title(),
        verification_url=verification_url,
        email_address=user.email,
    )
    

def notify_admin_of_new_testimonial(subject, user):
    """
    Sends an email to the admin of the site to notify them that a new testimonial has been
    created and is waiting for their approval
    """
    email_template_html = "email_assets/testimonial/testimonial.html"
    email_template_text = "email_assets/testimonial/testimonial.txt"
    
    admin_email_address = settings.EMAIL_HOST_USER
    
    return _send_email_helper(email_template_html,
                             email_template_text,
                             subject=subject,
                             from_email=admin_email_address,
                             to_email=admin_email_address,
                             username=user.username,
                             email_address=user.email,
                             )



def notify_user_of_approved_testimonial(subject, user):
    """
    Sends an email to the user that their testimonial has been approved
    """
    email_template_html = "email_assets/testimonial/testimonial_approved.html"
    email_template_text = "email_assets/testimonial/testimonial_approved.txt"
    
    admin_email_address = settings.EMAIL_HOST_USER
    
    return _send_email_helper(email_template_html,
                             email_template_text,
                             subject=subject,
                             from_email=admin_email_address,
                             to_email=user.email,
                             username=user.username,
                             )



def _send_email_helper(email_template_html, email_template_text, **kwargs):
    """
    A private helper function to send an email with the specified templates and context.

    Parameters:
        - email_template_html (str): Path to the HTML email template.
        - email_template_text (str): Path to the plain text email template.
    Parameters for kwargs:
      
        - subject (str): The subject line of the email.
        - from_email (str): The sender's email address.
        - to_email (str): The recipient's email address.
        - username (str): The recipient's username.
        - verification_url (str): The verification URL to be included in the email.

    Returns:
        - bool: True if the email was sent successfully, False otherwise.
    """
    return send_email(
        subject=kwargs["subject"],
        from_email=kwargs["from_email"],
        to_email=kwargs["to_email"],
        email_template=email_template_html,
        text_template=email_template_text,
        context={
            "username":kwargs["username"],
            "verification_url": kwargs.get("verification_url"),
            "email_address":kwargs.get("email_address"),
        }
    )

    
    