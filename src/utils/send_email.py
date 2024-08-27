from types import NoneType
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from typing import Optional

def send_email(subject:str, 
               from_email:str, 
               to_email:str, 
               email_template:str, 
               text_template:Optional[str]=None, 
               context: dict = None) -> bool:
    """
    Send an email with both HTML and plain text content.

    Args:
        subject (str): The subject of the email.
        from_email (str): The sender's email address.
        to_email (str): The recipient's email address.
        email_template (str): The path to the HTML template file.
        text_template (str, optional): The path to the plain text template file.
        context (dict): The context dictionary for rendering the templates.
     
    Returns:
        None
    """
    
    html_content = render_to_string(email_template, context)
    
    if text_template:
        text_content = render_to_string(text_template, context)
    else:
        text_content = ''
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True

    # try:
    #     msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
    #     return True
    # # except Exception as e:
    # #     print(f"Failed to send email: {e}")
        
    # except NoneType as e:
    #     print(f"Error: {e}")
        
    return False